$(function () {
    $(".lb").css({"width":$(".img").css("width")});
    $(window).resize(function() {
      $(".lb").css({"width":$(".img").css("width")});
    });
});