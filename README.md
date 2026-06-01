# Steps to setup this project:
## 1. Setup central control api
1.1  Setup
- Installation
download ngrok: 
Windows: microsoft store install ngrok en setup zodat linked github repo's de api kunnen bereiken
ubuntu: https://ngrok.com/docs/guides/device-gateway/linux

- Github token
1. go to: https://github.com/settings/personal-access-tokens and create a fine-grained token(more secure than classic)
2. Token Settings(name/desc/expiration up to you):
2.1 Repository access: (whichever), i chose all due to testing my local repositories as well 
2.2 Permissions(MUST HAVES for access/working of this project)
- Commit statuses:  Read and write
- Contents:         Read-only
- Metadata:         Read-only
- Pull requests:    Read-only


- .env
Copy the .env.example and save as .env.local, change the github token to your personal token(used for cloning repo's for sbom and vulnerability scanning)


1.2 commands to run the project alongside each other(ngrok is for running the project through a proxy so that you can reach it publicly)
- docker compose up --build
- ngrok http 8000


## 2. Linking a repository
2.1 Setup webhook
- Go to the specific repository -> settings -> webhooks -> add webhook
- Webhook settings:
1. Payload URL:     https://(link from ngrok)/webhook
2. Content type:    application/json


2.2 Enable blocking in the repo(currently in progress)
- IMPORTANT NOTE: for branch protection rules/rulesets enforcement being locked behind github teams(paying) the repo's where you want to apply the status blocking have to be public unless you want to pay for the team version($4 per user per repo) then it could be private

- go to specific repository -> settings -> branches -> add classic branch protection rule
(NOTE: hoe het momenteel werkt moet er eerst op z'n minst een keer worden gepusht met runnende applicatie zodat de security-scan status optie er tussen komt te staan)
1. name: main
2. Require status checks to pass before merging(check), source = "security-scan"