$('#summoner-input-button').click(function(){
  summoner_name = $("#summoner-text-input").val();
  console.log($(this).attr('host') + "/tilt-o-meter/" + summoner_name);
  window.location.href = $(this).attr('host') + "/tilt-o-meter/" + summoner_name;
});