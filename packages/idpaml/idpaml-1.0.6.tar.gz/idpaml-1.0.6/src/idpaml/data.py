#!/usr/bin/env python
import os
import io
import time
from argparse import Namespace
from typing import Union
from typing import Any
from time import sleep
import mlflow
import pandas as pd
from azureml.core import Workspace, Dataset, Datastore
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import ContainerClient, BlobClient, BlobProperties
from azure.storage.blob import BlobClient, DelimitedTextDialect


def df_from_delimited_blob(
    blob_url: str, 
    credential: Union[DefaultAzureCredential, ManagedIdentityCredential], 
    **kwargs: Any    
) -> pd.DataFrame:
    """Returns a pandas dataframe from a blob URL

    Args: 
        blob_url (str): blob url string including account and container names on url path
        credential (Union[DefaultAzureCredential, ManagedIdentityCredential]): auth credential for Azure Blob Client

    Returns: 
        df (pd.DataFrame): returned dataframe decoded from bytes

    """
    # retrieve keyvault from os environment vars
    assert "KEY_VAULT_NAME" in os.environ, KeyError("KEY_VAULT_NAME must be set in environment vars to access storage token.")
    keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    # get kv client from credential
    kv_client = SecretClient(vault_url=KVUri, credential=credential)
    storage_account = blob_url.split("/")[2].split(".")[0]
    retrieved_secret = kv_client.get_secret(f"{storage_account}-access-key-1")
    # parse blob url for storage account url, container, and blob 
    blob_url_split = blob_url.split("/")
    account_url = "/".join(blob_url_split[:3])+"/"
    container = blob_url_split[3]
    blob = "/".join(blob_url_split[4:])
    # connect to blob through client
    blob_client = BlobClient(account_url=account_url, credential=retrieved_secret.value, container_name=container, blob_name=blob)
    # specify IO format (include header)
    input_format = DelimitedTextDialect(delimiter=',', quotechar='"', lineterminator='\n', escapechar="", has_header=True)
    output_format = DelimitedTextDialect(delimiter=',', quotechar='"', lineterminator='\n', escapechar="", has_header=True)
    reader = blob_client.query_blob("SELECT * from BlobStorage", blob_format=input_format, output_format=output_format)
    # read into bytes-like object
    content = reader.readall()
    # decode dataframe from bytes
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    return df


def df_to_delimited_blob(
    df: pd.DataFrame,
    storage_account_url: str,
    output_blob: str, 
    credential: Union[DefaultAzureCredential, ManagedIdentityCredential],
    **kwargs: Any    
) :
    """uploads a pandas data frame to blob storage
    
    Args: 
        df (pd.DataFrame) : pandas dataframe to upload to blob location
        blob_url (str): blob url string including account and container names on url path
        credential (Union[DefaultAzureCredential, ManagedIdentityCredential]): auth credential for Azure Blob Client

    Returns: 
        blob_props (pd.DataFrame): returned properties of blob when created
    """
    assert "KEY_VAULT_NAME" in os.environ, KeyError("KEY_VAULT_NAME must be set in environment vars to access storage token.")
    keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    # get kv client from credential
    kv_client = SecretClient(vault_url=KVUri, credential=credential)
    storage_account = storage_account_url.split("/")[2].split(".")[0]
    retrieved_secret = kv_client.get_secret(f"{storage_account}-access-key-1")
    # link to blob client
    output_blob_split = output_blob.split("/")
    container = output_blob_split[0]
    blob = "/".join(output_blob_split[1:])
    container_client = ContainerClient(account_url=storage_account_url, credential=retrieved_secret.value, container_name=container)
    # convert pandas dataframe to string
    output = io.StringIO()
    output = df.to_csv(encoding='utf-8', index=False)
    # get metadata from kwargs
    try: 
        metadata = kwargs.get("metadata")
    except: 
        metadata = None
    if metadata:
        # try uploading blob
        try:
            container_client.upload_blob(blob, output, overwrite=True, encoding='utf-8', metadata=metadata)
        except Exception as err:
            print (f"Unexpected blob upload error {err}, {type(err)}")
    else:
        # try uploading blob
        try:
            container_client.upload_blob(blob, output, overwrite=True, encoding='utf-8')
        except Exception as err:
            print (f"Unexpected blob upload error {err}, {type(err)}")
    # get blob props
    sleep(3)
    blob_client = BlobClient(account_url=storage_account_url, credential=retrieved_secret.value, container_name=container, blob_name=blob)
    blob_props = blob_client.get_blob_properties()
    return blob_props



