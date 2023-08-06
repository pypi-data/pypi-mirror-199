# Handle to the workspace
from azure.ai.ml import MLClient
# Authentication package
from azure.identity import DefaultAzureCredential
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
credential = DefaultAzureCredential()

# Get a handle to the workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="b7fbc2be-be14-4cea-9633-40351430064d",
    resource_group_name="aml-starter-rg-dev",
    workspace_name="dispred-aml",
)
cpu_compute_target = "dualnode1-cc"
# let's see if the compute target already exists
cpu_cluster = ml_client.compute.get(cpu_compute_target)
logger.warning("THIS IS A TEST WARNING LOG.")
print(
    f"You already have a cluster named {cpu_compute_target}, we'll reuse it as is."
)