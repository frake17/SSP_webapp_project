$(document).ready(function(){
  $("#box").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".item").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});