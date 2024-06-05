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
last_order_id = ''
last_client_order_id = ''
last_product_id = ''
last_side = ''
last_quantity = ''

field_msgtype = 35
msgtype_execution_report = '8'
msgtype_reject = '3'
msgtype_logon = 'A'

field_exectranstype = 20
exectranstype_new = '0'

field_sendingtime = 52
field_msgseqnum = 34
field_targetcompid = 56
field_symbol = 55
field_text = 58

field_exectype = 150
exectype_new = '0'
exectype_partial = '1'
exectype_fill = '2'
exectype_done = '3'
exectype_cancelled = '4'
exectype_stopped = '7'
exectype_rejected = '8'
exectype_restated = 'D'
exectype_status = 'I'

field_clordid = 11
field_orderid = 37
field_quantity = 151
field_return_quantity = 38
field_side = 54
field_productid = 55

field_username = 553
field_password = 554
field_rawdata = 96
field_accesskey = 9407

side_type_buy = 'BUY'
side_type_sell = 'SELL'

side_buy = '1'
side_sell = '2'

type_market = 'MARKET'
type_limit = 'LIMIT'
type_twap = 'TWAP'

tag_new_order = '20=0'
tag_text = '58='

delimiter = '\x01'

field_cancelordersondisconnect = 8013
field_dropcopyflag = 9406
