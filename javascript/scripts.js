/* Variables */

url = "http://localhost:8082/output/display_videos"

/* Arrays */
videos = []
graphs = []

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


function parseDate(string) {
    return string
}

function GraphEntry(views,key) {
    var graphdata = []
    
    $.each(views, function(index,value) {
        
        points = new Array(2);        
        points[0] = parseDate(index);
        points[1] = parseInt(value);
        
        graphdata.push(points);
        
    });
    
    console.log(graphdata);

    var d2 = [[1, 7], [1, 8], [3, 5]];

    console.log(d2);
    
    $(function () {
        $.plot($("#graph_"+key), [d2]);
    });       
}

// Creates Video Entry

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
    
    graphs[key] = new GraphEntry(val.views,key);
    
    // console.debug(val.info['url'])
    // console.debug(val.info['date_published'])
    // console.debug(val.info['title'])
    // console.debug(val.info['thumbs'])
    // console.debug(val.views);
    // console.debug(val.tags);
    
}