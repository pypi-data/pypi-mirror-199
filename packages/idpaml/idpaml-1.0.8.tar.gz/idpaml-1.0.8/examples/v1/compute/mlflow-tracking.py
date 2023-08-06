from azureml.core import Workspace, Environment, Experiment, ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies

import mlflow

ws = Workspace.from_config()
mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
experiment_name = 'example-experiment'
mlflow.set_experiment(experiment_name)

# env = Environment(name="mlflow-env")
# # Specify conda dependencies with scikit-learn and temporary pointers to mlflow extensions
# cd = CondaDependencies.create(
#     conda_packages=["scikit-learn", "matplotlib"],
#     pip_packages=["azureml-mlflow", "pandas", "numpy"]
#     )


# configure script to run on compute
src = ScriptRunConfig(source_directory="src",
                      script="train.py",
                      compute_target="singlenode1-cc",
                      environment='azureml_py310_sdkv2')

exp = Experiment(workspace=ws, name=experiment_name)
run = exp.submit(src)