# **Calculator**
**A basic calculator app in Python.**

Uses shunting yard algorithm to evaluate simple mathematical expressions.

Supports:
* Addition
* Subtraction
* Multiplication
* Division
* Exponentiation
* Brackets
* Unary positive and negative

## Installation and Usage

First make sure [Python 3.8](https://www.python.org/) and [Pipenv](https://pipenv.pypa.io/en/latest/) are installed.

Clone the repository and enter the root directory:
```
git clone https://github.com/whabbot/calculator.git
cd calculator
```
Install dependencies using Pipenv:
```
pipenv install
``` 
Run the app from inside root directory:
```
pipenv run python prog/main.py
```

### To install dev dependencies and run tests
Install dev dependencies using Pipenv:
```
pipenv install --dev
```
This installs [pytest](https://docs.pytest.org) which is used for testing. Tests are located in the tests directory.

Run tests using pytest:
```
pytest
```