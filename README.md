# About this Project
This project contains an application to store the contents of .txt-files from the [Cosmas2 database of german language][1] in a snowflake database and return the contents as .csv-files. Said application is implemented with flask and served with gunicorn. Depending on the deployment model gunicorn might be served with NginX.
The project includes 3 different ways of deployment, described more in depth in their folders.

The following tools/frameworks/cloud-providers have been used to create/automate this process:
* Terraform
* Ansible
* Flask
* Pipenv
* Unittest
* Gunicorn
* Nginx
* Docker/Docker-Compose
* Snowflake
* Azure/DevOps/CICD-pipelines

# Prerequisits
- as described in [terraform][2]

# Deployment Goal
Choose one of the deployment models:
1. [Deploy the NginX+Gunicorn/Flask application directly to a VM with Ansible][3]
2. [CICD pipeline with Gunicorn/Flask to Azure Container Instances][4]
3. [CICD pipeline with NginX+Gunicorn/Flask and Docker-Compose to Azure App Services][5]

**Disclaimer:**
My azure test month ran out before I finished so 3. isn't 100% operational yet (only endpoint "/" is available, for the other endpoints it needs https enabled so that the snowflake-connector can work) and has some open issues in terms of automation. 1. and 2. should work as advertised.
The technologies aren't chosen to be a best fit for the problems but to showcase my ability to use them all. For the scope of the script I have automated here a simple function app might have sufficed.



[1]: https://cosmas2.ids-mannheim.de/cosmas2-web/
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform
[3]: https://github.com/Philipeace/cloudsolutions/tree/main/ansible
[4]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/CICDContainerInstance
[5]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/CICDComposeWebApp

