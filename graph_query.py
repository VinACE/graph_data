import json

class GraphQuery:
    def __init__(self, json_file="graph_data.json"):
        with open(json_file, "r") as f:
            self.data = json.load(f)

        # index apps, functions, variables by id for fast lookup
        self.apps = {app["id"]: app for app in self.data["applications"]}
        self.functions = {fn["id"]: fn for fn in self.data["functions"]}
        self.variables = {var["id"]: var for var in self.data["variables"]}

    # 🔹 Get all functions for a given application
    def get_functions_for_app(self, app_name):
        app_id = self._find_app_id(app_name)
        if not app_id:
            return []
        return [self.functions[e["function"]]["name"]
                for e in self.data["app_function_edges"] if e["app"] == app_id]

    # 🔹 Get all applications that use a given function
    def get_apps_for_function(self, function_name):
        fn_id = self._find_fn_id(function_name)
        if not fn_id:
            return []
        return [self.apps[e["app"]]["name"]
                for e in self.data["app_function_edges"] if e["function"] == fn_id]

    # 🔹 Get all variables used by a function
    def get_variables_for_function(self, function_name):
        fn_id = self._find_fn_id(function_name)
        if not fn_id:
            return []
        return [self.variables[e["variable"]]["name"]
                for e in self.data["function_variable_edges"] if e["function"] == fn_id]

    # 🔹 Get all functions that use a variable
    def get_functions_for_variable(self, variable_name):
        var_id = self._find_var_id(variable_name)
        if not var_id:
            return []
        return [self.functions[e["function"]]["name"]
                for e in self.data["function_variable_edges"] if e["variable"] == var_id]

    # 🔹 Full path: App → Functions → Variables
    def get_app_structure(self, app_name):
        functions = self.get_functions_for_app(app_name)
        result = {}
        for fn in functions:
            result[fn] = self.get_variables_for_function(fn)
        return result

    # -------------------
    # internal helpers
    # -------------------
    def _find_app_id(self, app_name):
        for k, v in self.apps.items():
            if v["name"].lower() == app_name.lower():
                return k
        return None

    def _find_fn_id(self, fn_name):
        for k, v in self.functions.items():
            if v["name"].lower() == fn_name.lower():
                return k
        return None

    def _find_var_id(self, var_name):
        for k, v in self.variables.items():
            if v["name"].lower() == var_name.lower():
                return k
        return None
