
```
gcloud builds submit --tag gcr.io/$PROJECT/gnis --timeout 15m
gcloud run deploy --platform managed gnis --image gcr.io/$PROJECT/gnis --memory 1024Mi
```

