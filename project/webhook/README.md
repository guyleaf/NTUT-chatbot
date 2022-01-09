## Cloud Functions For linebot_webhook

```powershell
gcloud beta functions deploy linebot_webhook_gpu_a --region=asia-east1 --allow-unauthenticated --entry-point=main --runtime=python39 --source=https://source.developers.google.com/projects/chatbot-project-3135/repos/github_guyleaf_ntut-chatbot/moveable-aliases/develop/paths/project/webhook --set-secrets='CHANNEL_SECRET=projects/567768457788/secrets/GPU_A_LINE_CHANNEL_SECRET_TOKEN:1,CHANNEL_ACCESS_TOKEN=projects/567768457788/secrets/GPU_A_LINE_CHANNEL_ACCESS_TOKEN:1,SQL_PASSWORD=projects/567768457788/secrets/GPU_A_SQL_PASSWORD:1' --trigger-http --project=chatbot-project-3135
```
