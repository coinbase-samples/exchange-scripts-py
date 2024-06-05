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
import time
import quickfix as fix
from app.configuration import Configuration
import configparser
from app.fix_session import logfix
from build_market_data import BuildMarketData

config = configparser.ConfigParser()


def main():
    """Main"""
    try:
        Configuration().build_config()
        settings = fix.SessionSettings('example.cfg')

        build = BuildMarketData()

        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SSLSocketInitiator(build, storeFactory, settings, logFactory)

        initiator.start()

        time.sleep(2)
        build.send_market_data_request(['BTC-USD'])

        while True:
            time.sleep(1)

    except (fix.ConfigError, fix.RuntimeError) as exception:
        logfix.error('Exception: %s', exception)


if __name__ == '__main__':
    main()
