import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

        # Edge lists
        self.app_function_edges = self.data.get("app_function_edges", [])
        self.function_variable_edges = self.data.get("function_variable_edges", [])

        # Original objects
        self.applications = self.data.get("applications", [])
        self.functions = self.data.get("functions", [])
        self.variables = self.data.get("variables", [])

    def _normalize(self, name: str) -> str:
        return name.strip().lower().replace(" ", "_")

    def list_apps(self) -> List[str]:
        return [app["name"] for app in self.applications]

    def list_functions(self) -> List[str]:
        return [fn["name"] for fn in self.functions]

    def list_variables(self) -> List[str]:
        return [var["name"] for var in self.variables]

    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_norm = self._normalize(app_name)
        funcs = [
            fn for app, fn in self.app_function_edges
            if self._normalize(app) == app_norm
        ]
        return funcs

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        apps = [
            app for app, fn in self.app_function_edges
            if self._normalize(fn) == fn_norm
        ]
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        vars_ = [
            var for fn, var in self.function_variable_edges
            if self._normalize(fn) == fn_norm
        ]
        return vars_

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_norm = self._normalize(var_name)
        funcs = [
            fn for fn, var in self.function_variable_edges
            if self._normalize(var) == var_norm
        ]
        return funcs

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app_norm = self._normalize(app_name)
        structure = {}
        for app, fn in self.app_function_edges:
            if self._normalize(app) == app_norm:
                structure[fn] = self.get_variables_for_function(fn)
        return structure
