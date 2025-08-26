// main.js

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

async function loadAppVariables(appName) {
    const data = await fetchData(`/variables/app/${appName}`);
    if (data && typeof data === "object") {
        Object.entries(data).forEach(([key, value]) => {
            console.log(`App: ${key}`, value);
            // Insert rendering logic here
        });
    }
}

async function loadFunctions(appName) {
    const data = await fetchData(`/functions/${appName}`);
    if (Array.isArray(data)) {
        data.forEach(fn => console.log(`Function: ${fn}`));
    }
}

async function loadApps(fnName) {
    const data = await fetchData(`/apps/${fnName}`);
    if (Array.isArray(data)) {
        data.forEach(app => console.log(`Application: ${app}`));
    }
}

async function loadFuncsByVariable(varName) {
    const data = await fetchData(`/functions/variable/${varName}`);
    if (Array.isArray(data)) {
        data.forEach(fn => console.log(`Function: ${fn}`));
    }
}

// Initialize visualization when page loads
document.addEventListener("DOMContentLoaded", () => {
    const appName = "shopping_app";
    const fnName = "checkout";
    const varName = "cart_items";

    loadAppVariables(appName);
    loadFunctions(appName);
    loadApps(fnName);
    loadFuncsByVariable(varName);
});
