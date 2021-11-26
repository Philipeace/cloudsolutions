# About this Project
This project contains an application to store the contents of .txt-files from searches on the [Cosmas2 database of german language][1] in a snowflake database and return the extracted contents as .csv-files. The readme's in the [/app folders will give more insight to this flask app][2]. Said app is running with gunicorn. Depending on the deployment model gunicorn might be proxied by NginX. 
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
- as described in [terraform][3]

# Deployment Goal
Choose one of the deployment models:
1. [Deploy the NginX+Gunicorn/Flask application directly to a VM with Ansible][4]
2. [CICD pipeline with Gunicorn/Flask to Azure Container Instances][5]
3. [CICD pipeline with NginX+Gunicorn/Flask and Docker-Compose to Azure App Services][6]

**Disclaimer:**
My azure test month ran out before I finished so 3. isn't 100% operational yet (only endpoint "/" is available, for the other endpoints it needs https enabled so that the snowflake-connector can work) and has some open issues in terms of automation. 1. and 2. should work as advertised.
The technologies aren't chosen to be a best fit for the problems but to showcase my ability to use them all. For the scope of the script I have automated here a simple function app might have sufficed.

Common pitfalls:
   ```
    SNOWFLAKE_ACCOUNT = O13IJkl.west-europe.azure (not just O13IJkl)
   ```

[1]: https://cosmas2.ids-mannheim.de/cosmas2-web/
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/ansible/app
[3]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform
[4]: https://github.com/Philipeace/cloudsolutions/tree/main/ansible
[5]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/CICDContainerInstance
[6]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/CICDComposeWebApp

