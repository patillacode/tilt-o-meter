$('#summoner-input-button').click(function(){
  summoner_name = $("#summoner-text-input").val();
  area = $("#area-select").val();
  // console.log($(this).attr('host') + "/tilt-o-meter/" + area + "/" + summoner_name);
  window.location.href = $(this).attr('host') + "/tilt-o-meter/" + area + "/" + summoner_name;
});

$("#summoner-text-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#summoner-input-button").click();
    }
});