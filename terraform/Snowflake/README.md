# Prerequisits
- snowflake account (required)
- terraform installed

# Get Started
**To create the snowflake infrastructure for ansible [automation][1] or local tests:**
1. fill in the values in terraform.tfvars
2. run the following commands:
   ```
    terraform init

    terraform plan
    
    terraform apply
   ```

Common pitfalls:
   ```
    SNOWFLAKE_ACCOUNT = O13IJkl.west-europe.azure (not just O13IJkl)
   ```

[Back to main][2]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/ansible
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/