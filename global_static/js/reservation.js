$(function () {    
    $('[data-toggle="tooltip"]').tooltip();
    $('.form_datetime_day').datetimepicker({
        language: 'zh',
        format: 'yyyy-mm-dd',
        weekStart: 1,
        autoclose: true,
        minView: 2,
    });
    $('.form_datetime_hour').datetimepicker({
        language: 'zh',
        format: 'yyyy-mm-dd hh:00:00',
        weekStart: 1,
        autoclose: true,
        minView: 1,
    });
})
/*
$(function () {
    $('.srpa-loader[loader-type="page"]').first().click();
    $('[data-toggle="tooltip"]').tooltip();
    $('.form_datetime_day').datetimepicker({
        language: 'zh',
        format: 'yyyy-mm-dd',
        weekStart: 1,
        autoclose: true,
        minView: 2,
    });
    $('.form_datetime_hour').datetimepicker({
        language: 'zh',
        format: 'yyyy-mm-dd hh:00:00',
        weekStart: 1,
        autoclose: true,
        minView: 1,
    });
})
function clean_js()
{
    $('.form_datetime_day').datetimepicker('remove');
    $('.form_datetime_hour').datetimepicker('remove');
}
function init_js()
{

    $('#info-form').on('submit', function(e){
        var form = $('#info-form');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                if(data.status == 0)
                    window.location.href=data.redirect;
                else if(data.status != 1)
                    alert(data.reason);
                $('#page').html(data.html);
                init_js();
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
}
*/