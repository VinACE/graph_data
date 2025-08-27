import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, json_file: str):
        with open(json_file, "r") as f:
            self.data = json.load(f)

        # Normalize applications and functions for easier lookup
        self.apps = {}
        self.functions = {}
        for app in self.data.get("applications", []):
            app_name_norm = self._normalize(app["name"])
            self.apps[app_name_norm] = {
                "name": app["name"],
                "functions": {}
            }
            for fn in app.get("functions", []):
                fn_name_norm = self._normalize(fn["name"])
                self.apps[app_name_norm]["functions"][fn_name_norm] = fn
                self.functions[fn_name_norm] = self.functions.get(fn_name_norm, [])
                self.functions[fn_name_norm].append(app["name"])

    def _normalize(self, name: str) -> str:
        return name.strip().lower().replace(" ", "_").replace("-", "_")

    def list_apps(self) -> List[str]:
        return [app["name"] for app in self.apps.values()]

    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_name_norm = self._normalize(app_name)
        app = self.apps.get(app_name_norm)
        if not app:
            return []
        return [fn["name"] for fn in app["functions"].values()]

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_name_norm = self._normalize(fn_name)
        return self.functions.get(fn_name_norm, [])

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_name_norm = self._normalize(fn_name)
        apps = self.functions.get(fn_name_norm, [])
        variables = []
        for app_name in apps:
            app_name_norm = self._normalize(app_name)
            fn = self.apps[app_name_norm]["functions"].get(fn_name_norm)
            if fn:
                variables.extend(fn.get("variables", []))
        return variables

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app_name_norm = self._normalize(app_name)
        app = self.apps.get(app_name_norm)
        if not app:
            return {}
        structure = {}
        for fn in app["functions"].values():
            structure[fn["name"]] = fn.get("variables", [])
        return structure
