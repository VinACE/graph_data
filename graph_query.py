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
        print("[DEBUG] App-Function edges:", self.app_function_edges[:10])

    def _normalize(self, name: str) -> str:
        """Normalize names: lowercase, replace spaces/hyphens with underscores"""
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
        apps = [self._normalize(self._get_name(a)) for a in self.applications]
        app_name_norm = self._normalize(self._fuzzy_match(app_name, apps))
        funcs = []
        for edge in self.app_function_edges:
            # handle list or dict edges
            if isinstance(edge, dict):
                edge_app = self._normalize(self._get_name(edge.get("app", "")))
                edge_fn = self._normalize(self._get_name(edge.get("function", "")))
            elif isinstance(edge, list) or isinstance(edge, tuple):
                edge_app = self._normalize(edge[0])
                edge_fn = self._normalize(edge[1])
            else:
                continue
            if edge_app == app_name_norm:
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_app('{app_name}') -> {funcs}")
        return funcs

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fns = [self._normalize(self._get_name(f)) for f in self.functions]
        fn_name_norm = self._normalize(self._fuzzy_match(fn_name, fns))
        apps = []
        for edge in self.app_function_edges:
            if isinstance(edge, dict):
                edge_app = self._normalize(self._get_name(edge.get("app", "")))
                edge_fn = self._normalize(self._get_name(edge.get("function", "")))
            elif isinstance(edge, list) or isinstance(edge, tuple):
                edge_app = self._normalize(edge[0])
                edge_fn = self._normalize(edge[1])
            else:
                continue
            if edge_fn == fn_name_norm:
                apps.append(edge_app)
        print(f"[DEBUG] get_apps_for_function('{fn_name}') -> {apps}")
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fns = [self._normalize(self._get_name(f)) for f in self.functions]
        fn_name_norm = self._normalize(self._fuzzy_match(fn_name, fns))
        vars_ = []
        for edge in self.function_variable_edges:
            if isinstance(edge, dict):
                edge_fn = self._normalize(self._get_name(edge.get("function", "")))
                edge_var = self._normalize(self._get_name(edge.get("variable", "")))
            elif isinstance(edge, list) or isinstance(edge, tuple):
                edge_fn = self._normalize(edge[0])
                edge_var = self._normalize(edge[1])
            else:
                continue
            if edge_fn == fn_name_norm:
                vars_.append(edge_var)
        print(f"[DEBUG] get_variables_for_function('{fn_name}') -> {vars_}")
        return vars_

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        vars_ = [self._normalize(self._get_name(v)) for v in self.variables]
        var_name_norm = self._normalize(self._fuzzy_match(var_name, vars_))
        funcs = []
        for edge in self.function_variable_edges:
            if isinstance(edge, dict):
                edge_fn = self._normalize(self._get_name(edge.get("function", "")))
                edge_var = self._normalize(self._get_name(edge.get("variable", "")))
            elif isinstance(edge, list) or isinstance(edge, tuple):
                edge_fn = self._normalize(edge[0])
                edge_var = self._normalize(edge[1])
            else:
                continue
            if edge_var == var_name_norm:
                funcs.append(edge_fn)
        print(f"[DEBUG] get_functions_for_variable('{var_name}') -> {funcs}")
        return funcs

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        apps = [self._normalize(self._get_name(a)) for a in self.applications]
        app_name_norm = self._normalize(self._fuzzy_match(app_name, apps))
        structure = {}
        for edge in self.app_function_edges:
            if isinstance(edge, dict):
                edge_app = self._normalize(self._get_name(edge.get("app", "")))
                edge_fn = self._normalize(self._get_name(edge.get("function", "")))
            elif isinstance(edge, list) or isinstance(edge, tuple):
                edge_app = self._normalize(edge[0])
                edge_fn = self._normalize(edge[1])
            else:
                continue
            if edge_app == app_name_norm:
                structure[edge_fn] = self.get_variables_for_function(edge_fn)
        print(f"[DEBUG] get_app_structure('{app_name}') -> {structure}")
        return structure
