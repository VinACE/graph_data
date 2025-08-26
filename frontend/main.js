// main.js

// ---------------- Utility Functions ----------------

// Fetch data from a given endpoint safely
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            console.error(`HTTP error! status: ${response.status}`);
            return null;
        }
        const data = await response.json();
        return data;
    } catch (err) {
        console.error("Fetch error:", err);
        return null;
    }
}

// Render variables by application
async function loadAppVariables(appName) {
    const data = await fetchData(`/variables/app/${appName}`);
    console.log("Variables received:", data);

    if (data && typeof data === "object") {
        Object.entries(data).forEach(([key, value]) => {
            console.log(`App: ${key}, Variables: ${value}`);
            // Example: render to DOM or chart
            // renderVariables(key, value);
        });
    } else {
        console.warn("No variables data available for app:", appName);
    }
}

// Render functions by application
async function loadFunctions(appName) {
    const data = await fetchData(`/functions/${appName}`);
    console.log("Functions received:", data);

    if (Array.isArray(data)) {
        data.forEach(fn => {
            console.log(`Function: ${fn}`);
            // Example: render to DOM or chart
            // renderFunction(fn);
        });
    } else {
        console.warn("No functions data available for app:", appName);
    }
}

// Render applications by function
async function loadApps(fnName) {
    const data = await fetchData(`/apps/${fnName}`);
    console.log("Applications received:", data);

    if (Array.isArray(data)) {
        data.forEach(app => {
            console.log(`Application: ${app}`);
            // Example: render to DOM or chart
        });
    } else {
        console.warn("No applications data available for function:", fnName);
    }
}

// Render functions by variable
async function loadFuncsByVariable(varName) {
    const data = await fetchData(`/functions/variable/${varName}`);
    console.log("Functions by variable received:", data);

    if (Array.isArray(data)) {
        data.forEach(fn => {
            console.log(`Function: ${fn}`);
            // Example: render to DOM or chart
        });
    } else {
        console.warn("No functions data available for variable:", varName);
    }
}

// ---------------- Initialize Visualization ----------------
document.addEventListener("DOMContentLoaded", async () => {
    const exampleAppName = "shopping_app";  // Example application
    const exampleFunctionName = "checkout"; // Example function
    const exampleVariableName = "cart_items"; // Example variable

    // Load data
    await loadAppVariables(exampleAppName);
    await loadFunctions(exampleAppName);
    await loadApps(exampleFunctionName);
    await loadFuncsByVariable(exampleVariableName);

    console.log("Frontend data fetch complete.");
});
