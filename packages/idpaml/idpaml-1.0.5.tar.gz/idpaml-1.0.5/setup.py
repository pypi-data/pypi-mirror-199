from setuptools import setup, find_packages
setup(
    name='idpaml',
    version='1.0.5',
    author='cpaulis2',
    description='AzureML wrapper for disease modeling.',
    long_description='This is a longer description for the project',
    url='https://github.com/uhg-internal/idp-aml',
    keywords='azureml, idp, aml',
    python_requires='>=3.6, <4',
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "azure-ai-ml",
        "scikit-learn",
        "mlflow-skinny",
        "azure-identity",
        "azure-storage-blob<=12.13.0",
        "azure-storage-file-share==12.10.1",
        "azure-common==1.1.28",
        "azure-identity~=1.12.0",
        "azure-mgmt-keyvault",
        "azure-mgmt-resource",
        "azure-mgmt-storage",
        "azure-keyvault",
        "opencensus-ext-azure",
        "PyYAML",
        "pyfiglet",
        "pandas",
        "pickle5",  # imported as pickle
        "pyyaml", 
        "azureml-core==1.48.0",
        "azureml-mlflow==1.48.0",
        "azure-keyvault-secrets==4.6.0",
        "torch~=2.0.0",
        "pytorch-lightning~=2.0.0",
        "azureml-fsspec~=0.1.0b3"
        ]
)