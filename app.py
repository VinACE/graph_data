"""from flask import Flask, request, jsonify
import sys
from graph_query import GraphQuery

graph = GraphQuery("graph_data.json")
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
"""

from fastapi import FastAPI
from typing import List, Dict
from graph_query import GraphQuery

graph = GraphQuery("graph_data.json")
app = FastAPI(
    title="Graph Data API",
    description="REST API for querying applications, functions, and variables from a graph dataset.",
    version="1.0.0",
)

# ---------------- REST API ----------------
@app.get("/functions/{app_name}", response_model=List[str], summary="Get functions by application")
def functions_by_app(app_name: str):
    return graph.get_functions_for_app(app_name)

@app.get("/apps/{fn_name}", response_model=List[str], summary="Get applications by function")
def apps_by_function(fn_name: str):
    return graph.get_apps_for_function(fn_name)

@app.get("/variables/function/{fn_name}", response_model=List[str], summary="Get variables by function")
def vars_by_function(fn_name: str):
    return graph.get_variables_for_function(fn_name)

@app.get("/variables/app/{app_name}", response_model=Dict[str, List[str]], summary="Get variables by application")
def vars_by_app(app_name: str):
    # GraphQuery doesn’t have get_variables_for_app, so we use get_app_structure
    return graph.get_app_structure(app_name)

@app.get("/functions/variable/{var_name}", response_model=List[str], summary="Get functions by variable")
def funcs_by_variable(var_name: str):
    return graph.get_functions_for_variable(var_name)

# ---------------- Run ----------------
# Run the API with: uvicorn app:app --host 0.0.0.0 --port 5000 --reload
