import struct
import warnings

from datetime import datetime, timedelta

from ..event_count import EventCount
from ..subject import UplinkSubject, DownlinkSubject, UplinkMessage, FailedAPICallException
from ..util import format_time

# TODO: Format Documentation.
# TODO: Supply properties for all avalible values.
# TODO: Unittest functionality.
# TODO: See what additional functionality can be added.
# TODO: Don't require net token.


def flatten_status(results):
    """Flattens the status message's 'properties' dictionary."""
    for status in results:
        status["value"]["properties"] = {d["name"]: d["value"] for d in status["value"]["properties"]}
    return results


def compare_min_version(version_string, major, minor, tag):
    version = [int(v) for v in version_string.split(".")]
    if version[0] < major:
        return False
    elif version[0] == major:
        if version[1] < minor:
            return False
        elif version[1] == minor and version[2] < tag:
            return False
    return True


class GatewayUplinkMessage(UplinkMessage):
    """Represents an uplink message from a gateway."""

    pass


class Gateway(UplinkSubject, DownlinkSubject, EventCount):
    """Represents a single Symphony gateway."""

    subject_name = "node"  # TODO: gateway????
    msgObj = GatewayUplinkMessage

    def get_status(self):
        """Returns the most recent gateway status dictionary"""
        url = "{}/data/gatewayStatus/node/{}/mostRecentEvents".format(self.client_edge_url, self.subject_id)
        params = {"maxResults": 1}
        return flatten_status(self._get(url, params=params)["results"])

    def get_config(self, query_interval_m=60):
        # Perform a query and filter to get the most recent config message
        _now = datetime.utcnow()
        _stati = self.get_statuses(_now - timedelta(minutes=query_interval_m), _now)
        _filtered = [_s for _s in _stati if _s["metadata"]["props"]["type"] == "config"]
        if len(_filtered) == 0:
            raise FailedAPICallException(
                "No config messages sent in the provided interval ({} mins), retry with a longer interval".format(
                    query_interval_m
                )
            )
        return _filtered[0]

    def get_last_gw_uplink(self, num=1):
        warnings.warn("This method has been deprecated")

    def get_cell_status(self):
        # Retrieve the most recent status and filter by cell signal data
        _status = self.get_status()
        if len(_status) == 0:
            raise FailedAPICallException("Could not retrieve gateway status")
        signal_data = {k: v for k, v in _status[0]["value"]["properties"].items() if "network_signal" in k}
        return signal_data

    def get_statuses(self, start_time, stop_time):
        """Returns the status messages for a particular time range."""
        url = "{}/data/gatewayStatus/node/{}/events/{}/{}".format(
            self.client_edge_url, self.subject_id, format_time(stop_time), format_time(start_time)
        )
        return flatten_status(self._get(url)["results"])

    def send_message(self, payload, port=0, priority=10):
        """Sends a message, targetted to the Customer Feedback ZeroMQ Socket
        internal to the Gateway.

        Args:
            payload(bytes): Data to send.
            port(int): The port number of the message.
            priority(int): The priority of the message.

        Returns:
            :class`.DownlinkMessage`
        """
        body = {"commandRoutes": {"linkAddresses": [self.subject_id + "!FFE!" + self.subject_id]}}
        return self._send_message_with_body(body, payload, False, 60, port, priority)

    def send_broadcast(self, payload, time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a broadcast message to all nodes listening to this gateway.

        Returns a `DownlinkMessage` object.
        """
        broadcast_mod_address = "$301$0-0-0-FFFFFFFFF"
        body = {"commandRoutes": {"linkAddresses": [broadcast_mod_address + "!101!" + self.subject_id]}}
        return self._send_message_with_body(body, payload, False, time_to_live_s, port, priority)

    def get_last_data(self, n=1):
        """Gets the last uplinked data from a gateway.

        Args:
            n: Number of events.

        Returns:
            (json): list of json events from the gateway.
        """
        url = "{}/data/uplinkPayload/node/{}/mostRecentEvents".format(self.client_edge_url, self.subject_id)
        params = {"maxResults": n}
        return self._get(url, params=params)

    def restart_gateway(self, ttl_s=120.0):
        """Sends a reset command to a gateway."""
        payload = struct.pack(">BQ", 0x7F, int(datetime.now().timestamp() * 1000))
        body = {"commandRoutes": {"linkAddresses": ["{}!FFD!{}".format(self.subject_id, self.subject_id)]}}
        return self._send_message_with_body(body, payload, True, ttl_s, 0, 10)

    def set_downlink_channel(self, auto_mode: bool, channel: int = None, ttl_s: float = 120.0):
        """
        Sets the gateway downlink channel.
        Args:
            auto_mode(bool): True to set downlink channel auto.
            channel(int): A channel number when downlink is manual.
            ttl_s(float): Time to live in seconds.

        Returns:
            :class`.DownlinkMessage`
        """
        # Check version
        _version = self._data.get("gatewayConfig").get("gateway_release_version")
        if _version is None:
            warnings.warn(
                "Cannot retrieve gateway release version, this function will not work if the gateway release < 2.1.1"
            )
        elif not compare_min_version(_version, 2, 1, 1):
            warnings.warn("Gateway version too old, this function will not work")

        if auto_mode is False:
            if channel is None:
                raise ValueError("When auto_mode is manual (False), a channel number must be provided")
            elif channel < 0 or channel > 47:
                raise ValueError("Channel value must fall within the range 0-47")
        else:
            channel = 0
        payload = struct.pack(">B?B", 0x04, auto_mode, channel)
        body = {"commandRoutes": {"linkAddresses": ["{}!FFD!{}".format(self.subject_id, self.subject_id)]}}
        return self._send_message_with_body(body, payload, True, ttl_s, 0, 10)
