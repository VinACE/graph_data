import json
from typing import List, Dict
from difflib import get_close_matches

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
        """Normalize names: strip, lowercase, replace spaces and hyphens with underscores"""
        return name.strip().lower().replace(" ", "_").replace("-", "_")

    def _get_name(self, obj):
        if isinstance(obj, dict):
            return obj.get("name", "").strip()
        elif isinstance(obj, str):
            return obj.strip()
        return ""

    def _fuzzy_match(self, name: str, candidates: List[str]) -> str:
        """Return closest match from candidates or the original name"""
        match = get_close_matches(name, candidates, n=1, cutoff=0.6)
        return match[0] if match else name

    # ---------------- List ----------------
    def list_apps(self) -> List[str]:
        return [self._get_name(app) for app in self.applications]

    def list_functions(self) -> List[str]:
        return [self._get_name(fn) for fn in self.functions]

    def list_variables(self) -> List[str]:
        return [self._get_name(var) for var in self.variables]

    # ---------------- Queries ----------------
    def get_functions_for_app(self, app_name: str) -> List[str]:
        apps = [self._get_name(a) for a in self.applications]
        app_name = self._fuzzy_match(app_name, apps)
        funcs = []
        for edge in self.app_function_edges:
            edge_app = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_app) == self._normalize(app_name):
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_app('{app_name}') -> {funcs}")
        return funcs

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fns = [self._get_name(f) for f in self.functions]
        fn_name = self._fuzzy_match(fn_name, fns)
        apps = []
        for edge in self.app_function_edges:
            edge_app = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_fn) == self._normalize(fn_name):
                apps.append(edge_app)
        print(f"[DEBUG] get_apps_for_function('{fn_name}') -> {apps}")
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fns = [self._get_name(f) for f in self.functions]
        fn_name = self._fuzzy_match(fn_name, fns)
        vars_ = []
        for edge in self.function_variable_edges:
            edge_fn = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[0])
            edge_var = self._get_name(edge.get("variable") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_fn) == self._normalize(fn_name):
                vars_.append(edge_var)
        print(f"[DEBUG] get_variables_for_function('{fn_name}') -> {vars_}")
        return vars_

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        vars_ = [self._get_name(v) for v in self.variables]
        var_name = self._fuzzy_match(var_name, vars_)
        funcs = []
        for edge in self.function_variable_edges:
            edge_fn = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[0])
            edge_var = self._get_name(edge.get("variable") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_var) == self._normalize(var_name):
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_variable('{var_name}') -> {funcs}")
        return funcs

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        apps = [self._get_name(a) for a in self.applications]
        app_name = self._fuzzy_match(app_name, apps)
        structure = {}
        for edge in self.app_function_edges:
            edge_app = self._get_name(edge.get("app") if isinstance(edge, dict) else edge[0])
            edge_fn = self._get_name(edge.get("function") if isinstance(edge, dict) else edge[1])
            if self._normalize(edge_app) == self._normalize(app_name):
                structure[edge_fn] = self.get_variables_for_function(edge_fn)
        print(f"[DEBUG] get_app_structure('{app_name}') -> {structure}")
        return structure
