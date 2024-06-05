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
import os
import quickfix as fix
import logging
import base64
import hmac
import hashlib

from app.dictionary import *

logging.basicConfig(level=logging.INFO)
logfix = logging.getLogger(__name__)


class FixSession:
    """FIX Session"""
    def __init__(self, session_id):
        self.session_id = session_id

    def send_message(self, message):
        """Sending FIX Messages to API"""
        fix.Session.sendToTarget(message, self.session_id)

    def on_message(self, message):
        """Process Application messages here"""
        msg_type = message.getHeader().getField(fix.MsgType().getTag())
        if msg_type == field_market_data_snapshot_full_refresh:
            logfix.info('Market Data Snapshot: %s', message.toString())
        elif msg_type == field_market_data_incremental_refresh:
            logfix.info('Market Data Incremental Refresh: %s', message.toString())
        else:
            logfix.info('Received message: %s', message.toString())


class Application(fix.Application):
    """FIX Application"""

    def __init__(self):
        super().__init__()
        self.username = str(os.environ.get('FIX_USERNAME'))
        self.password = str(os.environ.get('PASSPHRASE'))
        self.api_key = str(os.environ.get('API_KEY'))
        self.api_secret = str(os.environ.get('SECRET_KEY'))
        self.begin_string = str(os.environ.get('FIX_VERSION'))
        self.target_comp_id = str(os.environ.get('TARGET_COMP_ID'))
        self.sessionId = None
        self.fixSession = None

    def onCreate(self, sessionId):
        """Function called upon FIX Application startup"""
        logfix.info('onCreate: Session (%s)' % sessionId.toString())
        self.sessionId = sessionId
        self.fixSession = FixSession(self.sessionId)

    def onLogon(self, sessionId):
        """Function called upon Logon"""
        logfix.info('Successful Logon: Session (%s)' % sessionId.toString())

    def onLogout(self, sessionId):
        """Function called upon Logout"""
        logfix.info('Logout: Session (%s)' % sessionId.toString())

    def toAdmin(self, message, sessionId):
        """Function called for all outbound Administrative Messages"""
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        if msgType.getValue() == fix.MsgType_Logon:
            message.setField(fix.StringField(fix.Username().getTag(), self.username))
            message.setField(fix.StringField(fix.Password().getTag(), self.password))
            rawData = self.sign(
                message.getHeader().getField(fix.SendingTime().getTag()),
                msgType.getValue(),
                message.getHeader().getField(fix.MsgSeqNum().getTag()),
                self.api_key,
                message.getHeader().getField(fix.TargetCompID().getTag()),
                self.password
            )
            message.setField(fix.IntField(95, len(rawData)))
            message.setField(fix.StringField(96, rawData))

    def fromAdmin(self, message, sessionId):
        """Function called for all inbound Administrative Messages"""
        msg_type = message.getHeader().getField(fix.MsgType().getTag())
        if msg_type == "A":  # Logon message type
            logfix.info('Admin Message: %s', message.toString())
        else:
            logfix.info('Other Admin Message: %s', message.toString())

    def toApp(self, message, sessionId):
        """Function called for outbound Application Messages"""
        logfix.info('App Message Sent: %s', message.toString())

    def fromApp(self, message, sessionId):
        """Function called for inbound Application Messages"""
        logfix.info('App Message Received: %s', message.toString())
        self.fixSession.on_message(message)

    def sign(self, t, msg_type, seq_num, api_key, target_comp_id, password):
        message = delimiter.join([t, msg_type, seq_num, api_key, target_comp_id, password]).encode("utf-8")
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        return base64.b64encode(signature.digest()).decode()
