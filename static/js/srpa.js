function clean_js()
{
}
function init_js()
{
}
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
    $(document).on('click', '.srpa-loader', function(e){
        var loader_target = $(this).attr('loader-target');
        var loader_type = $(this).attr('loader-type');  // module, page
        var target = this;
        if($(target).parents('li').hasClass('active'))
            return;
        $.ajax({
            type: 'GET',
            url: loader_target,
            success: function(data){
                // Remove older js
                clean_js();
                // Refresh HTML data
                var content = $("#"+loader_type);
                content.fadeOut(0);
                content.html(data);
                content.fadeIn(500);
                // type-related actions
                if(loader_type == 'page')
                    $('li.li-page.active').removeClass('active');
                else if(loader_type == 'module')
                    $('li.li-module.active').removeClass('active');
                $(target).parents('li').addClass('active');
                // Init new js
                init_js();
            },
            error: function(request, error){
                alert('与服务器通信发生错误');
            },
        });
    });
});
