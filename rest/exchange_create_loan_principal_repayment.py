# Copyright 2024-present Coinbase Global, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, hmac, hashlib, time, requests, base64, os, sys
import uuid
from urllib.parse import urlparse

API_KEY = str(os.environ.get('API_KEY'))
PASSPHRASE = str(os.environ.get('PASSPHRASE'))
SECRET_KEY = str(os.environ.get('SECRET_KEY'))

if len(sys.argv) != 5:
    exit('Usage: python exchange_create_loan_principal_repayment.py'
         ' <loan_id> <from_profile_id> <currency> <native_amount>')

loan_id = sys.argv[1]
from_profile_id = sys.argv[2]
currency = sys.argv[3]
native_amount = sys.argv[4]

url = 'https://api.exchange.coinbase.com/loans/repay-principal'

timestamp = str(int(time.time()))
idem = str(uuid.uuid4())
method = 'POST'

url_path = urlparse(url).path

payload = {
   'loan_id': loan_id,
   'idem': idem,
   'from_profile_id': from_profile_id,
   'currency': currency,
   'native_amount': native_amount
}

message = timestamp + method + url_path + json.dumps(payload)
hmac_key = base64.b64decode(SECRET_KEY)
signature = hmac.digest(hmac_key, message.encode('utf-8'), hashlib.sha256)
signature_b64 = base64.b64encode(signature)

headers = {
   'CB-ACCESS-SIGN': signature_b64,
   'CB-ACCESS-TIMESTAMP': timestamp,
   'CB-ACCESS-KEY': API_KEY,
   'CB-ACCESS-PASSPHRASE': PASSPHRASE,
   'Accept': 'application/json',
   'content-type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
parse = json.loads(response.text)
print(json.dumps(parse, indent=3))

