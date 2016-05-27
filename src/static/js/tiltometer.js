function set_background(background_url){
    $('body').css('background-image', 'url(' + background_url + ')');
}

function set_gauge(summoner_name, tilt){
    var g = new JustGage({
        id: "gauge",
        value: tilt,
        min: 0,
        max: 100,
        title: summoner_name,
        label: "tilt points"
    });
}

$('#show-stats-button').click(function(){
    if ($(this).text() == "Stats") {
      $(this).text("Tiltometer");
   }
   else {
      $(this).text("Stats");
   }
    $("#tiltometer-section").toggle();
    $("#stats-section").slideToggle();
});

$( document ).ready(function() {
    set_background($BACKGROUND);
    set_gauge($SUMMONER_NAME, $TILT_LEVEL);
});
