## cUrl

> curl \
--header "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" \
-F 'image=@/Users/david/Documents/my_projects/cloud-run/wyze/images/cat1.jpg' \
'https://object-detection-2xihskugxq-ue.a.run.app/predict'


## Model

https://tfhub.dev/tensorflow/efficientdet/d0/1
