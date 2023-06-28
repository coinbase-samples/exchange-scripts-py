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
import os
import quickfix as fix
import time
from app.fix_session import Application
from app.dictionary import side_buy, side_sell

class BuildModify(Application):

    def modify_order(self,fixSession):
        """Build Order Status Message (H) based-on user input"""
        product = os.environ.get('FIX_PRODUCT_ID')
        order_id = os.environ.get('FIX_ORDER_ID')
        client_order_id = os.environ.get('FIX_CLIENT_ORDER_ID')
        side = os.environ.get('FIX_SIDE')

        base_quantity = '0.00011'  # updated order quantity
        limit_price = '55000'  # updated limit price

        message = self.create_header(fixSession.portfolio_id, fix.MsgType(fix.MsgType_OrderCancelReplaceRequest))
        message.setField(fix.Symbol(str(product)))
        message.setField(fix.OrdType(fix.OrdType_LIMIT))
        message.setField(fix.OrderID(order_id))
        message.setField(fix.OrigClOrdID(str(client_order_id)))
        message.setField(fix.OrderQty(float(base_quantity)))
        message.setField(fix.Price(float(limit_price)))
        message.setField(fix.Side(fix.Side_BUY if side == side_buy else fix.Side_SELL))

        print(side)
        trstime = fix.TransactTime()
        trstime.setString(str(time.time()))
        message.setField(trstime)
        fixSession.send_message(message)
