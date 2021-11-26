# About this Project
This project deploys the flask app using docker-compose to run the app with gunicorn in one container and nginx in another. It is automated with a CICD pipeline that runs unit-tests, builds the compose images and deploys them to an existing AppService on Azure.

# Important:
    Open issues:
        - snowflake-connector doesn't work without https enabled
        - automate 3-10 under Get Started with terraform/azcli
    Working items:
        - CICD pipeline for Compose WebApp
        - Compose Nginx-Gunicorn/Flask application

# Prerequisits
- as described in [terraform][1]

# Get Started
**To create the CICD pipeline:**
1.  create [terraform/Snowflake_Azure][2] infrastructure
2.  create a **github repository** from the contents of this folder

**In Azure Portal (or AzureCLI):**

3.  create a **storage account** 
4.  create a **file** share in the storage account
5.  **enable admin access** in the container registry **txtappregistry** and copy the **password** for lateruse
6.  create a App Service WebApp for Containers called **txtapp** (if the name is taken make sure to adjust the name in the deploy stage as well)
7.  in txtapp go to **configuration** and create the following key, values there:
   ```
    DOCKER_REGISTRY_SERVER_PASSWORD=**your password from 5. goes here**

    DOCKER_REGISTRY_SERVER_USERNAME=txtappregistry

    DOCKER_REGISTRY_SERVER_URL=https://txtappregistry.azurecr.io
   ```

8.  go to txtapp's identity section and enable system assigned identities
9.  in the container registry under IAM Control add the Role ACR pull to txtapp with system assigned identity enabled
10. create a path mapping in txtapp's configuration to the file share from 4 called azstmnt
 
**In Azure DevOps:**

11. In Settings create a service connection to your subscription called **txtappsubendpoint**
12. In Pipelines create a new empty pipeline and link your github repository from step 2
13. Create the following variables in the pipeline and assign them your values:
   ```
    $SNOWFLAKE_ACCOUNT

    $SNOWFLAKE_USERNAME

    $SNOWFLAKE_PASSWORD

    $azSubscription
   ```
   
**In the github repository:** 

14. Copy the **dockerRegistryServiceConnection** value from azure-pipelines.yml and put it in compose-pipeline.yml
15. **delete** azure-pipelines.yml and **rename** compose-pipeline.yml to azure-pipelines.yml
16. upload change
   ```
    git add azure-pipelines.yml

    git commit -m "your awesome commitmessage"

    git push
   ```
17. watch magic unfold


# Run locally:
If you have created the [terraform/Snowflake][3] infrastructure and created the first 3 variables from 2.3 on your environment run:
   ```
    docker-compose build --no-cache --pull

    docker-compose up
   ```

Common pitfalls:
   ```
    SNOWFLAKE_ACCOUNT = O13IJkl.west-europe.azure (not just O13IJkl)
   ```

[Back to main][4]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake_Azure
[3]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake
[4]: https://github.com/Philipeace/cloudsolutions/tree/main/