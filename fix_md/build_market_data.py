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
import uuid
import quickfix as fix
from app.fix_session import Application, logfix
from app.dictionary import field_subscribe, field_symbol, field_no_related_symbol


class BuildMarketData(Application):

    def send_market_data_request(self, symbols):
        """Send Market Data Request"""

        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.BeginString(self.begin_string))
        header.setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        header.setField(fix.SenderCompID(self.api_key))
        header.setField(fix.TargetCompID(self.target_comp_id))

        message.setField(fix.MDReqID(str(uuid.uuid4())))
        message.setField(fix.SubscriptionRequestType(field_subscribe))
        message.setField(fix.NoRelatedSym(len(symbols)))

        group = fix.Group(field_no_related_symbol, field_symbol)
        for symbol in symbols:
            group.setField(fix.Symbol(symbol))
            message.addGroup(group)

        logfix.info('Sending Market Data Request: %s', message.toString())
        self.fixSession.send_message(message)
