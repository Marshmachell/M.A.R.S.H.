import requests
import json
from base64 import b64decode

class MojangAPI:
    def __init__(self, username):
        self.username = username
        self._status_data = None
        self._profile_data = None
        self.last_error = None

    def _fetch_status(self):
        try:
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.username}")
            response.raise_for_status()
            self._status_data = response.json()
            self.last_error = None
            return True
        except requests.exceptions.RequestException as e:
            self.last_error = str(e)
            self._status_data = None
            return False
        
    def _fetch_profile(self):
        if not self.uuid:
            self.last_error = "UUID not found"
            return False
            
        try:
            response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{self.uuid}")
            response.raise_for_status()
            self._profile_data = response.json()
            self.last_error = None
            return True
        except requests.exceptions.RequestException as e:
            self.last_error = str(e)
            self._profile_data = None
            return False
        
    def _ensure_status_data(self):
        if self._status_data is None:
            self._fetch_status()

    def _ensure_profile_data(self):
        if self._profile_data is None and self.uuid:
            self._fetch_profile()

    @property
    def uuid(self):
        self._ensure_status_data()
        return self._status_data.get("id") if self._status_data else None
    
    @property
    def profile(self):
        self._ensure_profile_data()
        return ProfileData(self._profile_data) if self._profile_data else None

class ProfileData:
    def __init__(self, profile_data):
        self._data = profile_data or {}
    
    @property
    def textures(self):
        for prop in self._data.get("properties", []):
            if prop.get("name") == "textures":
                try:
                    decoded = b64decode(prop["value"])
                    return json.loads(decoded)
                except (ValueError, KeyError, TypeError):
                    return None
        return None
    
    @property
    def skin_url(self):
        textures = self.textures
        return textures.get("textures", {}).get("SKIN", {}).get("url") if textures else None
    
    @property
    def cape_url(self):
        textures = self.textures
        return textures.get("textures", {}).get("CAPE", {}).get("url") if textures else None
    
    @property
    def name(self):
        return self._data.get("name") if self._data else None