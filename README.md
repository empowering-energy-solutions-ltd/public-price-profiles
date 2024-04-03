price-profile
==============================

Price profile project is designed to create a profile of energy cost/emissions. This can be used in projects such as PV for optimisation of self consumption against exporting to ensure the site uses the energy it generates in the most cost effective way.

There is a `demo_notebook.ipynb` that can be found in the `notebooks` folder that gives examples of the different functions available in this project.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── example_electric_invoices.csv  <- An example .csv of electrical invoices that can be used in price profiling.
    │   └── example_gas.csv                <- An example .csv of gas invoices that can be used in price profiling
    │
    ├── notebooks          <- Jupyter notebooks. 
    │   └── demo_notebook.ipynb            <- Demo notebook of price profiling features
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │
    ├── timeseries         <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── common         <- Scripts to download or generate data
    │   │   ├── datetime_functions.py      <- Script to manipulate data using datetime functions.
    │   │   ├── enums.py                   <- Enums script for the project.
    │   │   └── measurements.py            <- Script holding measurement units for project.
    │   │
    │   ├── data           <- Scripts to turn raw data into features for modeling
    │   │   └── schema.py                  <- Schema script for the project.
    │   │
    │   ├── economic       <- Scripts to train models and then use trained models to make            
    │   │   ├── tariff_creator.py          <- Script holding `EnergyTariffImporter` class for importing price profile dict.
    │   │   ├── tariff_functions.py        <- Script for generating price profiles from both real site data and generating dummy versions.
    │   │   ├── tariff_schema.py           <- Tariff schemas script.
    │   │   └── tariff_structure.py        <- Script for concating individual charges into a single charge profile dataframe.
    │   │
    │   └── environmental  <- Scripts to create exploratory and results oriented visualizations
    │       └── carbon.py                  <- Script to retrieve carbon emissions intensity data from external api.
    │
    ├── pyproject.toml     <- Poetry .toml file for creating venv. Run poetry lock in cli to create venv
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
