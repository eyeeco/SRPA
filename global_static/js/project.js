$(function () {    
    $('[data-toggle="tooltip"]').tooltip();
    $('.form_datetime_hour').datetimepicker({
        format: 'yyyy-mm-dd hh:00:00',
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        minView: 1,
    });
    var x = 10000;
    $("#add-one-term").click(function(){
        x = x + 1;
        $.ajax({
            type: 'GET',
            url: $("#add-one-term").attr('action'),
            data: {"id":x},
            success: function(data){
                $("#data-forms").prepend(data.html);
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
    $(document).on('click','.delete-one-term',function(){
        $(this).parents(".budget").remove(); 
    });
    $("#info-form").on('submit',function(e) {
        var has_empty = false;
        $(".item").each(function(index,element){
            if(has_empty)return;
            if($(this).val() == ""){
                has_empty = true;
                e.preventDefault();
            }
        });
        $(".amount").each(function(){
            if(!has_empty && $(this).val() == ""){
                has_empty = true;
                e.preventDefault();
            }
        });
        if(has_empty){
            alert("预算明细不能为空");
            e.preventDefault();
        }
    });

})
