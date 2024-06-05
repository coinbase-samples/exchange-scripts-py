# Exchange FIX README.md

This repository is a Python application for Coinbase's Exchange FIX API.
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

We also want to store and grab variables to ensure connectivity to Exchange via FIX. To fill these values completely, you will need to generate an API key with trading functionality and also retrieve your portfolio ID, which is provided in the response of [Get Profiles](https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getprofiles). Finally, your SVC_ACCOUNTID is identical to your API_KEY.  Populate the below and run the following to declare these variables:

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

## 3. Running the application

Order details are configured inside `build_create_order.py`. Adjust order details in here, then place the order via the following command:

```
export ORDER_DICT=$(python client_create_order.py) 
```

The FIX application will connect to Coinbase, place the order with the provided order details, and then send a logout message to disconnect.

This saves critical order details to an environment variable dictionary. The next command allows us to parse this dictionary and save them to individual environment variables:

```
export FIX_CLIENT_ORDER_ID=$(echo $ORDER_DICT | jq -r '."last_client_order_id"')
export FIX_ORDER_ID=$(echo $ORDER_DICT | jq -r '."last_order_id"')
export FIX_QUANTITY=$(echo $ORDER_DICT | jq -r '."last_quantity"')
export FIX_SIDE=$(echo $ORDER_DICT | jq -r '."last_side"')
export FIX_PRODUCT_ID=$(echo $ORDER_DICT | jq -r '."last_product_id"')
```

Now, these variables are ready to be used in either of the following requests:

```
python client_get_order.py
```

```
python client_cancel_order.py
```

Finally, you can modify an existing limit order by editing limit_price and quantity inside `build_modify_order.py` and running the following command:
```
python client_modify_order.py
```
