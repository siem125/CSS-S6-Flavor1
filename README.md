# Steps to setup this project:
## 1. Setup central control api
1.1  Installation
download ngrok: 
Windows: microsoft store install ngrok en setup zodat linked github repo's de api kunnen bereiken
ubuntu: https://ngrok.com/docs/guides/device-gateway/linux


1.2 run the project commands
- docker compose up --build
- ngrok http 8000


## 2. Linking a repository
2.1 Setup webhook
- Go to the specific repository -> settings -> webhooks -> add webhook
- Paste this in the webhook(the link should be changed to either ngrok result or self hosting this project)
Payload URL:
https://(link)/webhook

Content type:
application/json


2.2 Enable blocking in the repo
- go to specific repository -> settings -> Banches -> add branch ruleset
