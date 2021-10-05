Fraud Demo
---

## Project

Create resources:
- A GCP project
- A GCS bucket
- 2 BigQuery datasets: feast (conventionally for Feast temp tables), another dataset for project data tables

Set the envs
- `PROJECT_ID`
- `BUCKET_NAME`
- `BIGQUERY_DATASET_NAME`


## Feast

### Apply

- Source table: `BigQuery Data Viewer`
- Feast dataset: `roles/bigquery.dataEditor`
- Firestore: `Cloud Datastore User`

### Get Historical Features

- BigQuery project-level: `bigquery.jobs.create`, `bigquery.readsessions.create`, `bigquery.readsessions.getData`
- BigQuery Feast dataset: `roles/bigquery.dataEditor`
- BigQuery Source table: `BigQuery Data Viewer`

### Materialize

- BigQuery project-level: `bigquery.jobs.create`, `bigquery.readsessions.create`, `bigquery.readsessions.getData`
- BigQuery Source table: `BigQuery Data Viewer`
- Firestore: `Cloud Datastore User`

### Get Online Feature

- Firestore: Cloud Datastore User

### GCS
- GCS: storage.bucket.get, storage.objects.*
