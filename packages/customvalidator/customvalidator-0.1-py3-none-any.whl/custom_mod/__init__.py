import logging
from functools import wraps

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


def my_function():
    print('hello')
    return 'hello'


def get_db_cred(func):
    @wraps(func)
    def wrapper_func(req):
        keyVaultName = "myappkv"
        KVUri = f"https://{keyVaultName}.vault.azure.net"
        # credential = DefaultAzureCredential()
        credential = ClientSecretCredential(tenant_id='26afc1b1-8393-439d-aa1a-483105d77dc3',
                                            client_id='9d2fe19f-47e6-498f-b384-6f94b0d55500',
                                            client_secret='lwk8Q~4LbZTagzrC6l0bpwrmraDrEQIalVZnfaf1')

        client = SecretClient(vault_url=KVUri, credential=credential)
        server = client.get_secret("SERVER").value
        database = client.get_secret("DATABASE").value
        username = client.get_secret("USERNAME").value
        password = client.get_secret("PASSWORD").value
        driver = '{ODBC Driver 17 for SQL Server}'
        # Some code to execute before the decorated function is called
        # payload = [server, database, username, password, driver]
        output_json = dict(zip(["server", "database", "username", "password", "driver"],
                               [server, database, username, password, driver]))
        # output_json = dict(zip(["Status", "Message", "Payload"],["200", "Success", payload]))
        request_data = req.get_json()
        request_data.update(output_json)

        result = func(request_data)
        # Some code to execute after the decorated function is called
        return result
    return wrapper_func