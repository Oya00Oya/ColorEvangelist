$(window).on("load resize",function(){
    var h=window.innerHeight||document.body.clientHeight||document.documentElement.clientHeight;
    $(".bg-attachment1 .bg-attachment-hidden").css("height",h);
});
