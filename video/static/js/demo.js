function video_request(filename) {
    // console.log("filename",filename);
    $.ajax({
        url:"video_request",
        type:'POST',
        data: {'file':filename},
        dataType:'json',
        success: function(data) {
            // console.log(data);
            var url='/static/'+data['url'];
            //change the whole object to refresh the video
            var video = document.getElementById("video");
            var html_str="<video id='my-video' width='700' height='500' controls='controls'>";
            html_str+="<source id='v1' src="+url+" type='video/mp4'>";
            html_str+="<object id='v2' data="+url+" >";
            html_str+="<embed id='v3' src="+url+" />";
            html_str+="</object>";
            html_str+="</video>";
            html_str+="<canvas id='myCanvas' class='mycanvas'></canvas>"
            // console.log(html_str);
            video.innerHTML=html_str; 
            paint(data['proposals'],data['duration']);

        }
    }); 
}

var pt=0;
var colors=['red','orange','green','blue'];
function get_color() {
    if (pt==colors.length) {
        pt=0;
    }
    return colors[pt++];
}

function paint(proposals,duration){
    pt=0;
    // console.log(proposals,duration);
    var width=425;
    var height=400;
    var span=25;
    $('#myCanvas').attr('width',width);
    $('#myCanvas').attr('height',height);
    var canvas=document.getElementById('myCanvas');
    var context=canvas.getContext('2d');
    var color='black';
    var X1=0;
    var X2=width;
    var Y=span; 
    context.strokeStyle = color; 
    context.lineWidth=5;
    context.beginPath();
    context.moveTo(X1,Y);
    context.lineTo(X2,Y); 
    context.stroke();  
    console.log(X1,X2,Y,color);
    for(var i=0;i<proposals.length;i++){
        Y+=span;
        X1=proposals[i]['start_time']/duration*width;
        X2=proposals[i]['end_time']/duration*width;
        color=get_color();
        console.log(X1,X2,Y,color);
        context.beginPath();
        context.strokeStyle=color;
        context.lineWidth=5;
        context.moveTo(X1,Y);
        context.lineTo(X2,Y);
        context.stroke(); 
        context.font="15px Georgia";
        context.fillText(proposals[i]['annotation'],X1+10,Y-5);
    }
    $("#myCanvas").click(function(e){
        var x=Math.floor(e.pageX-$("#myCanvas").offset().left);
        var y=Math.floor(e.pageY-$("#myCanvas").offset().top);
        console.log(x,y);
        var idx=-1;
        idx=Math.floor(y/(span+5));
        console.log("idx",idx);
        myVid=document.getElementById("my-video");
        if (idx==0) {
            myVid.currentTime=0;
        }else{
            myVid.currentTime=proposals[idx-1]['start_time'];
        }
        myVid.play();  
    });
}
