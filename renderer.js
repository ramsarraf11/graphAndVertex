const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const addVertexButton = document.getElementById('addVertexButton');
    const addWeightButton = document.getElementById('addWeightButton');
    const shortestPathButton = document.getElementById('shortestPathButton');
    const undoButton = document.getElementById('undoButton');
    const clearButton = document.getElementById('clearButton');
    const addVertexDialogButton = document.getElementById('addVertexDialogButton');
    const addEdgeDialogButton = document.getElementById('addEdgeDialogButton');
    const addWeightDialogButton = document.getElementById('addWeightDialogButton');
    const findShortestPathDialogButton = document.getElementById('findShortestPathDialogButton');

    // Event listeners for the buttons
    addVertexButton.addEventListener('click', () => showAddVertexDialog());
    addWeightButton.addEventListener('click', () => showAddWeightDialog());
    shortestPathButton.addEventListener('click', () => showFindShortestPathDialog());
    undoButton.addEventListener('click', () => undo());
    clearButton.addEventListener('click', () => clearGraph());
    addVertexDialogButton.addEventListener('click', () => addVertex());
    addEdgeDialogButton.addEventListener('click', () => addEdge());
    addWeightDialogButton.addEventListener('click', () => addWeight());
    findShortestPathDialogButton.addEventListener('click', () => findShortestPath());

    // Add a vertex to the graph
    function addVertex() {
        const vertexName = document.getElementById('vertexName').value.trim();
        if (vertexName) {
            ipcRenderer.send('addVertex', vertexName);
            hideDialog('addVertexDialog');
        }
    }

    // Add an edge to the graph
    function addEdge() {
        const sourceVertex = document.getElementById('sourceVertex').value.trim();
        const targetVertex = document.getElementById('targetVertex').value.trim();
        const edgeWeight = parseInt(document.getElementById('edgeWeight').value);

        if (sourceVertex && targetVertex && Number.isInteger(edgeWeight)) {
            ipcRenderer.send('addEdge', { sourceVertex, targetVertex, weight: edgeWeight });
            hideDialog('addEdgeDialog');
        }
    }

    // Add weight to an existing edge
    function addWeight() {
        const sourceVertex = document.getElementById('sourceVertex').value.trim();
        const targetVertex = document.getElementById('targetVertex').value.trim();
        const edgeWeight = parseInt(document.getElementById('edgeWeight').value);

        if (sourceVertex && targetVertex && Number.isInteger(edgeWeight)) {
            ipcRenderer.send('addWeight', { sourceVertex, targetVertex, weight: edgeWeight });
            hideDialog('addWeightDialog');
        }
    }

    // Find the shortest path between two vertices
    function findShortestPath() {
        const sourceVertex = document.getElementById('sourceVertex').value.trim();
        const targetVertex = document.getElementById('targetVertex').value.trim();

        if (sourceVertex && targetVertex) {
            ipcRenderer.send('findShortestPath', { sourceVertex, targetVertex });
            hideDialog('findShortestPathDialog');
        }
    }

    // Undo the last action
    function undo() {
        ipcRenderer.send('undo');
    }

    // Clear the graph
    function clearGraph() {
        ipcRenderer.send('clearGraph');
    }

    // Show the dialog for adding a vertex
    function showAddVertexDialog() {
        console.log(":( you are a asshole")
        showDialog('addVertexDialog');
    }

    // Show the dialog for adding an edge
    function showAddWeightDialog() {
        showDialog('addWeightDialog');
    }

    // Show the dialog for finding the shortest path
    function showFindShortestPathDialog() {
        showDialog('findShortestPathDialog');
    }

    // Show a dialog by ID
    function showDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = 'block';
    }

    // Hide a dialog by ID
    function hideDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = 'none';
    }
});
