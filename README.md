# Exchange API Scripts

This repository provides Python examples of the Coinbase Exchange Public APIs.
# Getting started

## 1. Gaining access

Clone the repository with the following command:
```
git clone https://github.com/coinbase-samples/exchange-scripts-py
```

## 2. Configuration

Depending on if you are accessing REST or FIX, dependencies will differ. Within each folder, you will find a requirements.txt file, from which you will be able to install dependencies with the following command: 

```
pip install -r requirements.txt
```

Additionally, these scripts make use of environment variables where applicable. Please note that only the first three values noted below are needed for REST APIs. The remainder are requirements for FIX. 

To fill these values, you will need to generate an API key with trading and reading functionality and also retrieve your portfolio ID, which is provided in the response of [Get Products](https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getprofiles). Finally, your SVC_ACCOUNTID is identical to your API_KEY. Populate the below and run the following to declare these variables:

```bash

export API_KEY=API_KEY_HERE
export PASSPHRASE=PASSPHRASE_HERE
export SECRET_KEY=SECRET_KEY_HERE
export PORTFOLIO_ID=PORTFOLIO_ID_HERE
export SVC_ACCOUNTID=SVC_ACCOUNT_ID_HERE
export FIX_VERSION=FIXT.1.1
export DEFAULT_APPL_VER_ID=9
export TARGET_COMP_ID=Coinbase
```

## 3. Running scripts

For REST, scripts are entirely standalone and do not require any main application to access. You can run them simply by running a command like the following:
```
python script_name_here.py
```