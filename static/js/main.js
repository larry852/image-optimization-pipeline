var selected = [];
$('input[type="checkbox"]').bind('click', function() {
    selected = [];
    $('#selectedTransformations').html('');
    $('input:checked').each(function() {
        selected.push($(this).attr('value'));
    });
    for (var i = selected.length - 1; i >= 0; i--) {
        var li = $('<li>');
        li.text(selected[i]).appendTo('#selectedTransformations');
    }
});
$("#process-button").click(function() {
    console.log(selected);
    post('/pipeline/'+$('#original').val(), {list_transformations: selected});
});

function post(path, params, method) {
    method = method || "post";

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

$("#ocr-button").click(function(){

    request = $.ajax({
        url: "/ocr",
        type: "post",
        data: {'text': $('#text').val()}
    });

    request.done(function (response, textStatus, jqXHR){
        console.log(response)
    });
});