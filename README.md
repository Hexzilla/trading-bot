# AutoTrader
Auto stock/options trading application using the TDAmeritrade API

1) Set up the venv with Python 3.9
   run setup.[sh|bat] to create and activate the Python virtual environment and install the packages.
 
2) Create Database: /db/sqlite_db_generator.py
   - Run sqlite_db_generator.py to create the SQLite database

3) To run the multi-user Flask app: /rest-api/main.py
    - Development: Configure the Run configuration with the following arguments to enable adhoc SSL:
        --host=0.0.0.0 --port=8443 --cert=adhoc
    - Production: The Flask app must run with a domain name with SSL certificate.
    - Endpoints: https://localhost:8443/authorize?api_key=API_KEY_HERE

4) Test Service: /brokers/tda/test/__init__.py 
   After using the Flask endpoint to authorize the application to access the TD Ameritrade account,
   the token file is generated in the /brokers/tda/auth/tokens folder.  Open the __init__.py and set the API_KEY value.

   The service reads the token file to create the TD Ameritrade client and ready to pull the data.