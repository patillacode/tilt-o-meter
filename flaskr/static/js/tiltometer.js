function sendForm() {
    const form = document.forms[0];
    const region = form.elements[0].value;
    const summoner_name = form.elements[1].value;

    if (region && summoner_name) {
        const url = `/tilt-o-meter/${region}/${summoner_name}`;
        form.action = url;
        form.submit();
    }
}


function drawChart() {
    console.log('DOM is ready.');
    var tilt = document.getElementById('tilt-value').value;
    var ctx = document.getElementById('tilt-chart').getContext('2d');
    const data = {
        labels: [
            'tilted',
            'not tilted',
        ],
        datasets: [{
            label: 'Tilt Level',
            data: [tilt, 100 - tilt],
            backgroundColor: [
                'rgb(255, 105, 0)',
                'rgb(150, 150, 150)',
            ],
            hoverOffset: 1
        }]
    };

    var tiltChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff'
                    }
                },
                title: {
                    display: false,
                    text: 'tilt-o-meter chart',
                    color: '#fff'
                }
            }
        },
    });
}
