// Copyright (c) 2021 by Tom Miller (https://codepen.io/creativeocean/pen/QWdpzPg)

// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



// Based on Tom Miller's Smoke Ring
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
