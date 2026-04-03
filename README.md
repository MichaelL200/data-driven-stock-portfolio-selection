# Project Name [![Flake8 Linting](https://github.com/Dnafivuq/golem_template/actions/workflows/lint.yml/badge.svg)](https://github.com/Dnafivuq/golem_template/actions/workflows/lint.yml) [![Pytest](https://github.com/Dnafivuq/golem_template/actions/workflows/test.yml/badge.svg)](https://github.com/Dnafivuq/golem_template/actions/workflows/test.yml) <a target="_blank" href="https://cookiecutter-data-science.drivendata.org/"><img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" /></a>

### Author: Michał Ludwiczak

## Overview
This repository implements a system for stock portfolio selection and optimization. The project leverages Monte Carlo simulations, technical analysis and machine learning techniques to identify and optimize investment strategies. It was developed as part of the Individual Project course in the 4th semester.

## Features/Functionalities
Key points of what exacly users can do or achive from our repository.
 - Clean code structure
 - Preconfigured GH CI with pytest and flake8
 - This template README

## Installation & Setup
To get started with this project, follow these steps:

1. **Clone the repository**
   ```sh
   git clone https://github.com/MichaelL200/data-driven-stock-portfolio-selection
   cd data-driven-stock-portfolio-selection
   ```

2. **Set up a virtual environment**

   **Linux / macOS**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows**
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1 #activate.bat for CMD
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt  # external dependencies
   pip install -e .                 # install src/ package in editable mode
   ```

4. **Set up environment variables**
   - Copy the example `.env.example` file and rename it to `.env`.
   - Update the values as needed.

## Usage
1. **Data Preprocessing**
   Run the preprocessing script to clean and prepare the dataset:
   ```sh
   python3 -m src.dataset
   ```

2. **Train the Model**
   Run the training script to train a machine learning model:
   ```sh
   python3 -m src.modeling.train
   ```

3. **Analyze Results**
   - Check the results in the `reports/` folder.
   - Open and explore Jupyter notebooks in the `notebooks/` folder for further analysis.

## Examples
In some cases, the project may serve as a tool or library. For these types of repositories, it's helpful to provide a variety of usage examples to demonstrate how the code can be applied.

## **Additional Resources**
- Detailed information about project structure is provided in the [Project Organization](#project-organization) section.
- Further explanations about model training and evaluation are documented in the `notebooks/` folder.

## Project Organization

```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- Project's docs
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8 and pytest
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations
    └── sp500                   <- Submodule to get S&P 500 components
```
