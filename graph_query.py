import json
from typing import List, Dict

class GraphQuery:
    def __init__(self, data_file: str):
        with open(data_file, "r") as f:
            self.data = json.load(f)

    def get_functions_for_app(self, app_name: str) -> List[str]:
        app = self.data.get(app_name)
        if app and "functions" in app:
            return app["functions"]
        return []

    def get_apps_for_function(self, fn_name: str) -> List[str]:
        fn_name = fn_name.lower()
        apps = [
            app_name
            for app_name, details in self.data.items()
            if "functions" in details and any(fn.lower() == fn_name for fn in details["functions"])
        ]
        return apps

    def get_variables_for_function(self, fn_name: str) -> List[str]:
        fn_name = fn_name.lower()
        vars_list = []
        for app in self.data.values():
            variables = app.get("variables", {})
            for func, vars_ in variables.items():
                if func.lower() == fn_name:
                    vars_list.extend(vars_)
        return vars_list

    def get_app_structure(self, app_name: str) -> Dict[str, List[str]]:
        app = self.data.get(app_name)
        if app and "variables" in app:
            return app["variables"]
        return {}

    def get_functions_for_variable(self, var_name: str) -> List[str]:
        var_name = var_name.lower()
        funcs = []
        for app in self.data.values():
            variables = app.get("variables", {})
            for func, vars_ in variables.items():
                if var_name in [v.lower() for v in vars_]:
                    funcs.append(func)
        return funcs
