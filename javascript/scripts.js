/* Variables */
urlLocal = "http://localhost:8080/output/display_videos"
urlRemote = "http://viewometer.appspot.com/output/display_videos"

/* Arrays */
videos = []
graphs = []
allVideos = []
allLabels = []

$(document).ready(function(){
    
    $(document.createElement("div")).attr("id","allgraphs").appendTo("#container").css("width","960px").css("height","840px");
    
    
    $.getJSON(urlLocal, function(data) {
    	$.each(data, function(key, val) {
            videos[key] = new VideoEntry(key,val);
    	});


    var plot = $.plot($("#allgraphs"), arrObj, {
               series: {
                   lines: { show: true }, points: { show: true } },
               		grid: { hoverable: true, clickable: true },
        	   	   xaxis: { mode: "time", timeformat: "%b %d <br> %H:%M",
         		}
    	});
    	
    	var legend0 = $(".legend").children()[0];
    	var legend1 = $(".legend").children()[1];
		legend0.style.width = "150px";
		legend1.style.width = "150px";
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
    
    graphs[key] = new GraphEntry(val.data,key,val.info['title']);



}

arrObj = [];

/* Creates Graph For Video Entry */

function GraphEntry(views,key,label) { 
    var graphdata = []

 
     $.each(views, function(index,value) {         

                  points = new Array(2); 
                  //label = "title"+index;
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
     
     allLabels.push(label);
     allVideos.push(graphdata);
     
     object = { data: graphdata, label: label}
     
     arrObj.push(object);
   	
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
