# Fact-checking Flow

## Requirements
* Python 3.6.4
* MySQL

You will need to create the MySQL database and user before running the application for the first time.  You can use a GUI admin tool,
or you can log in to MySQL as the `root` user (or other admin) and execute the following commands:

    CREATE DATABASE fact_flow_db;
    GRANT ALL PRIVILEGES
      ON fact_flow_db.* TO 'test_user'@'localhost'
      IDENTIFIED BY 'test_user_pass';


## Installation
1. Set and activate a Python virtual environment. Be sure to use Python 3.
2. Once you are in an active virtual environment, install all required dependencies `pip install -r requirements.txt`
3. Change directories into `rest-api/`, `cd rest-api`
4. (First time only) Initialize the database `python manage.py migrate`
5. Run the API server `python manage.py runserver`
