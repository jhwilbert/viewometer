$(document).ready(function(){
    
    var searchOptions = {
        target: '#url', // target to be updated with response
        beforeSubmit: holdUser, 
        success: showSearchQuery,
        dataType: "html", 
        resetForm: true 
    }
    
    $('#search').ajaxForm(searchOptions);
    
    $('.linked-search').live({
        mouseover: function() {
            $(this).stop().fadeTo(100, 0.8);
        },
        mouseout: function() {
            $(this).stop().fadeTo(100, 1);
        },
        click: function(){
            location = $(this).data(url);
        }
    })
    
    
});

function holdUser(formData, jqForm, options) {
    $("#status").html("Please wait. Your search is being submitted...");
    $("#status").fadeIn();
    return true;
}

function showSearchQuery(responseText, statusText, xhr, $form) {
    $("#status").fadeOut(function() {
        $(this).html("Search registered. Your search URL is <a href="+responseText+">"+responseText+"</a><br>Refresh this page to see it.").fadeIn();
    });
}