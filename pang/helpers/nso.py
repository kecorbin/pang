import requests
import os
import errno
from .files import MAKEFILE_BASE


class NSO(object):

    def __init__(self, url, username='admin', password='admin'):
        self.username = username
        self.password = password
        self.base_url = url

    @property
    def headers(self):
        headers = {
            'Content-Type': "application/vnd.yang.data+json",
            'Accept': "application/vnd.yang.collection+json,"
                      "application/vnd.yang.data+json"
            }
        return headers

    def _utf8_encode(self, obj):
        if obj is None:
            return None
        if isinstance(obj, str): # noqa
            return obj
        if type(obj) is list:
            return [self._utf8_encode(value) for value in obj]
        if type(obj) is dict:
            obj_dest = {}
            for key, value in obj.items():
                if 'EXEC' not in key and key != "operations":
                    obj_dest[self._utf8_encode(key)] = self._utf8_encode(value)
            return obj_dest
        return obj

    def get(self, uri):
        url = self.base_url + uri

        response = requests.get(url,
                                headers=self.headers,
                                auth=(self.username, self.password))
        if response.ok:
            return response
        else:
            response.raise_for_status()

    def get_device_config_xml(self, device):
        headers = {
            'Content-Type': "application/vnd.yang.data+xml",
            'Accept': "application/vnd.yang.collection+xml,"
                      "application/vnd.yang.data+xml"
            }
        url = '/api/config/devices/device/{}/config?deep'.format(device)
        url = self.base_url + url
        response = requests.get(url,
                                headers=headers,
                                auth=(self.username, self.password))
        return response.text

    def post(self, uri, data=None):
        url = self.base_url + uri

        response = requests.post(url,
                                 headers=self.headers,
                                 auth=(self.username, self.password))
        if response.ok:
            return response
        else:
            response.raise_for_status()

    def sync_from(self, device=None):
        if device:
            raise NotImplementedError
        else:
            url = "/api/config/devices/_operations/sync-from"
            resp = self.post(url)
            return resp.json()

    def get_device_config(self, device):
        """
        gets device configuration from NSO
        """
        url = '/api/config/devices/device/{}/config?deep'.format(device)
        resp = self.get(url)

        return self._utf8_encode(resp.json())

    def get_device_list(self):
        """
        returns a list of device names from NSO
        """
        url = "/api/running/devices/device"
        response = self.get(url)
        device_list = list()
        for d in response.json()["collection"]["tailf-ncs:device"]:
            device_list.append(d["name"])
        return device_list

    def get_ned_id(self, device):
        """
        returns a ned id for a given device in NSO
        """
        url = "/api/running/devices/device/{}/device-type?deep"
        url = url.format(device)
        response = self.get(url)
        try:
            # making some potentially bad assumptions here
            #
            # {
            #     "tailf-ncs:device-type": {
            #         "cli": {
            #             "ned-id": "tailf-ned-cisco-nx-id:cisco-nx",
            #             "protocol": "telnet"
            #         }
            #     }
            # }
            device_type = response.json()["tailf-ncs:device-type"]
            ned_id = device_type["cli"]["ned-id"]
            # tailf-ned-cisco-nx-id:cisco-nx
            ned_id = ned_id.split(":")[-1]  # cisco-nx
            return ned_id
        except LookupError:
            return None

    def generate_netsim_configs(self, devices):

        device_types = dict()
        # deal with generating load-dir
        for d in devices:

            xml_config = self.get_device_config_xml(d)
            filename = 'load-dir/{0}.xml'.format(d)
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, "w") as f:
                f.write(xml_config)

            # grab ned id for later
            ned_id = self.get_ned_id(d)
            if ned_id:
                device_types[d] = ned_id

        with open('Makefile', 'w') as fh:
            create_template = "\tncs-netsim create-device {} {}\n"
            add_template = "\tncs-netsim add-device {} {}\n"
            fh.write(MAKEFILE_BASE.format(base_url=self.base_url))
            fh.write("netsim:\n")

            first = True
            for device, ned in device_types.items():
                if first:
                    fh.write(create_template.format(ned, device))
                else:
                    fh.write(add_template.format(ned, device))
                first = False
