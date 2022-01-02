""" Computation form """
from django import forms
from .constants import (
    locations_msg,
    vehicle_msg
)

class CoordinatesInputForm(forms.Form):
    """Form for taking location as input"""
    no_of_vehicle = forms.CharField(max_length=100)
    coordinates = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': locations_msg,
            'class': 'coordinates-style'
            }),
        )
    
    # this function will be used for the validation for coordinates.
    def clean_coordinates(self):
        # extract the coordinates field from the data.
        coordinates = self.cleaned_data.get('coordinates')
        
        try:
            coordinates = eval(coordinates)
        except (NameError, SyntaxError):
            raise forms.ValidationError(locations_msg + ' Either there maybe a NameError or SyntaxError, Take a look for spaces or new lines.' )

        if not isinstance(coordinates, (tuple)):
            raise forms.ValidationError(locations_msg)
 
        return coordinates
    
    # this function will be used for the validation for no_of_vehicle.
    def clean_no_of_vehicle(self):
        # extract the no_of_vehicle field from the data.
        no_of_vehicle = self.cleaned_data.get('no_of_vehicle')
        try:
            no_of_vehicle = int(no_of_vehicle)
        except ValueError:
            raise forms.ValidationError(vehicle_msg)

        return no_of_vehicle
