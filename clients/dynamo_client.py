import boto3
from boto3.dynamodb.conditions import Key
import logging
from botocore.exceptions import ClientError


class DynamoDBClient:
    """
    A robust DynamoDB Client that abstracts complex operations
    and provides simplified methods for CRUD and querying operations.

    TODO:
        1. Add credentials for boto3
        2. Add type hints
        3. Add error handling and logging
        4. Add support for other DynamoDB transactions
    """

    def __init__(self, table_name, dynamo_resource=None):
        """
        Initializes the DynamoDBClient.

        Args:
            table_name (str): The name of the DynamoDB table to interact with.
            dynamo_resource (boto3.resource, optional): The DynamoDB resource object.
                If not provided, a default boto3 DynamoDB resource is used.
        """
        assert table_name, "Table name must not be empty"
        self.dynamo_resource = dynamo_resource or boto3.resource('dynamodb')
        self.table = self.dynamo_resource.Table(table_name)
        self.table_name = table_name

    def _log_query_details(self, partition_key, partition_value, sort_key=None, sort_value=None, index_name=None,
                           filter_expression=None):
        """
        Logs query details for traceability.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str, optional): The sort key name.
            sort_value (str, optional): The sort key value.
            index_name (str, optional): The name of the index to query.
            filter_expression (str, optional): Additional filter expression for the query.
        """
        logging.info(f"Querying Table: {self.table_name} | PK: {partition_key} | PK_Value: {partition_value} "
                     f"SK: {sort_key} | SK_Value: {sort_value} | Index: {index_name} | Filter: {filter_expression}")

    def _build_key_expression(self, partition_key, partition_value, sort_key=None, sort_value=None, comparator='eq'):
        """
        Creates the key expression for querying.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str, optional): The sort key name.
            sort_value (str or tuple, optional): The sort key value or range of values.
            comparator (str): Comparison operator. Options are 'eq', 'gt', 'gte', and 'between'.

        Returns:
            dict: A dictionary containing the KeyConditionExpression for query execution.
        """
        key_expr = Key(partition_key).eq(partition_value)
        if sort_key and sort_value:
            if comparator == 'eq':
                key_expr &= Key(sort_key).eq(sort_value)
            elif comparator == 'gt':
                key_expr &= Key(sort_key).gt(sort_value)
            elif comparator == 'gte':
                key_expr &= Key(sort_key).gte(sort_value)
            elif comparator == 'between':
                key_expr &= Key(sort_key).between(sort_value[0], sort_value[1])
        return {"KeyConditionExpression": key_expr}

    def _execute_query(self, key_expr, index_name=None, filter_expression=None,
                       projection_expression=None, descending_order=False, last_evaluated_key=None, limit=None):
        """
        Executes a DynamoDB query based on the provided parameters.

        Args:
            key_expr (dict): The key condition expression built for the query.
            index_name (str, optional): Name of the index to query.
            filter_expression (str, optional): Additional filter expression for the query.
            projection_expression (str, optional): Attributes to be projected in the query.
            descending_order (bool): Whether to return results in descending order.
            last_evaluated_key (dict, optional): Key to resume querying from.
            limit (int, optional): Maximum number of items to retrieve.

        Returns:
            tuple: A tuple containing a list of retrieved items and a last evaluated key for pagination.
        """
        query_params = key_expr.copy()

        if index_name:
            query_params["IndexName"] = index_name
        if filter_expression:
            query_params["FilterExpression"] = filter_expression
        if projection_expression:
            query_params["ProjectionExpression"] = projection_expression
        if descending_order:
            query_params["ScanIndexForward"] = False
        if last_evaluated_key:
            query_params["ExclusiveStartKey"] = last_evaluated_key
        if limit:
            query_params["Limit"] = limit

        try:
            response = self.table.query(**query_params)
            items = response.get("Items", [])
            last_evaluated_key = response.get("LastEvaluatedKey", None)
            return items, last_evaluated_key
        except ClientError as e:
            logging.error(f"Query failed: {e.response['Error']['Message']}")
            raise e

    def insert_item(self, item):
        """
        Inserts a new item into the DynamoDB table.

        Args:
            item (dict): A dictionary representing the item to insert.

        Raises:
            ClientError: If the insert operation fails.
        """
        try:
            self.table.put_item(Item=item)
            logging.info(f"Item inserted successfully: {item}")
        except ClientError as e:
            logging.error(f"Failed to insert item: {e.response['Error']['Message']}")
            raise e

    def fetch_items(self, partition_key, partition_value, sort_key=None, sort_value=None, index_name=None,
                    filter_expression=None, projection_expression=None, descending_order=True):
        """
        Retrieves items based on the partition and optional sort key.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str, optional): The sort key name.
            sort_value (str, optional): The sort key value.
            index_name (str, optional): The name of the index to query.
            filter_expression (str, optional): A filter expression to further refine results.
            projection_expression (str, optional): Attributes to retrieve.
            descending_order (bool): Whether to return results in descending order.

        Returns:
            list: A list of retrieved items.
        """
        self._log_query_details(partition_key, partition_value, sort_key, sort_value, index_name, filter_expression)
        key_expr = self._build_key_expression(partition_key, partition_value, sort_key, sort_value)
        items, _ = self._execute_query(key_expr, index_name, filter_expression, projection_expression, descending_order)
        return items

    def fetch_items_with_sort_greater_than(self, partition_key, partition_value, sort_key, sort_value,
                                           index_name=None, filter_expression=None, projection_expression=None):
        """
        Fetches items where the sort key is greater than a specified value.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str): The sort key name.
            sort_value (str): The sort key value to compare with (greater than).
            index_name (str, optional): The name of the index to query.
            filter_expression (str, optional): Additional filter expression.
            projection_expression (str, optional): Attributes to project in the result.

        Returns:
            list: A list of matching items.
        """
        self._log_query_details(partition_key, partition_value, sort_key, sort_value, index_name, filter_expression)
        key_expr = self._build_key_expression(partition_key, partition_value, sort_key, sort_value, comparator='gt')
        items, _ = self._execute_query(key_expr, index_name, filter_expression, projection_expression)
        return items

    def fetch_items_with_sort_range(self, partition_key, partition_value, sort_key, sort_range_start, sort_range_end,
                                    index_name=None):
        """
        Fetches items where the sort key is between two values.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str): The sort key name.
            sort_range_start (str): The start value of the sort key range.
            sort_range_end (str): The end value of the sort key range.
            index_name (str, optional): The name of the index to query.

        Returns:
            list: A list of matching items.
        """
        self._log_query_details(partition_key, partition_value, sort_key, f"{sort_range_start} to {sort_range_end}",
                                index_name, None)
        key_expr = self._build_key_expression(partition_key, partition_value, sort_key,
                                              (sort_range_start, sort_range_end), comparator='between')
        items, _ = self._execute_query(key_expr, index_name)
        return items

    def paginate_query(self, partition_key, partition_value, sort_key=None, sort_value=None, index_name=None,
                       last_evaluated_key=None, limit=None, filter_expression=None, descending_order=False,
                       projection_expression=None):
        """
        Retrieves paginated results for a query based on the partition and sort keys.

        Args:
            partition_key (str): The partition key name.
            partition_value (str): The partition key value.
            sort_key (str, optional): The sort key name.
            sort_value (str, optional): The sort key value.
            index_name (str, optional): The name of the index to query.
            last_evaluated_key (dict, optional): Key to resume querying from.
            limit (int, optional): Maximum number of items to retrieve.
            filter_expression (str, optional): Additional filtering criteria.
            descending_order (bool): Whether to return results in descending order.
            projection_expression (str, optional): Attributes to retrieve.

        Returns:
            tuple: A tuple containing a list of retrieved items and the last evaluated key.
        """
        self._log_query_details(partition_key, partition_value, sort_key, sort_value, index_name, filter_expression)
        key_expr = self._build_key_expression(partition_key, partition_value, sort_key, sort_value)
        return self._execute_query(key_expr, index_name, filter_expression, projection_expression, descending_order,
                                   last_evaluated_key, limit)

    def batch_get_items(self, partition_key, partition_values):
        """
        Retrieve multiple items in a batch based on partition key values.

        Args:
            partition_key (str): The partition key name.
            partition_values (list): A list of partition key values to retrieve items for.

        Returns:
            list: A list of items retrieved in the batch.

        Raises:
            ClientError: If the batch get operation fails.
        """
        keys = [{partition_key: val} for val in partition_values]
        request_items = {"Keys": keys, "ConsistentRead": True}

        try:
            response = self.dynamo_resource.batch_get_item(
                RequestItems={self.table_name: request_items},
                ReturnConsumedCapacity="TOTAL"
            )
            return response["Responses"][self.table_name]
        except ClientError as e:
            logging.error(f"Batch get operation failed: {e.response['Error']['Message']}")
            raise e
