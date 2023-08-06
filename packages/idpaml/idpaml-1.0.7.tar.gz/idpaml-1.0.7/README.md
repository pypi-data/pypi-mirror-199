# Infectious Disease Platform - AzureML Interface SDK

> *AzureML SDK simplification interface for disease forecasting/vulnerability.*

- Includes multiple functions related to ML engineering and operations
  - Credential managment
  - Data input/output
  - Experiment configuration and submission
  - Model registration

## Installation

Pypi should have the most up-to-date version of the package, so you should be able to pull directly from the public registry.

```bash
pip install idpaml==1.0.x
```

Alternatively, you can include the package in a conda environment configuration file. Just make sure to include the default conda channels in your file, as listed below:

```yaml
name: example_pipeline_env
channels:
  - anaconda
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - mlflow=2.1.1
  - ipython=8.9.0
  - jupyterlab=3.5.3
  - matplotlib=3.6.3
  - pandas=1.5.3
  - pip=22.3.1
  - pip:
    - scikit-learn==1.2.1
    - hydra-core==1.3.1
    - mlflow-skinny==2.1.1
    - azure-storage-blob<=12.13.0
    - azure-keyvault-secrets==4.6.0
    - idpaml==1.0.2
```
