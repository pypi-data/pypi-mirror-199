import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


class Keyvault:
    """ Class to retrieve secrets from Azure Keyvault """
    def __init__(self, keyvault_name: str = os.environ.get("KEY_VAULT_NAME")):
        """ Initialize the Keyvault class for a specific keyvault """
        kv_uri = f"https://{keyvault_name}.vault.azure.net"

        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=kv_uri, credential=credential)

    def get_secret(self, secret_name: str) -> str:
        """ Get a secret from the keyvault """
        return self.client.get_secret(secret_name).value
