$(document).ready(function() {
						

  $(".menu").mouseenter(function() {
    $(this).css("background-color","#bbbbbb");
    $(".submenu").css("display", "block");
  });
  $(".menu").mouseleave(function() {
    $(this).css("background-color","#20416c");
    $(".submenu").css("display", "none");
  });
  
});


