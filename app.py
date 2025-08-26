from fastapi import FastAPI
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
from graph_query import GraphQuery

app = FastAPI(
    title="Graph Data API",
    description="REST API for querying applications, functions, and variables from a graph dataset.",
    version="1.0.0",
)

# Mount frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Initialize GraphQuery
graph = GraphQuery("graph_data.json")

# ---------------- Endpoints with debug ----------------

@app.get("/functions/{app_name}", response_model=List[str])
def functions_by_app(app_name: str):
    print(f"[DEBUG] Requested app name: {app_name}")
    result = graph.get_functions_for_app(app_name)
    print(f"[DEBUG] Found functions: {result}")
    return result

@app.get("/apps/{fn_name}", response_model=List[str])
def apps_by_function(fn_name: str):
    print(f"[DEBUG] Requested function name: {fn_name}")
    result = graph.get_apps_for_function(fn_name)
    print(f"[DEBUG] Found apps: {result}")
    return result

@app.get("/variables/function/{fn_name}", response_model=List[str])
def vars_by_function(fn_name: str):
    print(f"[DEBUG] Requested function name for variables: {fn_name}")
    result = graph.get_variables_for_function(fn_name)
    print(f"[DEBUG] Found variables: {result}")
    return result

@app.get("/variables/app/{app_name}", response_model=Dict[str, List[str]])
def vars_by_app(app_name: str):
    print(f"[DEBUG] Requested app name for variables: {app_name}")
    result = graph.get_app_structure(app_name)
    print(f"[DEBUG] Found app structure: {result}")
    return result

@app.get("/functions/variable/{var_name}", response_model=List[str])
def funcs_by_variable(var_name: str):
    print(f"[DEBUG] Requested variable name: {var_name}")
    result = graph.get_functions_for_variable(var_name)
    print(f"[DEBUG] Found functions: {result}")
    return result

# ---------------- Run block ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
