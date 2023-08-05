#!/usr/bin/env python

import os
from pathlib import Path
from azure.ai.ml import MLClient
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
import logging
from typing import Tuple, Union, Dict
import yaml
from opencensus.ext.azure.log_exporter import AzureLogHandler

def client(
    logging_level: int=logging.ERROR,
    logging_disabled: bool=False,
    workspace_yaml: str=os.path.join(Path(__file__).parent, "workspace.yaml"),
    manual_yaml_file_path: str="",
    mode: str="file",
    app_insight_connection: str=None, 
    config: Dict=dict(
            subscription_id='7b690317-da0a-4e78-b75f-d33dccf720e8', 
            workspace_name='workspace-idprsv', 
            resource_group_name='idprsvml-common'
        ) 
) -> Tuple[logging.getLogger, MLClient, Union[DefaultAzureCredential, ManagedIdentityCredential]]:
    """Initiate the logger and AML client for a given workspace

    Create the logger at a desired level, connected to a pre-configured application insights and log
    analytics workspace. Connected to these resources via Instrumentation Key. Also return a workspace-enable AML
    client object.

    Args: 
        logging_level (int) : severity level for python logging according to docs at https://docs.python.org/3/library/logging.html#logging-levels
        logging_disabled (bool) : disable logging argument, default level is ERROR
        workspace_yaml (str) : path to workspace yaml location for authentication
        manual_yaml_file_path (str) : path to workspace yaml location
        mode (str) : whether or not to execute command as script or in databricks
        app_insight_connection (str) : connection string for application insights
    """

    
    # configure logging level
    logging.basicConfig(level=logging_level)
    # set logging level
    logger = logging.getLogger(__name__)
    # TODO: replace the all-zero GUID with your instrumentation key.
    if app_insight_connection is not None:
        logger.addHandler(AzureLogHandler(
            connection_string=app_insight_connection)
        )
    

    logger.info("Logger handler added.")
    # retrieve default aml network credential
    try:
        credential = DefaultAzureCredential()
    except Exception as exc:
        logger.error(exc)
        credential = ManagedIdentityCredential(client_id=os.environ.get("DEFAULT_IDENTITY_CLIENT_ID", None))
    try: 
        ml_client = MLClient.from_config(credential, **config)
    except Exception as exc:
        # print exception for attempted authorization
        logger.error(exc)
        # get client handle to the workspace if default authentication fails
        # load in workspace config
        if mode=='file':
            file_path = os.path.join(Path(__file__).parent, workspace_yaml)
        else:
            assert manual_yaml_file_path!="", ValueError("set manual_file_path argument")
            file_path = os.path.join(manual_yaml_file_path, workspace_yaml)
            
        with open(file_path, "r") as stream:
            try:
                ws_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(exc)
        # add default credential to workspace config
        ws_config['credential'] = credential
        ml_client = MLClient(**ws_config)

    # get workspace details from client
    workspace = ml_client.workspaces.get(name=ml_client.workspace_name)
    subscription_id = ml_client.connections._subscription_id
    resource_group = workspace.resource_group
    workspace_name = ml_client.workspace_name
    location = workspace.location
    
    # disable logger if requested
    if logging_disabled:
        logger = logging.getLogger(__name__)
        logger.propagate = False
    # push workspace details to logs
    logger.info(f"{subscription_id}:{resource_group}:{workspace_name}:{location}")
    return logger, ml_client, credential




    