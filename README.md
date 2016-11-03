# relay

A shim to get webhook POSTs from Docker Hub and post them to [Slack](http://slack.com).


## Setup

### Make a new Incoming Webhook in Slack's Integrations

![](http://i.imgur.com/y2FWZme.png)

Copy the webhook URL.

![](http://i.imgur.com/FPVIDeq.png)

### How to run on Docker

After running

``` bash
docker run --env SLACK_URL='https://hooks.slack.com/services/PUT/YOURS/HERE' --env RELAY_PORT=8080 --env=DEFAULT_CHANNEL='#dev' --env=IMAGE_URL='http://i.giphy.com/LYDNZAzOqrez6.gif' -p 8080:8080 dailyhotel/relay
```

visit <http://your-webserver-goes-here.com:8080/relay> and you should get the message "Relay is running."

Now, when your build pushes to Docker Hub you should get a nice notification in Slack.

![](https://raw.githubusercontent.com/DailyHotel/relay/master/docs/images/sample-msg.png)

### How to run on Kubernetes

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: slackrelay
  labels:
    app: slackrelay
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: slackrelay
  type: LoadBalancer
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: slackrelay
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: slackrelay
    spec:
      containers:
      - name: slackrelay
        image: dailyhotel/relay:latest
        env:
          - name: SLACK_URL
            value: "https://hooks.slack.com/services/PUT/YOURS/HERE"
          - name: RELAY_PORT
            value: "8080"
          - name: DEFAULT_CHANNEL
            value: "#dev"
        ports:
        - name: slackrelay-port
          containerPort: 8080
```

### Customize

Clone this repo.
Edit a file `channel_selector.json` in the repo directory that maps the repo path on Docker Hub to a channel in your Slack chat.
For example, to map <https://registry.hub.docker.com/u/psathyrella/ham/> and [our C++ build environment](https://registry.hub.docker.com/u/matsengrp/cpp/) to the relevant channels, the file would be:

``` json
{
    "psathyrella/ham":"#bcell",
    "matsengrp/cpp":"#infrastructure"
}
```
