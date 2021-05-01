import os
import time


class KnownNetwork:
    def __init__(self, ssid, other_content):
        self.ssid = ssid
        self.other_content = other_content

    def __str__(self):
        return f"{self.ssid}:{self.other_content}"


class KnownWifiManager:
    LINE_NETWORK = "network={"
    LAST_CHAR = "}"
    LINE_NETWORK_LEN = len(LINE_NETWORK)

    ssids = []

    def __init__(self):
        self.parse_networking_file()
        for ssid in self.ssids:
            print(ssid)

    def parse_networking_file(self):
        file = open("test_wpa_supplicant.conf")
        contents = file.read()
        file.close()

        self.ssids.clear()

        contents_left = contents
        index = contents_left.find(self.LINE_NETWORK)
        while index != -1:
            end = contents_left.find(self.LAST_CHAR)
            network_info = contents_left[index + 9: end]
            self.ssids.append(KnownNetwork(self.parse_ssid(network_info), self.parse_psk(network_info)))
            contents_left = contents_left[end + 1:]
            index = contents_left.find(self.LINE_NETWORK)
            time.sleep(1)


    def parse_ssid(self, network: str):
        start = network.find("ssid=\"") + 6
        finish = network[start:].find('"')
        return network[start:start + finish]

    def parse_psk(self, network: str):
        start = network.find("psk=\"") + 6
        finish = network[start:].find('"')
        return network[start:start + finish]

    def save(self):
        return
        file = open("test_wpa_supplicant.conf", "w+")

        file.write(f"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
                   f"update_config=1\n"
                   f"country=GB\n\n"
                   )
        for ssid in self.ssids:
            file.write('network={\n')
            file.write(f'    ssid="{ssid.ssid}"\n')
            file.write(f'    psk="{ssid.psk}"\n')
            file.write("}\n")

        file.close()


testing = KnownWifiManager()
