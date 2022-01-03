# Services Around Travel Salesman Problem

As a back-end engineer you are responsible for developing a wrapping service around this
library that communicates through publish/subscribe queues.

## Installation by Bash .sh
- Run `./script.sh` in terminal

## Installation Guide (Manual)

- Clone the repository and `cd <checkout-directory>` to in it.
- Docker-based environment for running the TSP. Install the [Docker](https://docs.docker.com/get-docker/) to Use it.
- Run `docker-compose build` for building images.
- Run `docker-compose up` to start the containers.

Visit `http://127.0.0.1:8000/` to get the view of Django based application.

## Design Details
For the TSP, I used the [google pub/sub](https://cloud.google.com/pubsub/docs/overview) services to communicate asynchronously that actually provides messaging between applications. Cloud Pub/Sub is designed to provide asynchronous messaging between applications. The main application `TSP` worked as Publisher for sending messages to a "topic" queue and on the other hand, another background service named as `subscriber` is used to `pull messages` from `topic` queue to run the solution over the given locations and display the routes over the console (at the moment)

Over the index page of `TSP` application, User is able to specify the following inputs:
- Number of vehicles.
- (x,y) location pairs.

and publish the data to `/publish/ `endpoint.

[![screencapture-127-0-0-1-8000-2022-01-02-17-04-48.png](https://i.postimg.cc/mg7PH5yt/screencapture-127-0-0-1-8000-2022-01-02-17-04-48.png)](https://postimg.cc/FYsFtGq4)

[![screencapture-127-0-0-1-8000-publish-2022-01-02-17-05-46.png](https://i.postimg.cc/k4HJZQv0/screencapture-127-0-0-1-8000-publish-2022-01-02-17-05-46.png)](https://postimg.cc/N91v2rVD)

[![screencapture-127-0-0-1-8000-publish-2022-01-02-19-16-15.png](https://i.postimg.cc/28F0dhNG/screencapture-127-0-0-1-8000-publish-2022-01-02-19-16-15.png)](https://postimg.cc/dL3Rw71Z)


#### NOTE: For performance improvements, when expecting a lot of data to manipulate and messages then We can design the subscriber to use the concept of multiprocessing workers to do job in parallel.

#### NOTE: Pulling routes details to User UI needs to implement as I was out of time to work on this side.


## Environments Variables:
For the assignment purposes, The `.env` and `.json` files are added with values here just for a plug-&-play configured version for project & topics but ones can update those variables for sending messages to its own project over Google cloud.

For authentication keys visit [authentication](https://cloud.google.com/docs/authentication/getting-started).

Keep the default ones OR override the following settings in your `.env` file:

```
PUB_SUB_TOPIC=
PUB_SUB_PROJECT=
PUB_SUB_SUBSCRIPTION=
GOOGLE_APPLICATION_CREDENTIALS='<path-to-json-file>'
```

## Testing:

### Run Python tests
docker-compose run --rm web ./manage.py test 
##### Added some few tests for the view basic functionality.

## Docker Images
The following commands can be used to attach with a container.
- `docker attach web`
- `docker attach subscriber`

[![Screenshot-2022-01-02-at-6-19-44-PM.png](https://i.postimg.cc/K8sZpXr9/Screenshot-2022-01-02-at-6-19-44-PM.png)](https://postimg.cc/hXTWh5Yx)
