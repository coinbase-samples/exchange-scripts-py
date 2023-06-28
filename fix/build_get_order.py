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
from app.fix_session import Application

class BuildGet(Application):

    def get_order(self,fixSession):
        """Build Order Status Message (H) based-on user input"""
        order_id = os.environ.get('FIX_ORDER_ID')
        client_order_id = os.environ.get('FIX_CLIENT_ORDER_ID')
        product = os.environ.get('FIX_PRODUCT_ID')

        message = self.create_header(fixSession.portfolio_id, fix.MsgType(fix.MsgType_OrderStatusRequest))
        message.setField(fix.OrderID(order_id))
        message.setField(fix.ClOrdID(str(client_order_id)))
        message.setField(fix.Symbol(str(product)))

        fixSession.send_message(message)
