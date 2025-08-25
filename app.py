from flask import Flask, request, jsonify
import sys
from graph_query.py import GraphDemo

graph = GraphDemo("graph_data.json")
app = Flask(__name__)

# ---------------- REST API ----------------
@app.route("/functions/<app_name>")
def functions_by_app(app_name):
    return jsonify(graph.get_functions_by_app(app_name))

@app.route("/apps/<fn_name>")
def apps_by_function(fn_name):
    return jsonify(graph.get_apps_by_function(fn_name))

@app.route("/variables/function/<fn_name>")
def vars_by_function(fn_name):
    return jsonify(graph.get_variables_by_function(fn_name))

@app.route("/variables/app/<app_name>")
def vars_by_app(app_name):
    return jsonify(graph.get_variables_by_app(app_name))

@app.route("/functions/variable/<var_name>")
def funcs_by_variable(var_name):
    return jsonify(graph.get_functions_by_variable(var_name))

# ---------------- CLI Mode ----------------
def cli():
    if len(sys.argv) < 3:
        print("Usage:")
        print(" python app.py functions <AppName>")
        print(" python app.py apps <FunctionName>")
        print(" python app.py vars_fn <FunctionName>")
        print(" python app.py vars_app <AppName>")
        print(" python app.py funcs_var <VariableName>")
        return

    cmd, name = sys.argv[1], sys.argv[2]

    if cmd == "functions":
        print(graph.get_functions_by_app(name))
    elif cmd == "apps":
        print(graph.get_apps_by_function(name))
    elif cmd == "vars_fn":
        print(graph.get_variables_by_function(name))
    elif cmd == "vars_app":
        print(graph.get_variables_by_app(name))
    elif cmd == "funcs_var":
        print(graph.get_functions_by_variable(name))
    else:
        print("Unknown command.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] not in ["runserver"]:
        cli()
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