def import_csv(args: Namespace) -> pd.DataFrame:
    """Parse the run arguments for import settings

    This function parses a pipeline step's argument template and then returns the 
    import dataframe using either local or remote import protocols

    Args:
        args (Namespace) : argparse argument template in namespace form
    Returns:
        df (pd.DataFrame) : dataframe instance from import
    """
    if args.compute_location == "local" :
            ws = Workspace(
                args.subscription_id, 
                args.resource_group_name, 
                args.workspace_name
            )
            # connect to datastore
            datastore = Datastore.get(ws, args.input_datastore)
            # specify filepath in datastore
            dataset = Dataset.Tabular.from_delimited_files(path=(datastore, args.input_filepath))
            # stream dataset from pandas dataframe
            df = dataset.to_pandas_dataframe() 
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    else:
        # if compute location is not local, than connect to mounted dataset on remote
        input_path = os.path.join(args.input_folder, args.input_filepath)
        df = pd.read_csv(input_path)
        # block any columns with "Unnamed" in them
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def export_csv(args: Namespace, df: pd.DataFrame, encoding: str="utf-8") -> Union[BlobProperties, str]:
    """Parse the run arguments for import settings

    This function parses a pipeline step's argument template and then returns the 
    import dataframe using either local or remote import protocols

    Args:
        args (Namespace) : argparse argument template in namespace form
        df (pd.Dataframe) : csv in dataframe form 
        encoding (str) : byte encoding for data transfer
    Returns:
        blob_props (BlobProperties) : returned properties of blob for verification
    """
    # output path setting
    
    if args.compute_location == "local": 
        ws = Workspace(
                args.subscription_id, 
                args.resource_group_name, 
                args.workspace_name
            )
        # connect to datastore
        datastore = Datastore.get(ws, args.output_datastore)
        # retrieve storage account token via verification of keyvault name 
        credential = DefaultAzureCredential()
        assert "KEY_VAULT_NAME" in os.environ, \
            KeyError("KEY_VAULT_NAME must be set in environment vars to access storage token for local compute data writing.")
        key_vault_name = os.environ["KEY_VAULT_NAME"]
        kv_uri = f"https://{key_vault_name}.vault.azure.net"
        # get kv client from credential
        kv_client = SecretClient(vault_url=kv_uri, credential=credential)
        account_name = datastore.account_name
        retrieved_secret = kv_client.get_secret(f"{account_name}-access-key-1")
        # specify account details
        container_name = datastore.container_name
        blob = args.output_filepath
        storage_account_url = f"https://{account_name}.blob.core.windows.net/"
        # convert pandas dataframe to string
        output = io.StringIO()
        output = df.to_csv(encoding=encoding, index=False)
        container_client = ContainerClient(
            account_url=storage_account_url, 
            credential=retrieved_secret.value, 
            container_name=container_name
        )
        # upload blob via container client for datastore
        container_client.upload_blob(
            name=blob, 
            data=output, 
            overwrite=True, 
            encoding=encoding, 
        )
        # give buffer for upload time
        time.sleep(3)
        # retrieve blob properties for verification
        blob_client = BlobClient(
            account_url=storage_account_url, 
            credential=retrieved_secret.value, 
            container_name=container_name, 
            blob_name=blob
        )
        # retrieve blob properties
        blob_props = blob_client.get_blob_properties()
        # log contents of current file
        mlflow.log_artifact(os.path.realpath(__file__))
        return blob_props
    else:
        # upload data to output using Output class from Azure SDK v2 if compute is remote
        # return path 
        output_path = os.path.join(args.output_folder, args.output_filepath)
        df.to_csv(output_path, index=False)
        return output_path
    
    


