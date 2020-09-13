
> curl -H "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')"  -G 0.0.0.0:8080 --data-urlencode "who=David"
> Hello David!

> curl -H "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" -d '{"start_date":"2020-07-01", "end_date":"2020-07-07"}' -H 'Content-Type: application/json' 0.0.0.0:8080/run


> curl --location --request POST 'http://localhost:8080/predict' \
--header "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" \
--form 'file=@/Users/davidrossouw/Documents/my_projects/cloud-run/simpson-api/data/abraham_grampa_simpson_0.jpg'

> curl \
--header "Authorization: Bearer $(gcloud config config-helper --format 'value(credential.id_token)')" \
-F 'image=@/Users/davidrossouw/Documents/my_projects/cloud-run/simpson-api/data/abraham_grampa_simpson_0.jpg' \
'0.0.0.0:8080/predict'
