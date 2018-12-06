$(function () {
    $(".lb").css({"width":$(".img").css("width")});
    $(".hh").css({"width":$(window).width()/2});
    $(".sr").children("div").children("input").addClass("form-control");
    $(window).resize(function() {
      $(".lb").css({"width":$(".img").css("width")});
      $(".hh").css({"width":$(window).width()/2});
    });
    $(".zctj").click(function() {
        var pwd = $("input[name='upwd']").val();
        var pwd2 = $("input[name='upwd2']").val();
        if (pwd != pwd2) {
            alert("两次密码不一致!");
            $("input[name='upwd']").val("");
            $("input[name='upwd2']").val("");
            return false;
        }
    })
});