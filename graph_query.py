import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

        self.app_function_edges = self.data.get("app_function_edges", [])
        self.function_variable_edges = self.data.get("function_variable_edges", [])

        self.applications = self.data.get("applications", [])
        self.functions = self.data.get("functions", [])
        self.variables = self.data.get("variables", [])

        print("[DEBUG] Applications:", [self._get_name(a) for a in self.applications])
        print("[DEBUG] Functions:", [self._get_name(f) for f in self.functions])

    def _normalize(self, name: str) -> str:
        """Lowercase and replace spaces/hyphens with underscores"""
        return name.strip().lower().replace(" ", "_").replace("-", "_")

    def _get_name(self, obj):
        if isinstance(obj, dict):
            return obj.get("name", "").strip()
        elif isinstance(obj, str):
            return obj.strip()
        return ""

    # ---------------- List nodes ----------------
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
            if isinstance(edge, dict):
                edge_app = self._get_name(edge.get("app", {}))
                edge_fn = self._get_name(edge.get("function", {}))
            elif isinstance(edge, (list, tuple)):
                edge_app, edge_fn = edge[0], edge[1]
            else:
                continue
            if self._normalize(edge_app) == app_norm:
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_app('{app_name}') -> {funcs}")
        return funcs

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        apps = []
        for edge in self.app_function_edges:
            if isinstance(edge, dict):
                edge_app = self._get_name(edge.get("app", {}))
                edge_fn = self._get_name(edge.get("function", {}))
            elif isinstance(edge, (list, tuple)):
                edge_app, edge_fn = edge[0], edge[1]
            else:
                continue
            if self._normalize(edge_fn) == fn_norm:
                apps.append(edge_app)
        print(f"[DEBUG] get_apps_for_function('{fn_name}') -> {apps}")
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_norm = self._normalize(fn_name)
        vars_ = []
        for edge in self.function_variable_edges:
            if isinstance(edge, dict):
                edge_fn = self._get_name(edge.get("function", {}))
                edge_var = self._get_name(edge.get("variable", {}))
            elif isinstance(edge, (list, tuple)):
                edge_fn, edge_var = edge[0], edge[1]
            else:
                continue
            if self._normalize(edge_fn) == fn_norm:
                vars_.append(edge_var)
        print(f"[DEBUG] get_variables_for_function('{fn_name}') -> {vars_}")
        return vars_

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_norm = self._normalize(var_name)
        funcs = []
        for edge in self.function_variable_edges:
            if isinstance(edge, dict):
                edge_fn = self._get_name(edge.get("function", {}))
                edge_var = self._get_name(edge.get("variable", {}))
            elif isinstance(edge, (list, tuple)):
                edge_fn, edge_var = edge[0], edge[1]
            else:
                continue
            if self._normalize(edge_var) == var_norm:
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_variable('{var_name}') -> {funcs}")
        return funcs

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app_norm = self._normalize(app_name)
        structure = {}
        for edge in self.app_function_edges:
            if isinstance(edge, dict):
                edge_app = self._get_name(edge.get("app", {}))
                edge_fn = self._get_name(edge.get("function", {}))
            elif isinstance(edge, (list, tuple)):
                edge_app, edge_fn = edge[0], edge[1]
            else:
                continue
            if self._normalize(edge_app) == app_norm:
                structure[edge_fn] = self.get_variables_for_function(edge_fn)
        print(f"[DEBUG] get_app_structure('{app_name}') -> {structure}")
        return structure
