import logging
from django.shortcuts import render
from django.views import View, generic
from django.contrib import messages
from .forms import CoordinatesInputForm
from .publish import push_payload


logger = logging.getLogger(__name__)

class PublishMessages(View):
    """
    View for publishing messages.
    """
    form_cls = CoordinatesInputForm
    initial = {}
    template_name = "TSP.html"

    def get(self, request):
        """
        render the form over GET call.
        """
        return render(request, self.template_name, {"form": CoordinatesInputForm(request.GET)})

    def post(self, request):
        """
        Sending coordinates to publisher queue.
        """
        form = self.form_cls(request.POST)
        
        if not form.is_valid():
            messages.error(request, form.errors)
        else:
            no_of_vehicle = form.cleaned_data["no_of_vehicle"]
            coordinates = form.cleaned_data["coordinates"]
            try:
                logger.info("Pushing payload to google pub/sub topic queue.")
                push_payload(no_of_vehicle, list(coordinates))
            except Exception as e:
                logger.error(f"Error in pushing data payload to topics queue : {e}")
                messages.error(request, e)
                return render(request, self.template_name, {"form": form})

            messages.success(request, 'Request is published successfully.')
        
        return render(request, self.template_name, {"form": form})
