import itertools

# A helper function to break an iterable into chunks of size batch_size.
def chunks(iterable, batch_size=100):        
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(secret_name):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url="https://trialhub-helpers.vault.azure.net/", credential=credential)
    secret = secret_client.get_secret(secret_name)
    return secret.value