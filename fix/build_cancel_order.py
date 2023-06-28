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
# limitations under the License.python c
import os
import quickfix as fix
from app.fix_session import Application
from app.dictionary import *

class BuildCancel(Application):

    def cancel_order(self, fixSession):
        order_id = os.environ.get('FIX_ORDER_ID')
        client_order_id = os.environ.get('FIX_CLIENT_ORDER_ID')
        base_quantity = os.environ.get('FIX_QUANTITY')
        side = os.environ.get('FIX_SIDE')
        product = os.environ.get('FIX_PRODUCT_ID')

        message = self.create_header(fixSession.portfolio_id, fix.MsgType(fix.MsgType_OrderCancelRequest))
        message.setField(fix.OrderID(str(order_id)))
        message.setField(fix.OrigClOrdID(str(client_order_id)))
        message.setField(fix.Symbol(str(product)))
        message.setField(fix.Side(fix.Side_BUY if side == side_type_buy else fix.Side_SELL))
        message.setField(fix.OrderQty(float(base_quantity)))
        fixSession.send_message(message)
