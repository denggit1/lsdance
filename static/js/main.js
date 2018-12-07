$(function () {
    $(".lb").css({"width":$(".img").css("width")});
    // $(".hh").css({"width":$(window).width()/2});
    $(".sr").children("div").children("input").addClass("form-control");
    $(window).resize(function() {
      $(".lb").css({"width":$(".img").css("width")});
      // $(".hh").css({"width":$(window).width()/2});
    });
    $(".zctj").click(function() {
        var stuid = $.trim($("input[name='stuid']").val());
        var pwd = $("input[name='upwd']").val();
        var pwd2 = $("input[name='upwd2']").val();
        var reg1 = /^[1]\d[2-3][0]\d{5}$/;   /*定义验证表达式*/
        if(!reg1.test(stuid)){
            alert("请输入规范的学号!");
            return false;
        }
        else if(pwd.length<6 | pwd.length>16){
            alert("请输入6-16位的密码!");
            return false;
        }
        else if (pwd != pwd2) {
            alert("两次密码不一致!");
            $("input[name='upwd']").val("");
            $("input[name='upwd2']").val("");
            return false;
        }
    })
});