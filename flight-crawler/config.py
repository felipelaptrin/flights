import os


def boolean_string_to_bool(string: str) -> bool:
    if string.upper() == "TRUE":
        return True
    return False


# SET PYTHON LOGGING LEVEL
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO")

# DATE PARSER
DATE_FORMAT = "%d/%m/%Y"

# RUN LOCALLY - USEFUL FOR DEBUGING AND DEVELOPMENT
RUN_LOCALLY_WITH_HEADER = boolean_string_to_bool(os.getenv("RUN_LOCALLY_WITH_HEADER", "FALSE"))

# URL TO CRAWL
GOOGLE_FLIGHTS_URL = os.getenv("GOOGLE_FLIGHTS_URL", "https://www.google.com/flights?hl=us")
MAX_MILHAS_URL = os.getenv("GOOGLE_FLIGHTS_URL", "https://www.maxmilhas.com.br/")


################
### DB SETTINGS
################
# USER OF THE DB
DB_USER = os.getenv("DB_USER")
# PASSWORD OF THE DB
DB_PASSWORD = os.getenv("DB_PASSWORD")
# NAME OF THE DB
DB_NAME = os.getenv("DB_NAME")
# NAME OF THE CLUSTER
DB_CLUSTER = os.getenv("DB_CLUSTER")
# ID OF THE CLUSTER (IN ATLAS)
CLUSTER_ID = os.getenv("CLUSTER_ID")
# NAME OF THE COLLECTION TO STORE THE DOCUMENTS
DB_COLLECTION = os.getenv("DB_COLLECTION")
# WHEN RUNNING IN AWS YOU CAN SPECIFY THE SECRET CONTAINING ALL THE ABOVE DATABASE CREDENTIALS. IF THIS IS EMPTY IT WILL USE THE ENVIRONMENT VARIABLES ABOVE
DATABASE_SECRET_NAME = os.getenv("DATABASE_SECRET_NAME")


################
### AWS
################
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
