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

```
python -m venv cs6111_proj1
source cs6111_proj1/bin/activate
pip install -r cs6111_proj1/requirements.txt
python -m main [google api key] [google engine id] [precision] "[query]"
```

## Internal Design of the project

### General Structure of the code
As explained in the list of files above, we separate the functions that are required to run the whole program into different python script based on its functionality. `main.py` is used to assemble the different pieces together and act as the main program. 

The reason of this code structure is modularity - we are able to change, update, or upgrade any of the modules in the program without changing other parts. For example, the `improve` function can be easily adapted to use different algorithm to generate the new proposed query, given that the current input signature is adequate for the new algorithm. Likewise, any changes in the `TF` component and `IDF` component in the function can be done seamlessly

`params.py` is also used to hold all the possible parameters for the project. Currently, we allow changes on the parameters of the **Rocchio algorithm**, as well as on the preprocessing method

Current Default values for `params.py`
```Python3
ALPHA = 1.0 # any positive float value
BETA = 0.9 # any positive float value
GAMMA = 0.05 # any positive float value, should be significantly smaller than ALPHA and BETA
STEMMER = "lemmatize" # ['none', 'porter', 'snowball', 'arlstem', 'arlstem2', 'lemmatize']
TOKENIZER = "word" # ['word', 'wordpunct', 'stanford', 'treebank']
LANGUAGE = "english"
TOP_K = 2
```

### External Library Used
In order for us to freeze the environment, all the packages that we use have been included in the [requirements.txt](requirements.txt). 

The main packages that we use in this project are:

- Numpy: Performing vectorized array calculations
- fire: Command Line Interface Framework
- nltk: Provide Stopwords, Stemming, and Lemmatization API
- googleapiclient: Search Engine API


## Query Modification Method

### Preprocessing and Document Generation
Currently, we use the `title` and `snippet` that is generated from the Google Search Engine API to act as the `document` 
for each of the search result. While we are able to scrape the HTML file through the `link` and get the text content, 
we found that the snippet from Google Search API has already contained the important keyword for query proposals.

In order to standardize and improve the query suggestion, we perform stop-words removal in order to prevent us from adding our
query with unimportant stopwords, and we also perform lemmatization to standardize our vocabulary. We found that stemming 
is not appropriate for our use case as it truncate our word, which might change the meaning once we provide it as our query

Nevertheless, we do realize that lemmatization might face the same problem as stemming, albeit less severe. It is a tradeoff 
between combining relevant words into single term versus the specificity of the words that we want to query

### Selecting New Keywords
We use TFIDF in order to create the word vector that is required for the Rocchio algortihm. In order to improve the vector query,
the Term Frequency is adjusted to its document length and we use logarithm scale for the inverse document frequency. 

Then, we use Rocchio Algorithm[1] to update the query vector that we have. The query vector is initialized with 1 for each term that is contained in the query and 0 otherwise. 
Using the Relevant Vectors and Nonrelevant Vectors that we generate through the user feedback and TF-IDF algorithm, we are able to update the current query vector that we have

In order to select keywords, we select the top 2 keywords in our query vector with the biggest score, apart from all the words that has been already contained in our current query. 

Literature:

[1]Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze: An Introduction to Information Retrieval, page 163-167. Cambridge University Press, 2009.

### Ordering New Keywords
Mimicking the current algorithm that is contained in the reference solution, we are keeping the order of the current query, and appending the new keywords generated through the rocchio algorithm at the back of the query. However, the order of the two words that has been generated depends on the query vector value, where the one with higher score will be placed in front

## Search Engine JSON API Key and Engine ID

```
API Key: AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA
Engine ID: ad8d80c3f1b726f69
```

## Query Transcript of Test Cases

- [Per Se](per_se.txt)
- [Brin](brin.txt)
- [Cases](cases.txt)