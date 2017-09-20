$(function () {
    $('.srpa-loader[loader-type="page"]').first().click();
})
function clean_js()
{
    $('.form_datetime_day').datetimepicker('remove');
    $('.form_datetime_hour').datetimepicker('remove');
}
function init_js()
{
    $('[data-toggle="tooltip"]').tooltip();
    $('.form_datetime_day').datetimepicker({
        format: 'yyyy-mm-dd',
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        minView: 2,
    });
    $('.form_datetime_hour').datetimepicker({
        format: 'yyyy-mm-dd hh:00:00',
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        minView: 1,
    });
    $('#search-form').on('submit', function(e){
        var form = $('#search-form');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                if(data.status == 0)
                    $('#status_table').html(data.html);
                else
                {
                    alert(data.reason);
                    $('#status_table').html('');
                }
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
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
                if(data.status == 2)
                    alert(data.reason);
                clean_js();
                $('#page').html(data.html);
                init_js();
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
}
