$(".password-view").click(function () {
    var type = $('.password').attr('type');
    if (type == 'password') {
        $('.password').attr('type', 'text');
        $('.password-icon i').removeClass('far fa-eye');
        $('.password-icon i').addClass('fas fa-eye-slash');
    }
    else {
        $('.password').attr('type', 'password');
        $('.password-icon i').addClass('far fa-eye');
        $('.password-icon i').removeClass('fas fa-eye-slash');
    }
    console.log(type);
});