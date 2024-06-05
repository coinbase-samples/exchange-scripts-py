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
import configparser
import quickfix as fix
import logging
from app.logger import setup_logger, format_message
import base64
import time
import hmac
import uuid
import json
import os
import sys
import hashlib
from app.dictionary import *

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class FixSession:
    """FIX Session"""
    def __init__(self, session_id, portfolio_id):
        self.session_id = session_id
        self.portfolio_id = portfolio_id

    def send_message(self, message):
        """Sending FIX Messages to API here"""
        fix.Session.sendToTarget(message, self.session_id)

    def on_message(self, message):
        """Process Application messages here"""
        if message.getHeader().getField(field_msgtype) == msgtype_execution_report and tag_new_order in str(message):
            self.get_exec_type(message)
        elif message.getHeader().getField(field_msgtype) == msgtype_reject:
            if tag_text in str(message):
                reason = message.getField(field_text)
                logfix.info('Message Rejected, Reason: {} '.format(reason))
            else:
                reason = 'Not Returned'
                logfix.info('Message Rejected, Reason: {} '.format(reason))

    def get_exec_type(self, message):
        """Util Function to parse Execution Reports"""

        exec_type = message.getField(field_exectype)
        if tag_text in str(message):
            reason = message.getField(field_text)
        else:
            reason = 'Not Returned'
        order_id = message.getField(field_orderid)
        symbol = message.getField(field_symbol)

        def handle_new_order():
            logfix.info('New Order - Order Not Filled')

        def handle_partial_fill():
            logfix.info('Order - Partial fill')

        def handle_full_fill():
            logfix.info('Order - Filled')

        def handle_order_done(order_id):
            logfix.info('Order {} Done'.format(order_id))

        def handle_order_cancelled(order_id, reason):
            logfix.info('Order {} Cancelled, Reason: {}'.format(order_id, reason))

        def handle_order_stopped(order_id, reason):
            logfix.info('Order {} Stopped, Reason: {}'.format(order_id, reason))

        def handle_order_rejected(order_id, reason):
            logfix.info('Order {} Rejected, Reason: {}'.format(order_id, reason))

        def handle_order_restated(order_id, reason):
            logfix.info('Order {} Restated, Reason: {}'.format(order_id, reason))

        def handle_order_status(order_id, message):
            logfix.info('Order Status for {} : {}'.format(order_id, format_message(message)))

        handlers = {
            exectype_new: handle_new_order,
            exectype_partial: handle_partial_fill,
            exectype_fill: handle_full_fill,
            exectype_done: lambda: handle_order_done(order_id),
            exectype_cancelled: lambda: handle_order_cancelled(order_id, reason),
            exectype_stopped: lambda: handle_order_stopped(order_id, reason),
            exectype_rejected: lambda: handle_order_rejected(order_id, reason),
            exectype_restated: lambda: handle_order_restated(order_id, reason),
            exectype_status: lambda: handle_order_status(order_id, message),
        }

        handler = handlers.get(exec_type)
        if handler:
            handler()
        else:
            return

