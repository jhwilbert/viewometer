$(document).ready(function(){
    
    $('#search').ajaxForm(function(data) { 
        $("#url").html("Search registered. Your search URL is"+ "<br><a href="+data+">"+data+"</a>"); 
    });
});
