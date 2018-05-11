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
            var html_str="<video id='my-video' width='600' height='400' controls='controls'>";
            html_str+="<source id='v1' src="+url+" type='video/mp4'>";
            html_str+="<object id='v2' data="+url+" >";
            html_str+="<embed id='v3' src="+url+" />";
            html_str+="</object>";
            html_str+="</video>";
            html_str+="<div class='span8' align='center'><label id='title' >"+data['name']+"  </label> </div>";
            html_str+="<canvas id='myCanvas' class='mycanvas'></canvas>"
            // console.log(html_str);
            video.innerHTML=html_str; 
            paint(data);

        }
    }); 
}

// var pt=0;
// var colors=['red','green'];
// function get_color() {
//     if (pt==colors.length) {
//         pt=0;
//     }
//     return colors[pt++];
// }

function paint(data){
    var proposals=data['proposals'];
    var predicts=data['predicts'];
    var duration=data['duration'];
    pt=0;
    var width=400;
    var height=600;
    var span=25;
    var lines_y= new Array();
    $('#myCanvas').attr('width',600);
    $('#myCanvas').attr('height',height);
    var canvas=document.getElementById('myCanvas');
    var context=canvas.getContext('2d');
    var color='black';
    var X1=0;
    var X2=width;
    var Y=span; 
    lines_y.push(Y);
    context.strokeStyle = color; 
    context.lineWidth=5;
    context.beginPath();
    context.moveTo(X1,Y);
    context.lineTo(X2,Y); 
    context.stroke();  
    // console.log(X1,X2,Y,color);
    for(var i=0;i<proposals.length;i++){
        Y+=span;
        X1=proposals[i]['start_time']/duration*width;
        X2=proposals[i]['end_time']/duration*width;
        color="red";
        lines_y.push(Y);
        context.beginPath();
        context.strokeStyle=color;
        context.lineWidth=5;
        context.moveTo(X1,Y);
        context.lineTo(X2,Y);
        context.stroke(); 
        context.font="15px Georgia";
        // context.fillText(proposals[i]['annotation'],X1+10,Y-5);
    }
    
    console.log(predicts);
    for(var i=0;i<predicts.length;i++){
        Y+=span;
        X1=predicts[i]['start_time']/duration*width;
        X2=predicts[i]['end_time']/duration*width;
        color="green";
        console.log(X1,X2,Y,color);
        lines_y.push(Y);
        context.beginPath();
        context.strokeStyle=color;
        context.lineWidth=5;
        context.moveTo(X1,Y);
        context.lineTo(X2,Y);
        context.stroke(); 
        context.font="15px Georgia";
        // context.fillText(proposals[i]['annotation'],X1+10,Y-5);
    }
    console.log(lines_y);
    //find the nearest line
    $("#myCanvas").click(function(e){
        var y=Math.floor(e.pageY-$("#myCanvas").offset().top);
        var min=999;
        var idx=-1;
        console.log(y);
        for (var i = lines_y.length - 1; i >= 0; i--) {
            if(Math.abs(lines_y[i]-y)<min){
                idx=i;
                min=Math.abs(lines_y[i]-y);
            }
        }
        console.log("idx",idx);
        myVid=document.getElementById("my-video");
        //show annotation
        if (idx!=0) {
            // alert(proposals[idx-1]['annotation']);
            if(idx<=proposals.length)
                $("#annotation").val(proposals[idx-1]['annotation']);
            else
                $("#caption").val(predicts[idx-1-proposals.length]['annotation']);
        }  
        //switch of clip
        if (idx==0) {
            myVid.currentTime=0;
        }else{
            if(idx<=proposals.length)
                myVid.currentTime=proposals[idx-1]['start_time'];
            else
                myVid.currentTime=predicts[idx-1-proposals.length]['start_time'];
                $("#caption").val(predicts[idx-1-proposals.length]['annotation']);
        
        }
        myVid.play();  
    });
    // $("#myCanvas").dblclick(function(e){
    //     var y=Math.floor(e.pageY-$("#myCanvas").offset().top);
    //     var min=999;
    //     var idx=-1;
    //     console.log(y);
    //     for (var i = lines_y.length - 1; i >= 0; i--) {
    //         if(Math.abs(lines_y[i]-y)<min){
    //             idx=i;
    //             min=Math.abs(lines_y[i]-y);
    //         }
    //     }
    //     console.log("idx",idx);
    //     if (idx!=0) {
    //         // alert(proposals[idx-1]['annotation']);
    //         $("#annotation").val(proposals[idx-1]['annotation']);
    //     }
    // });
}
