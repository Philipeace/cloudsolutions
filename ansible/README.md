# About this Project
This project deploys the flask app using ansible to configure and run the app with gunicorn and nginx on a remote machine.

# Prerequisits:
- as described in [terraform/Snowflake][1]
- ansible installed

# Get Started
**To deploy the software:**
1. create [terraform/Snowflake][1] infrastructure
2. install ssh on the host machine
   ```
    sudo apt install ssh
   ```
3. on the control node run
   ```
    ssh-copy-id username@HostIP
   ```
4. **fill in missing information** in inventory.yml and the missing path to the /app directory in setup-playbook.yml
5. run ansible with
   ```
    ansible-playbook -i inventory.yml setup-playbook.yml
   ```
You should now be able to see the website when opening the IP of the VM in a browser.

[Back to main][2]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/