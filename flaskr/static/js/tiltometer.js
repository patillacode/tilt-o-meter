function sendForm() {
    toggleSpinner();

    const form = document.forms[0];
    const region = form.elements[0].value;
    const summoner_name = form.elements[1].value;

    if (region && summoner_name) {
        const url = `/tilt-o-meter/${region}/${summoner_name}`;
        form.action = url;
        form.submit();
    }
}

function toggleSpinner() {
    var spinner = document.getElementById('spinner');
    var overlay = document.getElementById('overlay');

    if (spinner.style.display === 'none') {
        spinner.style.display = 'block';
        overlay.style.opacity = '0.3';
    } else {
        spinner.style.display = 'none';
    }
}

function drawChart() {
    var tilt = document.getElementById('tilt-value').value;
    var canvas = document.getElementById('tilt-chart');
    var ctx = canvas.getContext('2d');

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
            animations: {
                tension: {
                    duration: 5000,
                    easing: 'linear',
                    loop: true
                }
            },
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
