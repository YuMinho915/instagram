$(document).ready(function(){
    $('.register_container').hide()
});

//회원가입 버튼
function register_change(){
    $('.login_container').hide()
    $('.register_container').show()
}

//회원가입 취소 버튼
function register_change2(){
    $('.login_container').show()
    $('.register_container').hide()
}


function register(){
    let email =  $('#email').val()
    let name = $('#name').val()
    let nickname = $('#nickname').val()
    let password = $('#pw').val()


    $.ajax({
        type: "POST",
        url: "/sign_up",
        data: {
            email_give: email,
            name_give: name,
            nickname_give: nickname,
            password_give : password
        },
        success: function (response) {
            alert(response['msg'])


        },
    });
}
//로그인 하기!
function login(){
    let email = $('#login_email').val()
    let password = $('#login_pw').val()


    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            email_give: email,
            password_give: password
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")

            } else {
                alert(response['msg'])
            }
        }
    });
}

