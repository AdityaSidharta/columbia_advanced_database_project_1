# CS6111 - Advanced Database System - Project 1

## Team Members
```
Name: Aditya Kelvianto Sidharta
UNI: aks2266
```

```
Name: Rishav Agarwal
UNI: ra3141
```

## List of Files
```
├── validity.py -> Testing validity of the parameters
├── search.py -> Performing google search on the given query
├── requirements.txt -> Containing all required package for the program
├── README.md -> Project Manual and Project Documentation
├── process.py -> Perform preprocessing on the given document, including filtering, lemmatization/stemming.
├── per_se.txt -> [TEST CASE] returning result on Per Se restaurant
├── params.py -> Parameters to be adjusted for the program
├── notebook -> Personal Jupyter Notebook for testing
│ ├── AdvancedDB_Project1.ipynb -> Rishav's Personal Notebook
│ └── [Adi] Scratch.ipynb -> Adi's Personal Notebook
├── model.py -> Performing TF-IDF Calculation and Rocchio Calculation
├── main.py -> Main Function of the program
├── LICENSE -> License of the program
├── display.py -> Functions for displaying current status to Standard Output
├── cases.txt -> [TEST CASE] returning result on COVID-19 cases
└── brin.txt -> [TEST CASE] returning result on Sergey Brin
```


## Running the Program

### Setting up the program

This program assumes that you have:

1. Python 3.6 or later installed. Installation instructions can be found at: [https://www.tecmint.com/install-python-in-ubuntu/](https://www.tecmint.com/install-python-in-ubuntu/)
2. Virtual Environment Installed. Installation instructions can be found at: [https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

Setting up and Activating Virtual Environment and Installing the Required packages
```
python -m venv cs6111_proj1
source cs6111_proj1/bin/activate
pip install -r requirements.txt
```

For the purpose of reproducibility, you need to setup an ipykernel that have the same environment that you have in your python program. In order to have the same environment in your jupyter notebook:
```
python -m ipykernel install --user --name cs6111_proj1
```

### Executing the program
The syntax for running the program is as follows:
```
python -m main <google api key> <google engine id> <precision> <query>
```

Example
```
python -m main AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 0.9 "per se"
python -m main AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 0.9 "cases"
python -m main AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 0.9 "brin"
```


## Description of the project

### Internal Design of the project


### General Structure of the code

### External Library Used

## Query Modification Method

### Selecting New Keywords

### Ordering New Keywords

## Search Engine JSON API Key and Engine ID

## Query Transcript of Test Cases
