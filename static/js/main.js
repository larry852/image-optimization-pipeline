$('input[type="checkbox"]').bind('click', function() {
    selected = [];
    $('#selectTransformations').html('');

    $('input:checked').each(function() {
        selected.push($(this).attr('value'));
    });

    for (var i = selected.length - 1; i >= 0; i--) {
	    var li = $('<li>');
	    li.text(selected[i]).appendTo('#selectTransformations');
    }    
});