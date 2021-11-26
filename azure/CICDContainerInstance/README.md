# About this Project
This project deploys the flask app using docker-compose to run the app with gunicorn in one container and nginx in another. It is automated with a CICD pipeline that runs unit-tests, builds the compose images and deploys them to an existing AppService on Azure.


# Prerequisits
- as described in [terraform][1]

# Get Started
**To create the CICD pipeline:**
1. create [terraform/Snowflake_Azure][2] infrastructure

**In Azure Portal (or AzureCLI):**

2. **enable admin access** in the container registry **txtappregistry** and copy the **password** for later use

**In Azure DevOps:**

3.  create an **azure git repository** from the contents of this folder in the **txtconverter_comsas2** project  
4.  In Pipelines **create an empty pipeline** and link your azure repository from step 2
5.  Create the following variables on the pipeline and assign them your values if open:
   ```
    $SNOWFLAKE_ACCOUNT

    $SNOWFLAKE_USERNAME

    $SNOWFLAKE_PASSWORD

    $acrPassword = your password from 3. goes here

    $azSubscription = enter your azure subscription information here

    $acrName = txtappregistry (leave as is)

    $acrLoginServer = txtappregistry.azurecr.io (leave as is)

    $resourceGroup = txtapprg (leave as is)
    
   ```
 
**In the azure git repository:**

6.   Copy the **dockerRegistryServiceConnection** value from azure-pipelines.yml and put it in container-pipeline.yml
7.   **delete** azure-pipelines.yml and **rename** container-pipeline.yml to azure-pipelines.yml
8.   upload change
   ```
    git add azure-pipelines.yml

    git commit -m "your awesome commitmessage"

    git push
   ```

9.    watch magic unfold

# Run locally:
If you have created the [terraform/Snowflake][3] infrastructure and created the first three (snowflake) variables from 5. on your environment run:
   ```
    docker build -t flask_container .

    docker run -e SNOWFLAKE_USERNAME -e SNOWFLAKE_PASSWORD -e SNOWFLAKE_ACCOUNT -p 80:80 flask_container
   ```

You should now be able to see the app running on http://localhost

For more information on how to run the app without docker see [Flask/Gunicorn][4]

[Back to main][5]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake_Azure
[3]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake
[4]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/CICDComposeWebApp/app
[5]: https://github.com/Philipeace/cloudsolutions/tree/main/