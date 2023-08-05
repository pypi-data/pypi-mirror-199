# Core Utilities

Numerous functions for data movement, experimental logging, and training cycles are offered through the package.

## Client and SDK Initialization

Most the contingent classes and functions enumerated by the source code call the Azure credential and identity manager by default, but if you want to manually authenticate yourself, you can simply run the following code in any AzureML environment:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
# default credential automatically searches for first valid auth option
credential = DefaultAzureCredential()
ml_client = MLClient(
    DefaultAzureCredential(), 
    subscription_id='7b690317-da0a-4e78-b75f-d33dccf720e8', 
    workspace_name='workspace-idprsv', 
    resource_group_name='idprsvml-common'
)
```

The credential is typically evaluated lazily, meaning it doesn't authenticate you into the SDK until *you attempt to use it*. For example, test your credential using the code below:

```python
from azure.core.exceptions import HttpResponseError
# if the client is configured correctly, and a compute target named cpu-4node-1 exists,
# it should return "cpu-node-1 is an available compute target."
try:
    res = ml_client.compute.get("cpu-4node-1")
    print(f"{res.name} is an available compute target.")
except HttpResponseError as error:
    print("Request failed: {}".format(error.message))
```

## Data Access

Data can be registered as a [Data Asset](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-data-assets?tabs=cli) in AzureML. This allows you to access data during remote compute jobs, such as when you may direct a distribute training job to a compute cluster as a target. If you want to access data in-memory on you local compute instance, then you can utilize the `df_from_delimited_blob` and `df_to_delimited_blob` functions available in `idpaml.data` module available through this package.
These functions convert Pandas dataframes into blobs located on storage accounts, and vice versa.

The only stipulations required are:

1. There is an [access key for the desired storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) stored as a secret on an Azure Key Vault instance, with a secret name in the format of `{storage_account}-access-key-1`.
2. Your user (or the service principal being utilized for authentication) has an [access policy](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal) to *get* keys and secrets from this Azure Key Vault instance.

Once those two things are squared away, just make sure to set an environment variable `KEY_VAULT_NAME` in your python script to the name of your Azure Key Vault, as shown below.

For example, if you wish to import a flat file from a storage blob into a Pandas dataframe, you can run the `df_to_delimited_blob` function as described below.

```python
from idpaml.data import df_from_delimited_blob, df_to_delimited_blob
from azure.identity import DefaultAzureCredential
# default credential automatically searches for first valid auth option
credential = DefaultAzureCredential()
# specify key vault name for where storage account access key can be found as a secret
os.environ["KEY_VAULT_NAME"] = "dispred-kvault-nonprod"
df_to_delimited_blob(
    df=df, 
    storage_account_url="https://amldevsastage.blob.core.windows.net/", 
    output_blob="devmladls/gold/sicklecell/sicklecell_clean.csv", 
    credential=credential
)
```

If the reverse is true and you wish to pull down data from a storage account, than you should run the `df_from_delimited_blob` function.

```python
import os

os.environ["KEY_VAULT_NAME"] = "dispred-kvault-nonprod"
df  = df_from_delimited_blob(blob_url="https://amldevsa.blob.core.windows.net/.../test.csv", credential=credential)
```
