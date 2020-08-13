# cloud-run

## Description
This is code for a containerized service to be deployed on Google's cloud-run. The service is currently a "helloworld" service - it provides a http request endpoint that returns "Hello there!" or "Hello {name}!" where the name is submitted by the user. The service also submits request logs.

## Build instructions
```
docker build -t helloworld:local .
```

## Test locally:
```
> docker run -p 8080:8080 \
-v=$HOME/.config/gcloud/application_default_credentials.json:\
/root/.config/gcloud/application_default_credentials.json \
helloworld:local
> curl --data-urlencode "who=David" --get http://0.0.0.0:8080/ \
-H "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')"
> Hello David!
```

