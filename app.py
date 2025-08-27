import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

        # Edge lists (as objects)
        self.app_function_edges = self.data.get("app_function_edges", [])
        self.function_variable_edges = self.data.get("function_variable_edges", [])

        # Original objects
        self.applications = self.data.get("applications", [])
        self.functions = self.data.get("functions", [])
        self.variables = self.data.get("variables", [])

    def _normalize(self, name: str) -> str:
        """Normalize names for matching (case and space insensitive)"""
        return name.strip().lower().replace(" ", "_")

    # ---------------- List all ----------------
    def list_apps(self) -> List[str]:
        return [app["name"] for app in self.applications]

    def list_functions(self) -> List[str]:
        return [fn["name"] for fn in self.functions]

    def list_variables(self) -> List[str]:
        return [var["name"] for var in self.variables]

    # ---------------- Queries ----------------
    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_norm = self._normalize(app_name)
        return [
            edge["function"] for edge in self.app_function_edges
            if self._normalize(edge["app"]) == app_norm
        ]

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        return [
            edge["app"] for edge in self.app_function_edges
            if self._normalize(edge["function"]) == fn_norm
        ]

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        return [
            edge["variable"] for edge in self.function_variable_edges
            if self._normalize(edge["function"]) == fn_norm
        ]

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_norm = self._normalize(var_name)
        return [
            edge["function"] for edge in self.function_variable_edges
            if self._normalize(edge["variable"]) == var_norm
        ]

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        """Return a mapping of function -> variables for a given app"""
        app_norm = self._normalize(app_name)
        structure = {}
        for edge in self.app_function_edges:
            if self._normalize(edge["app"]) == app_norm:
                fn_name = edge["function"]
                structure[fn_name] = self.get_variables_for_function(fn_name)
        return structure
