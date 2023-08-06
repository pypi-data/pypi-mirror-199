"""
Application db table factory.
"""
from dataclasses import dataclass
from typing import Any

import boto3


@dataclass
class DynamoDbTableFactory:
    """
    DynamoDB table factory.
    """

    table_name: str

    def __call__(self) -> Any:
        return boto3.resource("dynamodb").Table(self.table_name)