class Application(fix.Application):

    config = configparser.RawConfigParser()

    PASSPHRASE = str(os.environ.get('PASSPHRASE'))
    API_KEY = str(os.environ.get('API_KEY'))
    API_SECRET = str(os.environ.get('SECRET_KEY'))
    PORTFOLIO = str(os.environ.get('PORTFOLIO_ID'))

    def __init__(self):
        super().__init__()
        self.last_order_id = last_order_id
        self.last_client_order_id = last_client_order_id
        self.last_product_id = last_product_id
        self.last_side = last_side
        self.last_quantity = last_quantity
        self.firstRun = True

    def onCreate(self, sessionID):
        """Function called upon FIX Application startup"""
        logfix.info('onCreate : Session (%s)' % sessionID.toString())
        self.sessionID = sessionID
        self.fixSession = FixSession(self.sessionID, self.PORTFOLIO)
        return

    def onLogon(self, sessionID):
        """Function called upon Logon"""
        logfix.info('---------------Successful Logon----------------')
        self.sessionID = sessionID
        return

    def onLogout(self, sessionID):
        """Function called upon Logout"""
        return

    def toAdmin(self, message, sessionID):
        """Function called for all outbound Administrative Messages"""
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        if msgType.getValue() == fix.MsgType_Logon:
            username = fix.StringField(field_username, os.environ.get('FIX_USERNAME'))
            message.setField(username)
            password = fix.StringField(field_password, os.environ.get('PASSPHRASE'))
            message.setField(password)

            rawData = self.sign(message.getHeader().getField(field_sendingtime),
                                message.getHeader().getField(field_msgtype),
                                message.getHeader().getField(field_msgseqnum), self.API_KEY,
                                message.getHeader().getField(field_targetcompid),
                                self.PASSPHRASE)
            rawDataLength = fix.IntField(95, len(rawData))
            message.setField(rawDataLength)
            message.setField(fix.StringField(field_rawdata, rawData))
            message.setField(fix.StringField(field_accesskey, self.API_KEY))

            logfix.info('(Admin) S >> %s' % format_message(message))
        else:
            return

    def fromAdmin(self, message, sessionID):
        """Function called for all inbound Administrative Messages"""
        if message.getHeader().getField(field_msgtype) == msgtype_logon:
            logfix.info('(Admin) R << %s' % format_message(message))
        self.fixSession.on_message(message)
        return

    def toApp(self, message, sessionID):
        """Function called for outbound Application Messages"""
        logfix.info('(App) S >> %s' % format_message(message))
        self.last_client_order_id = message.getField(field_clordid)
        return

    def fromApp(self, message, sessionID):
        """Function called for inbound Application Messages"""
        logfix.info('(App) R << %s' % format_message(message))

        if message.isSetField(field_clordid) and message.isSetField(field_return_quantity):
            if message.getField(field_clordid) == self.last_client_order_id:
                self.last_order_id = message.getField(field_orderid)
                self.last_quantity = message.getField(field_return_quantity)
                self.last_side = message.getField(field_side)
                self.last_product_id = message.getField(field_productid)

                order_details = {
                    'last_client_order_id': self.last_client_order_id,
                    'last_order_id': self.last_order_id,
                    'last_quantity': self.last_quantity,
                    'last_side': self.last_side,
                    'last_product_id': self.last_product_id
                }

                if self.firstRun:
                    order_json = json.dumps(order_details)
                    print(order_json)
                    self.firstRun = False
        return

    def sign(self, t, msg_type, seq_num, api_key, target_comp_id, password):
        message = delimiter.join([t, msg_type, seq_num, api_key, target_comp_id, password]).encode("utf-8")
        hmac_key = base64.b64decode(self.API_SECRET)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        sign_b64 = base64.b64encode(signature.digest()).decode()
        return sign_b64

    def create_header(self, portfolio_id, message_type):
        """Construct FIX header"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(message_type)
        message.setField(fix.Account(portfolio_id))
        message.setField(fix.ClOrdID(str(uuid.uuid4())))
        return message

    def build_create_order(self, fixSession, sessionID):
        """Construct FIX Message based on User Input"""
        time.sleep(3)
        self.create_order(fixSession)
        time.sleep(6)
        self.logout(fixSession, sessionID)

    def build_get_order(self, fixSession, sessionID):
        """Construct FIX Message based on User Input"""
        time.sleep(3)
        self.get_order(fixSession)
        time.sleep(6)
        self.logout(fixSession, sessionID)

    def build_cancel_order(self, fixSession, sessionID):
        """Construct FIX Message based on User Input"""
        time.sleep(3)
        self.cancel_order(fixSession)
        time.sleep(6)
        self.logout(fixSession, sessionID)

    def build_modify_order(self, fixSession, sessionID):
        """Construct FIX Message based on User Input"""
        time.sleep(3)
        self.modify_order(fixSession)
        time.sleep(6)
        self.logout(fixSession, sessionID)

    def logout(self, fixSession, sessionID):
        logout_message = fix.Message()
        header = logout_message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_Logout))
        fixSession.send_message(logout_message)
        time.sleep(1)
        sys.exit()

    def run_create_order(self):
        """Run Create Order Application"""
        self.build_create_order(self.fixSession, self.sessionID)

    def run_get_order(self):
        """Run Get Order Application"""
        self.build_get_order(self.fixSession, self.sessionID)

    def run_cancel_order(self):
        """Run Cancel Order Application"""
        self.build_cancel_order(self.fixSession, self.sessionID)

    def run_modify_order(self):
        """Run Modify Order Application"""
        self.build_modify_order(self.fixSession, self.sessionID)
