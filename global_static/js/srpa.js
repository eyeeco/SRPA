$(function(){
    $(document).on('click', 'img.captcha', function(){
        var refresh_url = $(this).attr('refresh-url');
        $.getJSON(refresh_url, {}, function(json) {
            var img = $('#id_captcha_2');
            var hidden = $('#id_captcha_0');
            hidden.prop('value', json.key);
            img.prop('src', json.img);
        });
    });
});
