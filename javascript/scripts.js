/* Variables */

urlLocal = "http://localhost:8082/output/display_videos"
urlRemote = "http://viewometer.appspot.com/output/display_videos"

/* Arrays */
videos = []
graphs = []

$(document).ready(function(){
	
    $.getJSON(urlLocal, function(data) {		
    	$.each(data, function(key, val) {
            
            videos[key] = new VideoEntry(key,val)
    	});
    });
    

	$('#search').submit(function() {
      
      return true;
    });
    
});


function parseDate(string) {
    string = string.split("T")
    stringTime = string[1]
    stringDate = string[0]
    
    stringTime = stringTime.split(":")
    stringDate = stringDate.split("-")
    
      
    return new Date(stringDate[0], stringDate[1], stringDate[2], stringTime[0], stringTime[1])
  }

function GraphEntry(views,key) {
    
    
    var graphdata = []
    
    //console.debug(parseDate("2011-10-05T14:32"));
    
    console.log(views);
         
     $.each(views, function(index,value) {
           
         $.each(value, function(index2,value2) {
            
        points = new Array(2);        
        points[0] = parseDate(index2).getTime();
        points[1] = parseInt(value2);
        
        graphdata.push(points);
        });
     });
    
     console.debug(graphdata)
     
     var d2 = graphdata
     
     console.log(graphdata)
     var options = {
       xaxis: {
           mode: "time",
           timeformat: "%b %d <br> %H:%M",          
           //minTickSize: [1, "day"]
       },
       yaxis: {
          min: 0,
          // max:10
       }
     }
     

     
     console.log(d2);
     
     
     $(function () {
         $.plot($("#graph_"+key), [d2], options);
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
           
    $(document.createElement("div")).attr("id","graph_"+key).appendTo("#video_"+key).addClass("graph").css("width","900px").css("height","240px");
    
    graphs[key] = new GraphEntry(val.views,key);
    
    // console.debug(val.info['url'])
    // console.debug(val.info['date_published'])
    // console.debug(val.info['title'])
    // console.debug(val.info['thumbs'])
    // console.debug(val.views);
    // console.debug(val.tags);
    
}