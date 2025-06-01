import requests

class MinecraftServerStatusAPI():
    def __init__(self, edition, address):
        self.edition = edition
        self.address = address
        self._data = None
        self.last_error = None

    def _fetch_status(self):
        try:
            response = requests.get(f"https://api.mcstatus.io/v2/status/{self.edition}/{self.address}")
            response.raise_for_status()
            self._data = response.json()
            self.last_error = None
            return True
        except requests.exceptions.RequestException as e:
            self.last_error = str(e)
            self._data = None
            return False

    def _ensure_data(self):
        if self._data is None:
            self._fetch_status()

    @property
    def is_online(self):
        self._ensure_data()
        return self._data.get("online") if self._data else False
    
    @property
    def host(self):
        self._ensure_data()
        return self._data.get("host") if self._data else False
    
    @property
    def port(self):
        self._ensure_data()
        return self._data.get("port") if self._data else 0
    
    @property
    def ip(self):
        self._ensure_data()
        return self._data.get("ip_address") if self._data else 'Unknown'
    
    @property
    def version(self):
        self._ensure_data()
        return self._data.get("version", {}).get("name_clean" if self.edition=="java" else "name") if self._data else 'Unknown'
    
    @property
    def online(self):
        self._ensure_data()
        return self._data.get("players", {}).get("online") if self._data else 0
    
    @property
    def max_online(self):
        self._ensure_data()
        return self._data.get("players", {}).get("max") if self._data else 0
    
    @property
    def motd_clean(self):
        self._ensure_data()
        return self._data.get("motd", {}).get("clean") if self._data else 'Unknown'
    
    @property
    def icon(self):
        self._ensure_data()
        return f"https://api.mcstatus.io/v2/icon/{self.address}"