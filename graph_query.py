import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

        # Edge lists (may contain strings or objects)
        self.app_function_edges = self.data.get("app_function_edges", [])
        self.function_variable_edges = self.data.get("function_variable_edges", [])

        # Original objects
        self.applications = self.data.get("applications", [])
        self.functions = self.data.get("functions", [])
        self.variables = self.data.get("variables", [])

    def _normalize(self, name: str) -> str:
        """Normalize names for matching (case and space insensitive)"""
        return name.strip().lower().replace(" ", "_")

    def _get_name(self, obj):
        """Return the 'name' if obj is dict, or obj itself if string."""
        if isinstance(obj, dict):
            return obj.get("name", "")
        elif isinstance(obj, str):
            return obj
        return ""

    # ---------------- List all ----------------
    def list_apps(self) -> List[str]:
        return [self._get_name(app) for app in self.applications]

    def list_functions(self) -> List[str]:
        return [self._get_name(fn) for fn in self.functions]

    def list_variables(self) -> List[str]:
        return [self._get_name(var) for var in self.variables]

    # ---------------- Queries ----------------
    def get_functions_for_app(self, app_name: str) -> List[str]:
        app_norm = self._normalize(app_name)
        funcs = []
        for edge in self.app_function_edges:
            edge_app_name = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn_name = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_app_name) == app_norm:
                funcs.append(edge_fn_name)
        return funcs

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        apps = []
        for edge in self.app_function_edges:
            edge_app_name = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn_name = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_fn_name) == fn_norm:
                apps.append(edge_app_name)
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        vars_ = []
        for edge in self.function_variable_edges:
            edge_fn_name = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[0])
            edge_var_name = self._get_name(edge.get("variable") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_fn_name) == fn_norm:
                vars_.append(edge_var_name)
        return vars_

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_norm = self._normalize(var_name)
        funcs = []
        for edge in self.function_variable_edges:
            edge_fn_name = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[0])
            edge_var_name = self._get_name(edge.get("variable") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_var_name) == var_norm:
                funcs.append(edge_fn_name)
        return funcs

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        """Return a mapping of function -> variables for a given app"""
        app_norm = self._normalize(app_name)
        structure = {}
        for edge in self.app_function_edges:
            edge_app_name = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn_name = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_app_name) == app_norm:
                structure[edge_fn_name] = self.get_variables_for_function(edge_fn_name)
        return structure
