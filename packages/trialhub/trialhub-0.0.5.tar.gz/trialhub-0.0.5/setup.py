from setuptools import setup, find_packages

setup(
    name='trialhub',
    version='0.0.5',
    description='Helper modules for TrialHub project',
    author='FindMeCure team',
    author_email='ivo@findmecure.com',
    url='https://github.com/IvayloYosifov/trialhub-helpers',
    packages=['.'],
    py_modules=['vector_db', 'helper', 'azure_storage', 'pubmed_entrez', 'pubmed_download', 'open_ai'],
    package_data={'.':['config.json']},
    install_requires=[
        'openai',
        'biopython',
        'pinecone-client',
        'azure-storage-blob',
        'cryptography',
        'azure-identity',
        'azure-keyvault-secrets'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)