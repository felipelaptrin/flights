import json
import os

import botocore
import botocore.session
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from config import AWS_REGION


def get_secret(secret_name: str) -> dict:
    print("Getting Database secrets from AWS...")
    client = botocore.session.get_session().create_client("secretsmanager", region_name=AWS_REGION)
    cache_config = SecretCacheConfig()
    cache = SecretCache(config=cache_config, client=client)
    secret = cache.get_secret_string(secret_name)
    print("Database secrets retrieved correctly!")
    return secret
