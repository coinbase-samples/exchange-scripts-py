# Exchange FIX README.md

This repository is a Python application for Coinbase's Exchange FIX API to stream market data.
# Getting started

## 1. Gaining access

Clone the repository with the following command:
```
git clone https://github.com/coinbase-samples/exchange-scripts-py
```

## 2. Configuration

You will need to install two dependencies for this to operate: quickfix and certifi. This allows for Python to successfully connect to Coinbase via FIX. This can be done with the following command:

```
pip install -r requirements.txt
```

We also want to store and grab variables to ensure connectivity to Exchange via FIX. Please note that your SVC_ACCOUNTID is identical to your API_KEY.  Populate the below and run the following to declare these variables:

```bash

export API_KEY=API_KEY_HERE
export PASSPHRASE=PASSPHRASE_HERE
export SECRET_KEY=SECRET_KEY_HERE
export SVC_ACCOUNTID=SVC_ACCOUNT_ID_HERE
export FIX_VERSION=FIXT.1.1
export DEFAULT_APPL_VER_ID=9
export TARGET_COMP_ID=Coinbase
```

## 3. Running the application

To open a connection to Coinbase Exchange to stream market data via FIX 5.0, run the following command:

```
python client_market_data.py 
```

