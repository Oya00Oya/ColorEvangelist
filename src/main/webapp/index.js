//首屏自适应高度
var $window = $(window);
$window.on("load resize", function () {
    var h = window.innerHeight || document.body.clientHeight || document.documentElement.clientHeight;
    $(".bg-attachment1 .bg-attachment-hidden").css("height", h);
});

$window.on("load",function () {
    var scrll_to_start = function () {
        $('html,body').animate({scrollTop: $('#start').offset().top}, 800);
    };
    //start按钮滚动到指定位置
    $("#img_start_button").click(scrll_to_start);
    $("#txt_start_button").click(scrll_to_start);
    $("#img_down_arrow").click(scrll_to_start);
});
