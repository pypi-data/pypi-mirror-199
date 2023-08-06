from setuptools import setup, find_packages

setup(
    name='trialhub',
    version='0.0.3',
    description='Helper modules for TrialHub project',
    author='FindMeCure team',
    author_email='ivo@findmecure.com',
    url='https://github.com/IvayloYosifov/trialhub-helpers',
    packages=find_packages(),
    install_requires=[
        'openai',
        'biopython',
        'pinecone-client',
        'azure-storage-blob',
        'cryptography',
        'azure-identity',
        'azure-keyvault-secrets'
    ],
)