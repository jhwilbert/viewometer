/* Arrays */
videos = [];
graphs = [];
allVideos = [];
allLabels = [];
arrObj = [];

$(document).ready(function(){
    
    $(document.createElement("div")).attr("id","allgraphs").appendTo("#container").css("width","960px").css("height","540px");
    
    $.getJSON(jsonPath, function(data) {
        dataObjects = data[searchTerm]
        
        // Create Objects
         $.each(dataObjects, function(key, val) {        
                videos[key] = new VideoEntry(key,val);
        });
    
        // Graph Plotting
        var plot = $.plot($("#allgraphs"), arrObj, {
                   series: {
                        lines: { show: true }, points: { show: true } },
                         grid: { hoverable: true, clickable: true },
                         xaxis: { mode: "time", timeformat: "%b %d <br> %H:%M",
                     }
         });
        $(".legend").hide();
         
         // Graph Behaviour
         $("#allgraphs").bind("plotclick", function (event, pos, item) {
             if (item) {
                 items = $("div:contains('"+item.series.label+"')");
                 item = items[items.length-1];
                 $.scrollTo(item,800);
                 $(item.nextSibling).removeClass("off").addClass("on"); 
             }
         });
                 

    });
});

/* Creates Video Entry */
function VideoEntry(key,val) {

        // Create Video Elements (parent)
        $(document.createElement("div")).attr("id","video_"+key).appendTo("#container").addClass("span-24 video")

        $(document.createElement("a")).attr("name","video_"+key).appendTo("#video_"+key).attr("id","video_"+key)

        // Create Title  (child)
        $(document.createElement("div")).attr("id","title_"+key).appendTo("#video_"+key).html(val.info['title']).addClass("title");
        
        // Create Content
        $(document.createElement("div")).attr("id","content_"+key).appendTo("#video_"+key).addClass("off");
            
        // Create Image  (child)
        $(document.createElement("img")).attr({ src: val.info['thumbs'] }).attr("id","img_"+key).appendTo("#title_"+key).addClass("thumb");
        
         // Create URL  (child)
        $(document.createElement("div")).attr("id","url_"+key).appendTo("#title_"+key).html("<a href="+val.info['url']+">" + val.info['url']+"</a>").addClass("link");
        
         // Create Date  (child)
        $(document.createElement("div")).attr("id","date_"+key).appendTo("#title_"+key).html(val.info['date_published']).addClass("published");
               
        $(document.createElement("div")).attr("id","graph_"+key).appendTo("#content_"+key).addClass("graph").css("width","900px").css("height","240px");
        
        graphs[key] = new GraphEntry(val.data,key,val.info['title']);


        // Behaviour    
        $("#title_"+key).click(function() {
            if($("#content_"+key).hasClass('on')) {
                $("#content_"+key).removeClass("on").addClass("off");
            } else if($("#content_"+key).hasClass('off')){
                $("#content_"+key).removeClass("off").addClass("on");                    
            }    
        });
}


/* Creates Graph For Video Entry */

function GraphEntry(views,key,label) { 
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
