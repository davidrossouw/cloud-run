## Local Dev

> curl -H "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')"  -G 0.0.0.0:8080 --data-urlencode "who=David"
> Hello David!

> curl \
--header "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" \
-F 'image=@/Users/davidrossouw/Documents/my_projects/cloud-run/simpson-api/data/abraham_grampa_simpson_0.jpg' \
'0.0.0.0:8080/predict'

## Build
> docker build . --tag gcr.io/my-cloud-run-284115/object-detection:latest
> docker push gcr.io/my-cloud-run-284115/object-detection:latest


## Deploy

gcloud run deploy object-detection \
  --image gcr.io/my-cloud-run-284115/object-detection:latest \
  --memory 4Gi \
  --region us-east1 \
  --platform managed

## cUrl

> curl \
--header "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" \
-F 'image=@/Users/davidrossouw/Documents/my_projects/cloud-run/simpson-api/data/abraham_grampa_simpson_0.jpg' \
'https://object-detection-2xihskugxq-ue.a.run.app/predict'


## Model

https://tfhub.dev/tensorflow/efficientdet/d0/1
