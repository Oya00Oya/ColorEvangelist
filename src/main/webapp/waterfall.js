/**
 * Created by wwtliu on 14/9/5.
 */
    $(document).ready(function(){
        $(window).on("load",function(){
            imgLocation();
            //JSON字符串
            var dataImg = {"data":[{"src":"showbg1c.JPG"},{"src":"showbg2c.JPG"},
                {"src":"showbg3c.JPG"},{"src":"showbg4c.jpg"},{"src":"showbg5c.jpg"},{"src":"showbg6c.jpg"},{"src":"showbg7c.jpg"},{"src":"showbg8c.jpg"},{"src":"showbg9c.jpg"},{"src":"showbg10c.jpg"}]};
            window.onscroll = function(){
                if(scrollside()){
                    $.each(dataImg.data,function(index,value){
                        var box = $("<div>").addClass("box").appendTo($("#container"));
                        var content = $("<div>").addClass("content").appendTo(box);
                   console.log("./waterfallimgs/"+$(value).attr("src"));
                        $("<img>").attr("src","./waterfallimgs/"+$(value).attr("src")).appendTo(content);
                    });
                    imgLocation();
                }
            };
        });
    });

    function scrollside(){
        var box = $(".box");
        var lastboxHeight = box.last().get(0).offsetTop+Math.floor(box.last().height()/2);//获取最后的元素的高度，到加载到一半
        var documentHeight = $(document).width();
        var scrollHeight = $(window).scrollTop();//滚动的距离
        return (lastboxHeight<scrollHeight+documentHeight)?true:false;//
    }
    function imgLocation(){
        var box = $(".box");
        var boxWidth = box.eq(0).width();
        var num = Math.floor($(window).width()/boxWidth);
        var boxArr=[];
        box.each(function(index,value){
       console.log(index+"--"+value);
            var boxHeight = box.eq(index).height()+60;
            if(index<num){
                boxArr[index]= boxHeight;
           console.log(boxHeight);
            }else{
                var minboxHeight = Math.min.apply(null,boxArr);
           console.log(minboxHeight);
                var minboxIndex = $.inArray(minboxHeight,boxArr);
           console.log(minboxIndex);
           console.log(value);
                $(value).css({
                    "position":"absolute",
                    "top":minboxHeight,
                    "left":box.eq(minboxIndex).position().left
                });
                boxArr[minboxIndex]+=box.eq(index).height();
            }
        });
    }