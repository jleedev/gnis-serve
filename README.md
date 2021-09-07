
```
gcloud builds submit --tag gcr.io/$PROJECT/gnis --timeout 15m
gcloud run deploy --platform managed gnis --image gcr.io/$PROJECT/gnis --memory 1024Mi
```

Available here: https://gnis-x5m3uj6fcq-uc.a.run.app/capabilities
