import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)
        self.app_function_edges = self.data.get("app_function_edges", [])
        self.function_variable_edges = self.data.get("function_variable_edges", [])

    def _normalize(self, name: str) -> str:
        return name.strip().lower().replace(" ", "_")

    def list_apps(self) -> List[str]:
        return self.data.get("applications", [])

    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_norm = self._normalize(app_name)
        return [fn for app, fn in self.app_function_edges if self._normalize(app) == app_norm]

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        return [app for app, fn in self.app_function_edges if self._normalize(fn) == fn_norm]

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        return [var for fn, var in self.function_variable_edges if self._normalize(fn) == fn_norm]

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_norm = self._normalize(var_name)
        return [fn for fn, var in self.function_variable_edges if self._normalize(var) == var_norm]

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app_norm = self._normalize(app_name)
        result = {}
        for app, fn in self.app_function_edges:
            if self._normalize(app) == app_norm:
                vars_ = self.get_variables_for_function(fn)
                result[fn] = vars_
        return result
