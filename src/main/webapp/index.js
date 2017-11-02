//首屏自适应高度
$(window).on("load resize", function () {
    var h = window.innerHeight || document.body.clientHeight || document.documentElement.clientHeight;
    $(".bg-attachment1 .bg-attachment-hidden").css("height", h);
});

$(document).ready(function () {
    var scrll_to_start = function () {
        $('html,body').animate({scrollTop: $('#start').offset().top}, 800);
    };
    //start按钮滚动到指定位置
    var $img_start_button = $("#img_start_button");
    var $txt_start_button = $("#txt_start_button");

    $img_start_button.click(scrll_to_start);
    $txt_start_button.click(scrll_to_start);
    $("#img_down_arrow").click(scrll_to_start);


    //start button hover
    var img_start_button_hover = function () {
        $img_start_button.css("background","url(imgs/start_button_hover.png) no-repeat center center");
        $img_start_button.css("background-size","95% 95%");
    };

    var img_start_button_hover_out = function () {
        $img_start_button.css("background","url(imgs/start_button.png) no-repeat center center");
        $img_start_button.css("background-size","95% 95%");
    };
    $img_start_button.hover(img_start_button_hover,img_start_button_hover_out);
    $txt_start_button.hover(img_start_button_hover,img_start_button_hover_out);
});