from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()


long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name='analytic_workspace_client',
    version='1.1.0',

    description='Библиотека для подключения к Analytic Workspace',
    long_description=long_description,
    long_description_content_type="text/markdown",


    author='Analytic Workspace',
    author_email='aw_help@analyticworkspace.ru',
    url='https://analyticworkspace.ru/',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],

    python_requires='>=3.8,<4',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    install_requires=[
        'python-dotenv>=0.21,<1.0',
        'httpx>=0.23,<1.0',
        'pandas>=1.5,<2.0',
        'pydantic>=1.10,<2.0',
        'colorama>=0.4,<0.5'
    ],

    extras_require={
        'dev': 'pyspark==3.3.1',
    },
    
    setup_requires=['wheel'],  
)
