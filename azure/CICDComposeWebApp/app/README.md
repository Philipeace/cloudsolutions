# About the Flask/Gunicorn application
This Folder contains the flask app to manage the two endpoints "/" and "/data". 
On "/" the app receives a .txt-file which it then cuts into pieces and stores in a snowflake database. The first few lines of the database are then shown and the contents of the .txt-file are returned as a .csv-file download option.
On "/data" the app shows the first 100 rows of the database and allows for the user to delete single rows.

# Prerequisits
- as described in [terraform/Snowflake][1]
- pipenv installed
- use python 3.9

# Get Started

**To run the app locally:**

1. create [terraform/Snowflake][1] infrastructure
2. install dependencies from pipenv (in this folder):
   ```
    pipenv install
   ```
3. to start the app on linux first set these environment variables:
   
   ```
    $SNOWFLAKE_ACCOUNT

    $SNOWFLAKE_USERNAME

    $SNOWFLAKE_PASSWORD
   ```
4. run unittests with
   
   ```
    pipenv run py.test apitest.py
   ```

5. run flask with

   ```
    pipenv run flask run
   ```
You should now be able to see flask running on http://localhost:5000 and test it with files from [testfiles][2]

6. (optional on linux) run gunicorn with

   ```
    pipenv run gunicorn -c gunicorn.conf.py
   ```

You should now be able to see gunicorn running on http://localhost:8080 and test it with files from [testfiles][2]

Common pitfalls:
   ```
    SNOWFLAKE_ACCOUNT = O13IJkl.west-europe.azure (not just O13IJkl)
   ```

[Back to main][3]

[1]: https://github.com/Philipeace/cloudsolutions/tree/main/terraform/Snowflake
[2]: https://github.com/Philipeace/cloudsolutions/tree/main/azure/ComposeWebApp/app/testfiles
[3]: https://github.com/Philipeace/cloudsolutions/tree/main/