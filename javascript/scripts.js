/* Variables */

url = "http://localhost:8082/output/display_videos"

/* Arrays */
videos = []

$(document).ready(function(){
	
    $.getJSON(url, function(data) {		
    	$.each(data, function(key, val) {
            
            videos[key] = new VideoEntry(key,val)
    	});
    });
    

	$('#search').submit(function() {
      
      return true;
    });
    
});


function VideoEntry(key,val) {
    
    // Create Video Elements (parent)
    $(document.createElement("div")).attr("id","video_"+key).appendTo("#container").addClass("span-24 border video");
    
    // Create Image  (child)
    $(document.createElement("img")).attr({ src: val.info['thumbs'] }).attr("id","img_"+key).appendTo("#video_"+key);
    
    // Create Title  (child)
    $(document.createElement("div")).attr("id","title_"+key).appendTo("#video_"+key).html(val.info['title']);
    
     // Create Date  (child)
    $(document.createElement("div")).attr("id","date_"+key).appendTo("#video_"+key).html(val.info['date_published']);
    
     // Create URL  (child)
    $(document.createElement("div")).attr("id","url_"+key).appendTo("#video_"+key).html(val.info['url']);
           
    $(document.createElement("div")).attr("id","graph_"+key).appendTo("#video_"+key).addClass("graph").css("width","500px").css("height","200px");
    
    var d2 = [[4, 7], [12, 8], [3, 5]];
    
    $(function () {
        //$.plot($("#graph"+key), [d2]);
    });   
    // console.debug(val.info['url'])
    // console.debug(val.info['date_published'])
    // console.debug(val.info['title'])
    // console.debug(val.info['thumbs'])

     console.debug(val.views);
    // console.debug(val.tags);
    
}