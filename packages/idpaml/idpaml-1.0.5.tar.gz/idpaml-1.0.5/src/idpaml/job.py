#!/usr/bin/env python

# import the libraries
from typing import Optional, Dict
from azure.ai.ml import command
from azure.ai.ml import Input
from ._initialization import client

class AzureMLJob:
    """Job submission class for azureml command to run against data assets

    A temporary wrapper class for sending script runs, complete with mlflow logging, 
    to a specified experiment and job bucket.

    Params:
        input_data (str) : path to data in azureml datastores
        input_configuration (Dict) : config struct optionally passed by Hydra
        tags (Dict) : tag dictionary
        code_directory (str) : directory location on compute instance of codebase, e.g. {compute_instance}/code/Models/test/src/
        command (str) : command to run in directory, complete with dict specifications
        environment (str) : environment logged to azure upon which to run codebase command
        compute_cluster (str) : compute resources in azure to run jobs
        job (str) : display name of job
        experiment (str) : display name of experiment
    """

    def __init__(
        self, 
        input_data: Optional[str]= None,
        input_configuration: Optional[Dict] = None, 
        tags: Optional[Dict] = None, 
        code_directory: Optional[str] = None,
        cli_command: Optional[str] = None, 
        environment: Optional[str] = None,
        compute_cluster: Optional[str] = None,
        job: Optional[str] = None, 
        experiment: Optional[str] = None,
        **kwargs
    ):
        logger, ml_client, credential = client()
        # set ml_client and experiment name
        self._ml_client = ml_client
        self.experiment = experiment
        # point input data into configuration dict
        if 'data' in input_configuration.keys():
            input_configuration['data'] = Input(
                type="uri_file", 
                path=input_data
            )
        # clean code directory string 
        # code_directory_strip = code_directory.lstrip("/")
        codebase = code_directory
        # construct command from specification
        self.command = command(
                inputs=input_configuration,
                code=codebase,  # location of source code
                # The inputs/outputs are accessible in the command via the ${{ ... }} notation
                command=cli_command,
                # ready-made environment
                environment=environment,
                compute=compute_cluster,
                # An experiment is a container for all the iterations one does on a certain project. All the jobs submitted under the same experiment name would be listed next to each other in Azure ML studio.
                experiment_name=experiment,
                display_name=job, 
                tags=tags
            )
        
    @property 
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = value

    def run(self):
        """Create or update job run under experiment name

        Params: 
            self (AzureMLJob) : object
        """
        command_to_run = self.command
        # set job on create or update
        client_job = self._ml_client.jobs.create_or_update(command_to_run)
        return client_job


# # configure the command job
# job = command(
#     inputs=dict(
#         # uri_file refers to a specific file as a data asset
#         data=Input(
#             type="uri_file",
#             path="https://azuremlexamples.blob.core.windows.net/datasets/credit_card/default%20of%20credit%20card%20clients.csv",
#         ),
#         test_train_ratio=0.2,  # input variable in main.py
#         learning_rate=0.25,  # input variable in main.py
#         registered_model_name=registered_model_name,  # input variable in main.py
#     ),
#     code="/mnt/batch/tasks/shared/LS_root/mounts/clusters/cpaulis2-ci/code/Models/test/src/",  # location of source code
#     # The inputs/outputs are accessible in the command via the ${{ ... }} notation
#     command="python main.py --data ${{inputs.data}} --test_train_ratio ${{inputs.test_train_ratio}} --learning_rate ${{inputs.learning_rate}} --registered_model_name ${{inputs.registered_model_name}}",
#     # This is the ready-made environment you are using
#     environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest",
#     # This is the compute you created earlier
#     compute="dualnode1-cc",
#     # An experiment is a container for all the iterations one does on a certain project. All the jobs submitted under the same experiment name would be listed next to each other in Azure ML studio.
#     experiment_name="train_model_credit_default_prediction",
#     display_name="credit_default_prediction",
# )

