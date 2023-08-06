import importlib
import os
import sys

import ray

from common_utils.dynamodb_methods import DynamoDbTable

sys.path.append(os.path.abspath(".."))
DynamoDbTable = importlib.import_module(
    "gad-infra.common_utils.dynamodb_methods"
).DynamoDbTable


@ray.remote
class DynamoDbTableRay(DynamoDbTable):
    pass
