gsap.registerPlugin(Draggable);

function rotateNeedle(tilt) {
    gsap.to(".needle", {
        rotation: 40 + ((tilt * 270) / 100)
    });
}

window.onload = function() {
    tilt = document.getElementById('tilt_value').value;
    rotateNeedle(tilt);
    toggleSpinner();
};

window.onmousemove = window.ontouchmove = (e) => {
    if (e.touches) {
        e.clientX = e.touches[0].clientX;
        e.clientY = e.touches[0].clientY;
    }
    gsap.to("#c, #s", {
        rotationY: -20 + (e.clientX / innerWidth) * 40,
        rotationX: 10 - (e.clientY / innerHeight) * 20
    });
};

gsap.set(".needle", {
    transformOrigin: "100px 100px",
    rotation: 40
});
gsap.set(".ring1", {
    transformOrigin: "50% 50%",
    rotation: 130
});
gsap.set(".speed-app", {
    perspective: 400
});
gsap.set("#s", {
    overflow: "visible",
    width: "66.7%",
    height: "66.7%",
    left: "50%",
    top: "50%",
    xPercent: -50,
    yPercent: -50,
    z: 20
});
