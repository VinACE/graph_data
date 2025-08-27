import json

class GraphQuery:
    def __init__(self, json_file):
        with open(json_file, "r") as f:
            self.data = json.load(f)

    def list_apps(self):
        return [app["name"] for app in self.data["applications"]]

    def get_functions_for_app(self, app_name):
        for app in self.data["applications"]:
            if app["name"] == app_name:
                return [fn["name"] for fn in app["functions"]]
        return []

    def get_apps_for_function(self, fn_name):
        apps = []
        for app in self.data["applications"]:
            for fn in app["functions"]:
                if fn["name"] == fn_name:
                    apps.append(app["name"])
        return apps

    def get_variables_for_function(self, fn_name):
        vars_set = set()
        for app in self.data["applications"]:
            for fn in app["functions"]:
                if fn["name"] == fn_name:
                    vars_set.update(fn.get("variables", []))
        return list(vars_set)

    def get_app_structure(self, app_name):
        for app in self.data["applications"]:
            if app["name"] == app_name:
                return {fn["name"]: fn.get("variables", []) for fn in app["functions"]}
        return {}

    def get_functions_for_variable(self, var_name):
        funcs = []
        for app in self.data["applications"]:
            for fn in app["functions"]:
                if var_name in fn.get("variables", []):
                    funcs.append(fn["name"])
        return funcs
