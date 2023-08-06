#!/usr/bin/env python
# import the libraries
import sys
import argparse
from azure.ai.ml import Input, Output
from azure.ai.ml.constants import AssetTypes
from omegaconf import DictConfig

def compile_args(cmd_literal_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parse command.")
    arg_templated = [arg for arg in cmd_literal_args if arg[:2]=="--"]
    for arg in arg_templated:
        parser.add_argument(arg, required=True)
    args = parser.parse_args()
    return args

def arg_prep(config: DictConfig, step: str, compute_location: str) -> tuple[dict, dict, str] | dict: 
    """Uses the config file to set argument parameters
    Defines argument step preparation from a config file. 
    Args:
        config (DictConfig) : hydra yaml config specification
        step (str) : step to process in config file
        compute_location (str) : remote step to process in file
    Returns: 
        arg_parameters (dict) : dict of parameters for remote job processing
        outputs (dict) : outputs dict for mount locations
        cmd_literal (str) : bash command literal to run remote job on
    """
    # set argument parameters from config file
    arg_parameters = {
        **config.conf['steps'][step]['parameters'], 
        **config.conf['main']['workspace']
    }
    # set command literals
    if compute_location != "local":
        cmd_literal = "python run.py"
    # if inputs exist, enter input information
    inputs = {}
    if "input" in list(config.conf['steps'][step].keys()):
        arg_parameters["input_datasets"] = ",".join(list(config.conf['steps'][step]['input'].keys()))
        for input_dataset in config.conf['steps'][step]['input'].keys():
            # pass in data structure input information
            # input_dataset_str = json.dumps(dict(config.conf['steps'][step]['input'][input_dataset]))
            # arg_parameters[input_dataset] = input_dataset_str
            # rename keys to include input dataset name for unique param values
            input_dataset_paramdict = {f"{input_dataset}_{key}":val for key, val in config.conf['steps'][step]['input'][input_dataset].items()}
            # add dataset store and filepath data to arg_parameters
            arg_parameters = {**arg_parameters,  **input_dataset_paramdict}
            # set datastore and file path for each dataset listed
            datastore = config.conf['steps'][step]['input'][input_dataset]['datastore']
            input_path = f"azureml://subscriptions/{config.conf['main']['workspace']['subscription_id']}/resourcegroups/{config.conf['main']['workspace']['resource_group_name']}/workspaces/{config.conf['main']['workspace']['workspace_name']}/datastores/{datastore}/paths/"
            # add inputs to arg_parameters 
            # add raw input information to cmd literal
            if compute_location != "local":
                inputs[f"{input_dataset}_folder"] = Input(type=AssetTypes.URI_FOLDER, path=input_path, mode="ro_mount")
                job_config_input_params = [f"--{k} ${{inputs.{k}}}" for k in input_dataset_paramdict.keys()]
                # cmd_literal = " ".join([cmd_literal, job_config_input_params])
        if compute_location != "local":
            arg_parameters = {**arg_parameters, **inputs}
            # join parameter string for command
            job_input_params = [f"--{k} ${{inputs.{k}}}" for k in inputs.keys()]
            # join input params
            # cmd_literal = " ".join([cmd_literal, job_input_params])
            
    outputs = {}
    # if outputs exists as a folder, enter output information
    if "output" in list(config.conf['steps'][step].keys()):
        arg_parameters["output_datasets"] = ",".join(list(config.conf['steps'][step]['output'].keys()))
        for output_dataset in config.conf['steps'][step]['output'].keys():
            # pass in data structure information as json dumps data
            # output_dataset_str = json.dumps(dict(config.conf['steps'][step]['output'][output_dataset]))
            # arg_parameters[output_dataset] = output_dataset_str
            # rename keys to include input dataset name for unique param values
            output_dataset_paramdict = {f"{output_dataset}_{key}":val for key, val in config.conf['steps'][step]['output'][output_dataset].items()}
            # add dataset store and filepath data to arg_parameters
            arg_parameters = {**arg_parameters, **output_dataset_paramdict}
            # set datastore and file path for each dataset listed
            datastore = config.conf['steps'][step]['output'][output_dataset]['datastore']
            output_path = f"azureml://subscriptions/{config.conf['main']['workspace']['subscription_id']}/resourcegroups/{config.conf['main']['workspace']['resource_group_name']}/workspaces/{config.conf['main']['workspace']['workspace_name']}/datastores/{datastore}/paths/"
            
            if compute_location != "local":
                outputs[f"{output_dataset}_folder"] = Output(type=AssetTypes.URI_FOLDER, path=output_path, mode="rw_mount")
                # add raw input information to cmd literal
                # NOTE: standard input parameters still have a prefix of "inputs." for the cmd literal
                # only the URI folder object input recieves a prefix of "outputs."
                job_config_output_params = [f"--{k} ${{inputs.{k}}}" for k in output_dataset_paramdict.keys()]
                # cmd_literal = " ".join([cmd_literal, job_config_output_params])
        # add outputs to arg_parameters
        if compute_location != "local":
            # add outputs to cli command
            job_output_params = [f"--{k} ${{outputs.{k}}}" for k in outputs.keys()]
            # join output parameters
            # cmd_literal = " ".join([cmd_literal, job_output_params])
    

    if compute_location != "local":
        # add all arg parameter values
        job_arg_params = [f"--{k} ${{inputs.{k}}}" for k in arg_parameters.keys()]
        # concatenate all argument parameters
        all_arg_params = job_config_input_params + job_input_params + job_config_output_params + job_output_params + job_arg_params
        # get unique values for argument params
        arg_params = list(set(all_arg_params))
        arg_params.sort()
        arg_params_literal = " ".join(arg_params)
        cmd_literal = " ".join([cmd_literal, arg_params_literal])
        # replace double brackets in command literal
        cmd_literal = cmd_literal.replace("{", "{{").replace("}", "}}")
        return arg_parameters, outputs, cmd_literal
    else: 
        return arg_parameters

# class AzureMLJob:
#     """Job submission class for azureml command to run against data assets

#     A temporary wrapper class for sending script runs, complete with mlflow logging, 
#     to a specified experiment and job bucket.

#     Params:
#         input_data (str) : path to data in azureml datastores
#         input_configuration (Dict) : config struct optionally passed by Hydra
#         tags (Dict) : tag dictionary
#         code_directory (str) : directory location on compute instance of codebase, e.g. {compute_instance}/code/Models/test/src/
#         command (str) : command to run in directory, complete with dict specifications
#         environment (str) : environment logged to azure upon which to run codebase command
#         compute_cluster (str) : compute resources in azure to run jobs
#         job (str) : display name of job
#         experiment (str) : display name of experiment
#     """

#     def __init__(
#         self, 
#         input_data: Optional[str]= None,
#         input_configuration: Optional[Dict] = None, 
#         tags: Optional[Dict] = None, 
#         code_directory: Optional[str] = None,
#         cli_command: Optional[str] = None, 
#         environment: Optional[str] = None,
#         compute_cluster: Optional[str] = None,
#         job: Optional[str] = None, 
#         experiment: Optional[str] = None,
#         **kwargs
#     ):
#         logger, ml_client, credential = client()
#         # set ml_client and experiment name
#         self._ml_client = ml_client
#         self.experiment = experiment
#         # point input data into configuration dict
#         if 'data' in input_configuration.keys():
#             input_configuration['data'] = Input(
#                 type="uri_file", 
#                 path=input_data
#             )
#         # clean code directory string 
#         # code_directory_strip = code_directory.lstrip("/")
#         codebase = code_directory
#         # construct command from specification
#         self.command = command(
#                 inputs=input_configuration,
#                 code=codebase,  # location of source code
#                 # The inputs/outputs are accessible in the command via the ${{ ... }} notation
#                 command=cli_command,
#                 # ready-made environment
#                 environment=environment,
#                 compute=compute_cluster,
#                 # An experiment is a container for all the iterations one does on a certain project. All the jobs submitted under the same experiment name would be listed next to each other in Azure ML studio.
#                 experiment_name=experiment,
#                 display_name=job, 
#                 tags=tags
#             )
        
#     @property 
#     def command(self):
#         return self._command
    
#     @command.setter
#     def command(self, value):
#         self._command = value

#     def run(self):
#         """Create or update job run under experiment name

#         Params: 
#             self (AzureMLJob) : object
#         """
#         command_to_run = self.command
#         # set job on create or update
#         client_job = self._ml_client.jobs.create_or_update(command_to_run)
#         return client_job