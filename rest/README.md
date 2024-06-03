# Exchange API REST Scripts

This repository provides examples of common [REST API endpoints](https://docs.cdp.coinbase.com/exchange/reference) to use with Coinbase Exchange.
# Getting started

## 1. Gaining access

Clone the repository with the following command:
```
git clone https://github.com/coinbase-samples/exchange-scripts-py
```

## 2. Configuration

Within the REST folder, you will find a requirements.txt file, from which you will be able to install dependencies with the following command: 

```
pip install -r requirements.txt
```

Additionally, these scripts make use of environment variables where applicable. 

To fill these values, you will need to generate an API key with trading and reading functionality. Populate the below and run the following to declare these variables:

```bash

export API_KEY=ACCESSKEYHERE
export PASSPHRASE=PASSPHRASEHERE
export SECRET_KEY=SECRET_KEYHERE
```

There is also the usage of your Profile ID for several endpoints. This ID (which is API key-specific) can be retrieved from the [Get Profiles](https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getprofiles) endpoint, which is called with the included script `exchange_get_profiles.py`. Once you have retrieved your profile ID, you can add it as an environment variable with the following command:
```
export PROFILE_ID=PROFILE_IDHERE
```

## 3. Running scripts

Run directly from your command line, e.g.: 
```
python exchange_get_profiles.py
```

Several of these scripts utilize command line arguments to increase ease of use, e.g.:
```
python exchange_create_crypto_address.py BTC
```