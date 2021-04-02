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
