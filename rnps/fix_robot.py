########################################################################
# robot-nps, Network Protocol Simulator for Robot Framework
#
# Copyright (C) 2015 David Arnold
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

from base import *
from fix import FixParser

# Module-local logger.
logger = logging.getLogger(__name__)


########################################################################

class FixServerSession(BaseServerSession):
    def __init__(self, factory, address):
        BaseServerSession.__init__(self, factory, address)
        self.set_protocol("FIX")
        self.parser = FixParser()
        return

    def dataReceived(self, data):
        """Handle a received packet.

        Override of Twisted method from base class."""

        self.parser.append_buffer(data)

        msg = self.parser.get_message()
        while msg:
            if msg.message_type == '0' and self.factory.auto_receive_heartbeats:
                logger.info("FIX: Session [%s]: consumed heartbeat",
                            self.factory.name)
                return

            self.received_messages.append(msg)
            logger.info("%s: server queuing 35=%s",
                        self.factory.name,
                        msg.message_type)

            msg = self.parser.get_message()

        return


class FixServerFactory(BaseServerFactory):
    def __init__(self, robot, name, port, version):
        BaseServerFactory.__init__(self, robot, name, port, version)
        self.set_protocol("FIX", FixServerSession)
        return


class FixClient(BaseClient):
    def __init__(self, factory, address):
        self.set_protocol("FIX")
        BaseClient.__init__(self, factory, address)
        self.parser = FixParser()
        return

    def dataReceived(self, data):
        """Handle a received packet.

        Override of Twisted method from base class."""

        self.parser.append_buffer(data)
        msg = self.parser.get_message()
        while msg:

            if msg.message_type == '0' and self.factory.auto_receive_heartbeats:
                logger.info("FIX: Session [%s]: consumed heartbeat",
                            self.factory.name)
                return

            self.received_messages.append(msg)
            logger.info("%s: client queuing 35=%s",
                        self.factory.name,
                        msg.message_type)

        return


class FixClientFactory(BaseClientFactory):
    def __init__(self, robot, name,
                 server_host, server_port,
                 protocol_version, client_port):
        BaseClientFactory.__init__(self, robot, name,
                                   server_host, server_port,
                                   protocol_version, client_port)
        self.set_protocol("FIX", FixClient)
        return


class FixRobot(BaseRobot):
    def __init__(self):
        self.protocol_name = "FIX"
        BaseRobot.__init__(self)
        return

    def create_client(self, client_name,
                      server_host, server_port,
                      protocol_version, client_port="0"):
        """Create a FIX client session."""

        if client_name in self.clients:
            raise errors.DuplicateClientError(client_name)

        client = FixClientFactory(self, client_name,
                                  server_host, server_port,
                                  protocol_version, client_port)
        self.clients[client_name] = client
        logger.info("Created FIX client: %s %s -> %s:%s v%s",
                    client_name, client_port, server_host,
                    server_port, protocol_version)
        return

    def create_server(self, server_name, port, version):
        """Create a FIX server."""

        if server_name in self.servers:
            raise errors.DuplicateServerError(server_name)

        server = FixServerFactory(self, server_name, port, version)
        self.servers[server_name] = server
        logger.info("Created FIX server: %s @ port %s v%s",
                    server_name, port, version)
        return

    def create_message(self, name):
        if name in self.messages:
            raise errors.DuplicateMessageError(name)

        constructor = soupbin.Messages.get(soup_type)
        if not constructor:
            raise errors.BadMessageTypeError(soup_type)

        self.messages[name] = constructor()
        return

    def destroy_message(self, name):
        if name not in self.messages:
            raise errors.NoSuchMessageError(name)

        del self.messages[name]
        return

    def set_integer_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_float_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_boolean_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_string_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_timestamp_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_time_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return

    def set_date_field(self, message_name, tag, value):
        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        return
    
    def get_field(self, message_name, tag):
        """Get field value from this message."""

        msg = self.messages.get(message_name)
        if not msg:
            raise errors.NoSuchMessageError(message_name)

        if not msg.has_payload():
            raise errors.NotAnOuchMessageError(message_name)

        return msg.get_payload().get_field(field_name)


########################################################################
