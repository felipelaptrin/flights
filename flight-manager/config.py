import os


def boolean_string_to_bool(string: str) -> bool:
    if string.upper() == "TRUE":
        return True
    return False


# SET PYTHON LOGGING LEVEL
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO")

# TRESHOLD FOR DEFINING HOW MANY CRAWLERS (LAMBDA FUNCTION) CAN RUN AT THE SAME TIME
# IF NUMBER OF DESIRED CRAWLER IS HIGHER THAN THIS, THE CRAWLERS WILL NOT RUN
MAX_CRAWLERS = int(os.getenv("MAX_CRAWLERS", 100))

# NAME OF THE AWS LAMBDA FUNCTION CONTAINING THE CRAWLER FUNCTION
CRAWLER_LAMBDA_NAME = os.getenv("CRAWLER_LAMBDA_NAME")

# NAME OF THE AWS REGION THAT CONTAINS THE LAMBDA FUNCTION
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# DATE PARSER
DATE_FORMAT = "%d/%m/%Y"

# IF DRY_RUN MODE IS ENABLED THE LAMBDAS WILL NOT BE TRIGGERED. ACCEPT 'TRUE' and 'FALSE'
DRY_RUN = boolean_string_to_bool(os.getenv("DRY_RUN", "TRUE"))
