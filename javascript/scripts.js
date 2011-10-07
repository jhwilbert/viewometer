/* Variables */
urlLocal = "http://localhost:8082/output/display_videos"
urlRemote = "http://viewometer.appspot.com/output/display_videos"

/* Arrays */
videos = []
graphs = []
allVideos = []


$(document).ready(function(){
    
    $(document.createElement("div")).attr("id","allgraphs").appendTo("#container").css("width","900px").css("height","240px");
    
    
    $.getJSON(urlLocal, function(data) {
    	$.each(data, function(key, val) {
            videos[key] = new VideoEntry(key,val);
    	});
        
        
        var options = {
          xaxis: {
              mode: "time",
              timeformat: "%b %d <br> %H:%M",
          }
        }
            	
    	$.plot($("#allgraphs"), allVideos,options );
    });

});

/* Creates Video Entry */

function VideoEntry(key,val) {
    
    // Create Video Elements (parent)
    $(document.createElement("div")).attr("id","video_"+key).appendTo("#container").addClass("span-24 border video");
    
    // Create Image  (child)
    $(document.createElement("img")).attr({ src: val.info['thumbs'] }).attr("id","img_"+key).appendTo("#video_"+key).addClass("thumb");
    
    // Create Title  (child)
    $(document.createElement("div")).attr("id","title_"+key).appendTo("#video_"+key).html(val.info['title']).addClass("title");
    
     // Create Date  (child)
    $(document.createElement("div")).attr("id","date_"+key).appendTo("#video_"+key).html("Published on:" + val.info['date_published']).addClass("published");
    
     // Create URL  (child)
    $(document.createElement("div")).attr("id","url_"+key).appendTo("#video_"+key).html("<a href="+val.info['url']+">" + val.info['url']+"</a>").addClass("link");
           
    $(document.createElement("div")).attr("id","graph_"+key).appendTo("#video_"+key).addClass("graph").css("width","900px").css("height","240px");
    
    graphs[key] = new GraphEntry(val.data,key);



}

/* Creates Graph For Video Entry */

function GraphEntry(views,key) { 
    var graphdata = []
 
     $.each(views, function(index,value) {         

                  points = new Array(2);        
                  points[0] = parseDate(value.datetime).getTime();
                  points[1] = parseInt(value.views);      
                  graphdata.push(points);

          });
     
     var options = {
       xaxis: {
           mode: "time",
           timeformat: "%b %d <br> %H:%M",
       }
     }
     
     $(function () {
         $.plot($("#graph_"+key), [graphdata], options);
     });
     
     allVideos.push(graphdata);
}


/* Helper Functions */

function parseDate(string) {
    string = string.split("T")
    stringTime = string[1]
    stringDate = string[0]
    
    stringTime = stringTime.split(":")
    stringDate = stringDate.split("-")
    
      
    return new Date(stringDate[0], stringDate[1], stringDate[2], stringTime[0], stringTime[1])
}
