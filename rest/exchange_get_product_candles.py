# Copyright 2023-present Coinbase Global, Inc.
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

import json, requests, sys

if len(sys.argv) != 2:
    exit('Usage: python exchange_get_product_candles.py <product_id>')

product_id = sys.argv[1]
granularity = 86400

url = f'https://api.exchange.coinbase.com/products/{product_id}/candles?granularity={granularity}'

method = 'GET'

headers = {
   'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print(response.status_code)
parse = json.loads(response.text)
print(json.dumps(parse, indent=3))