# import os
# from time import sleep
# from typing import Union
# import io
# from time import sleep
# import pandas as pd
# from azure.ai.ml.entities import Data
# from typing import Optional, Dict, Any
# from azure.ai.ml.constants._common import AssetTypes
# from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
# from azure.storage.blob import BlobClient, DelimitedTextDialect, ContainerClient
# from ._initialization import client


# class AzureMLDataAsset(Data):
    """Data wrapper class for azureml data assets
    
    A child class of the SDKv2 AzureML data class to expedite the creation and maintenance of 
    data assets for workflow assignments and pipeline jobs.

    Params:
        name (str) : Name of the resource
        version (str) : version of the resource
        description (str) : description of the resource
        tags (Dict) : dictionary tags for the resource
        properties (Dict) : asset properties dictionary from artifact class https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-ml_1.3.0/sdk/ml/azure-ai-ml/azure/ai/ml/entities/_assets/asset.py
        path (str) : path to access resource

    # """
    # def __init__(
    #     self,
    #     *,
    #     description: Optional[str] = None,
    #     tags: Optional[Dict] = None,
    #     properties: Optional[Dict] = None,
    #     path: Optional[str] = None,
    #     type: str = AssetTypes.URI_FOLDER,
    #     **kwargs,
    # ):
    #     # replicate init function from data class from AzureML sdk documentation
    #     logger, ml_client, credential = client()
    #     self._ml_client = ml_client
    #     self._skip_validation = kwargs.pop("skip_validation", False)
    #     self._mltable_schema_url = kwargs.pop("mltable_schema_url", None)
    #     self._referenced_uris = kwargs.pop("referenced_uris", None)
    #     self.type = type
        
    #     # set name equal to file name (sans suffix) from path
    #     self.name = path.split("/")[-1].split(".")[0]
    #     super().__init__(
    #         name=self.name,
    #         path=path,
    #         description=description,
    #         tags=tags,
    #         type=type,
    #         properties=properties,
    #         **kwargs,
    #     )
    #     self.path = path
    #     try:
    #         latest_version = {d.name: d.latest_version for d in ml_client.data.list()}[self.name]
    #         self.latest_version = latest_version
    #     except KeyError as e:
    #         logger.error(e)
    #         logger.info("Data asset does not exist. Creating first version.")
    #         self.latest_version = "1"

    # def _get_all_latest_assets(self) -> Dict[str, str]:
    #     """Get all data assets registered in workspace

    #     Params:
    #         self (AzureMLDataAsset) : object
    #     """
    #     # use client to retrieve available assets and asset latest versions
    #     asset_versions = {d.name: d.latest_version for d in self._ml_client.data.list()}
    #     return asset_versions
    
    # def _get_latest_version(self) -> int:
    #     """Get latest version for specified asset

    #     Params:
    #         self (AzureMLDataAsset) : object
    #     """
    #     # use client to retrieve available assets and asset latest versions
    #     asset_version = self._get_all_latest_assets()[self.name]
    #     return asset_version

    # @property 
    # def latest_version(self):
    #     return self._latest_version
    
    # @latest_version.setter
    # def latest_version(self, value):
    #     self._latest_version = value

    # def update_to_new_version(self) -> Any:
    #     """Create resource if this currently does not exist.
        
    #     Params:
    #         self (AzureMLDataAsset) : object 
    #     """
    #     # check to see if current object exists
    #     if self.name not in self._get_all_latest_assets().keys():
    #         # create data resource if not extant
    #         self.latest_version = "1"
    #         self._ml_client.data.create_or_update(self)
    #         return self
    #     else:
    #         self._ml_client.data.create_or_update(self)
    #         sleep(3)
    #         self.latest_version = self._get_latest_version()
    #         return self