/* Variables */

url = "http://localhost:8080/output/display_videos"

$(document).ready(function(){
	
	s=setTimeout("getJSON()",1000);
	
});


// first get the highlighted ones and push them
$.getJSON(url, function(data) {		
	$.each(data, function(key, val) {
	    d1.push([i, Math.sin(i)]);
	    
		console.debug(val.info['url'])
		console.debug(val.info['date_published'])
		console.debug(val.info['title'])
		console.debug(val.info['thumbs'])
		
		console.debug(val.views)
	});
});