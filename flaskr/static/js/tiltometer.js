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

function drawTiltValue() {
    console.log('drawing tilt value.....');
    var tilt = document.getElementById('tilt-value').value;
    var canvas = document.getElementById('tilt-chart');
    var ctx = canvas.getContext('2d');
    var x = canvas.width / 2;
    var y = canvas.height / 2;

    ctx.font = '24pt Swiftel';
    ctx.fillStyle = '#ff6900';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(tilt, x, y);
    console.log('done!');
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
            // animation: {
            //     onComplete: drawTiltValue()
            // },
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
