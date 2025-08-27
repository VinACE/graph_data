import json
import re
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

    def _normalize(self, name: str) -> str:
        """Normalize names: lowercase, convert CamelCase and spaces to underscores"""
        name = name.strip()
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.replace(" ", "_").lower()

    def list_apps(self) -> List[str]:
        """Return all app names"""
        return list(self.data.keys())

    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_name_norm = self._normalize(app_name)
        for key, value in self.data.items():
            if self._normalize(key) == app_name_norm:
                return value.get("functions", [])
        return []

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_name_norm = self._normalize(fn_name)
        apps = [
            app_name
            for app_name, details in self.data.items()
            if "functions" in details and any(self._normalize(fn) == fn_name_norm for fn in details["functions"])
        ]
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_name_norm =
