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
        fn_name_norm = self._normalize(fn_name)
        vars_list = []
        for app in self.data.values():
            variables = app.get("variables", {})
            for func, vars_ in variables.items():
                if self._normalize(func) == fn_name_norm:
                    vars_list.extend(vars_)
        return vars_list

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app_name_norm = self._normalize(app_name)
        for key, value in self.data.items():
            if self._normalize(key) == app_name_norm:
                return value.get("variables", {})
        return {}

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_name_norm = self._normalize(var_name)
        funcs = []
        for app in self.data.values():
            variables = app.get("variables", {})
            for func, vars_ in variables.items():
                if var_name_norm in [self._normalize(v) for v in vars_]:
                    funcs.append(func)
        return funcs
