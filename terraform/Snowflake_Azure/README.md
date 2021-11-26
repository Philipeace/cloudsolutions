# Prerequisits
- snowflake account (required)
- azure account (required)
- azure cli installed
- terraform installed

# Get Started
**To create the snowflake infrastructure for [CICD pipelines][1] run the following commands:**
1. fill in the values in terraform.tfvars
2. run the following commands:
   ```
    az login

    terraform init

    terraform plan
    
    terraform apply
   ```
   
Common pitfalls:
   ```
    SNOWFLAKE_ACCOUNT = O13IJkl.west-europe.azure (not just O13IJkl)
   ```

[Back to main][2]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/azure
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/