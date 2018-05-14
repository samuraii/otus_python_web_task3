# Python code analyzer

## Description 

Python code analyzer script is used to analyze the python files within the given folder, or github repo. It will count unique verbs used in function names and shows the statistics for the first 10 of them.

## Installation

In order to make this script work you'll need to do the following:

1. Clone the repo and activate virtual environment

    ```bash
    git clone https://github.com/samuraii/otus_python_web_task3
    ```

2. Activate virtual env

    Mac OS, Linux:
    
    ```bash
    source env\bin\activate
    ```
    
    Windows:
    
    ```bash
    env/Scripts/activate
    ```

3. Install nltk required packages for text analysis

    ```bash
    python nltk_install.py
    ```

## Usage

In order to use the script path a folder, or a github link to repo. If you pass the github repo you also should explain it to script with additional parametr --repo=True

#### Usage with folder:

```bash
python analyzer.py env/
```

Output:
```bash
total 1424 words, 39 unique
********************
get 603
add 157
find 94
make 88
run 69
apply 67
remove 58
tokenize 49
initialize 33
finalize 24
```

#### Usage with github repo:

```bash
python analyzer.py https://github.com/geekcomputers/Python --repo=True
```

Output:
```bash
total 17 words, 7 unique
--------------------
add 7
get 3
find 2
remove 2
readandencryptandsave 1
readanddecryptandsave 1
run 1

```

# Project goals

Educational