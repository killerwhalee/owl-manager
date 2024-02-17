// Plot the graph
const Chart = window.Chart;

for (let i = 1;;i++) {
    // Take input from html
    X_INPUT = document.getElementById('csvInput-x-' + i);
    Y_INPUT = document.getElementById('csvInput-y-' + i);
    
    if (!X_INPUT || !Y_INPUT) {
        break;
    }
    
    GRAPH = document.getElementById('plotting-' + i);
    X_DATA = JSON.parse(X_INPUT.value);
    Y_DATA = JSON.parse(Y_INPUT.value);
    
    X_INPUT.value = "";
    Y_INPUT.value = "";
    
    color = Math.floor(Math.random() * 240);
    light = Math.floor(Math.random() * 80);
    
    new Chart(GRAPH, {
        type: 'line',
        data: {
            labels: X_DATA,
            datasets: [{
                data: Y_DATA,
                fill: false,
                borderColor: `hsl(${color}, 100%, ${light}%)`,
                tension: 0.1
            }]
        },
        options: {
            elements: {
                point: {
                    pointStyle: false
                },
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    // display: false,
                    type: 'linear'
                },
                y: {
                    display: false,
                    min: -5,
                    max: 105
                },
            },
            animation: {
                onComplete: function () {
                    var a = document.getElementById('imageDownload-' + i);
                    a.href = this.toBase64Image();
                },
            },
        },
        plugins: []
    });
}

