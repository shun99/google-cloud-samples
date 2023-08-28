NAME=${1:-test-chat}
PROJECT_ID=$(gcloud config get project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")

gcloud functions deploy \
    test-chat \
    --gen2 \
    --runtime=python311 \
    --region=asia-northeast1 \
    --source=. \
    --entry-point=hello_chat \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars=PROJECT_NUMBER=${PROJECT_NUMBER},PROJECT_ID=${PROJECT_ID}

