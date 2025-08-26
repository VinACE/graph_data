# Graph Data API

A **REST API** built with **FastAPI** for exploring relationships between applications, functions, and variables in a graph dataset. This project allows developers and analysts to query how applications use functions, what variables are involved, and how everything connects.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [API Endpoints](#api-endpoints)
- [Examples](#examples-from-graph_datajson)
- [Visual Diagram](#visual-diagram)
- [Usage](#usage)
- [Swagger / Interactive Documentation](#swagger--interactive-documentation)
- [License](#license)

---

## Project Structure

```
graph_data/
├─ app.py               # FastAPI application with API endpoints
├─ graph_query.py       # GraphQuery class for data querying logic
├─ graph_data.json      # Sample graph dataset
└─ README.md            # Project documentation
```

- `app.py` – Main API application using **FastAPI**.  
- `graph_query.py` – Contains the **GraphQuery** class that loads the JSON data and provides querying methods.  
- `graph_data.json` – Dataset describing applications, functions, variables, and their relationships.  

---

## Dataset

- **applications** – Apps being analyzed (e.g., `ShoppingApp`, `FinanceApp`).  
- **functions** – Actions that apps can perform (e.g., `add_to_cart`, `checkout`).  
- **variables** – Data used by functions (e.g., `cart_id`, `payment_method`).  
- **edges** – Connections between apps & functions (`app_function_edges`) and functions & variables (`function_variable_edges`).  

---

## API Endpoints

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `/functions/{app_name}` | List all functions an app can perform | List of function names |
| `/apps/{fn_name}` | List all apps that use a specific function | List of app names |
| `/variables/function/{fn_name}` | List all variables used by a function | List of variable names |
| `/variables/app/{app_name}` | List all variables in an app, grouped by function | Dictionary: function → variables |
| `/functions/variable/{var_name}` | List all functions that use a specific variable | List of function names |

---

## Examples from `graph_data.json`

### 1. `/functions/{app_name}`
**Request:**  
`GET /functions/ShoppingApp`  
**Response:**
```json
["add_to_cart", "checkout"]
```

### 2. `/apps/{fn_name}`
**Request:**  
`GET /apps/checkout`  
**Response:**
```json
["ShoppingApp", "FinanceApp"]
```

### 3. `/variables/function/{fn_name}`
**Request:**  
`GET /variables/function/checkout`  
**Response:**
```json
["cart_id", "payment_method"]
```

### 4. `/variables/app/{app_name}`
**Request:**  
`GET /variables/app/ShoppingApp`  
**Response:**
```json
{
  "add_to_cart": ["cart_id"],
  "checkout": ["cart_id", "payment_method"]
}
```

### 5. `/functions/variable/{var_name}`
**Request:**  
`GET /functions/variable/cart_id`  
**Response:**
```json
["add_to_cart", "checkout"]
```

---

## Visual Diagram

ShoppingApp
│
├─ add_to_cart
│   └─ cart_id
│
└─ checkout
    ├─ cart_id
    └─ payment_method

*This diagram helps visualize how applications, functions, and variables are connected.*

---

## Usage

### 1. Install dependencies
```bash
pip install fastapi uvicorn
```

### 2. Run the API
```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

### 3. Access interactive documentation
- Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)  
- ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)  

You can test all endpoints directly in the browser using Swagger.

---

## License

This project is licensed under the **MIT License**.

