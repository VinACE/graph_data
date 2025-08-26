const cyContainer = document.getElementById('cy');
const appSelect = document.getElementById('appSelect');

// Populate dropdown with available apps
// For simplicity, we'll hardcode apps here; you can fetch dynamically if you have an endpoint
const apps = ["ShoppingApp", "FinanceApp"];
apps.forEach(app => {
    const option = document.createElement('option');
    option.value = app;
    option.text = app;
    appSelect.appendChild(option);
});

// Load graph initially
loadGraph(appSelect.value);

appSelect.addEventListener('change', () => {
    loadGraph(appSelect.value);
});

function loadGraph(appName) {
    fetch(`/variables/app/${appName}`)
        .then(res => res.json())
        .then(appData => {
            const elements = [];

            // Add App node
            elements.push({ data: { id: appName, label: appName } });

            // Add functions and variables
            const functions = appData[appName];
            for (const [fn, vars] of Object.entries(functions)) {
                elements.push({ data: { id: fn, label: fn } });
                elements.push({ data: { source: appName, target: fn } });

                vars.forEach(v => {
                    elements.push({ data: { id: v, label: v } });
                    elements.push({ data: { source: fn, target: v } });
                });
            }

            // Clear previous graph
            cyContainer.innerHTML = '';

            // Render Cytoscape graph
            cytoscape({
                container: cyContainer,
                elements: elements,
                style: [
                    {
                        selector: 'node',
                        style: {
                            'label': 'data(label)',
                            'background-color': '#0074D9',
                            'color': '#fff',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'width': 'label',
                            'height': 'label',
                            'padding': '10px'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'line-color': '#ccc',
                            'target-arrow-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }
                    }
                ],
                layout: { name: 'breadthfirst', directed: true, padding: 10 }
            });
        });
}
