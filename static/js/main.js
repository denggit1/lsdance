$(function () {
    $(".lb").css({"width":$(".img").css("width")});
    // $(".hh").css({"width":$(window).width()/2});
    $(".qun").css({"width":$(window).width()/2});
    $(".sr").children("div").children("input").addClass("form-control");
    $(window).resize(function() {
        $(".lb").css({"width":$(".img").css("width")});
        // $(".hh").css({"width":$(window).width()/2});
        $(".qun").css({"width":$(window).width()/2});
    });
    $(".zctj").click(function() {
        var stuid = $.trim($("input[name='stuid']").val());
        var pwd = $("input[name='upwd']").val();
        var pwd2 = $("input[name='upwd2']").val();
        var reg1 = /^\d{2}[2-3][0]\d{5}$/;   /*定义验证表达式*/
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
        else {
            $.ajax({
                url: '/register',
                type: 'post',
                data: {'stuid':stuid, 'upwd':pwd},
                dataType: 'json',
                success: function(data){
                    if(data.status=='sid1'){
                        alert('用户名已存在！')
                    }
                    else if(data.status=='sid0'){
                        alert('注册成功！');
                        window.location.replace("/");
                    }
                }
            })
        }
    });
    $(".dltj").click(function () {
        var stuid= $.trim($("input[name='stuid']").val());
        var upwd = $("input[name='upwd']").val();
        if (!stuid){
            alert('用户名不能为空！')
        }
        else if (!upwd){
            alert('密码不能为空！')
        }
        else {
            $.ajax({
                url: '/login',
                type: 'post',
                data: {'stuid':stuid, 'upwd':upwd},
                dataType: 'json',
                success: function(data){
                    if(data.status=='sid0'){
                        alert('用户名不存在！');
                    }
                    else if (data.status=='pwd0') {
                        alert('密码错误！');
                    }
                    else if (data.status=='ok'){
                        alert('登录成功');
                        window.location.replace("/");
                    }
                }
            });
        }
    });
});