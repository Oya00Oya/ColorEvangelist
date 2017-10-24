/**
 * Created by ysyco on 2017/7/4.
 */
//上传图片一
$("#img-change1").click(function () {
    $("#file1").click();
})
/*$("#file").change(function (event) {*/
var filechange1=function(event){
    var files = event.target.files, file;
    if (files && files.length > 0) {
        // 获取目前上传的文件
        file = files[0];// 文件大小校验的动作
        // if(file.size > 1024 * 1024 * 2) {
        //     alert('图片大小不能超过 2MB!');
        //     return false;
        // }
        // 获取 window 的 URL 工具
        var URL = window.URL || window.webkitURL;
        // 通过 file 生成目标 url
        var imgURL = URL.createObjectURL(file);
        //用attr将img的src属性改成获得的url
        $("#img-change1").attr("src",imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};



function post() {
    var post_return=false;
    $.ajaxFileUpload({
        url: '/imgUpload.do',
        fileElementId:'file1',//////////////////这个需要改吗
        dataType:'txt',
        secureuri : false,
        success: function (data){
            console.log(data)
            var t1;
            function timer_tick() {
                console.log("timer_tick");
                $.ajax({
                    url: 'http://localhost:8080/'+ 'output_sketch/'+data+'_out.png',
                    success: function () {
                        $('#output_sketch').attr('src', '/output_sketch/'+data+'_out.png').show();
                        window.clearInterval(t1);
                    }
                });
            }
            t1 = window.setInterval(timer_tick, 1000);
            post_return=true;
        },
        error:function(data,status,e){
            alert(e);
        }
    });
    return post_return;
}

$("#btn1").click(function () {
    post();
});
//上传图片3
$("#img-change2").click(function () {
    $("#file2").click();
})
/*$("#file").change(function (event) {*/
var filechange2=function(event){
    var files = event.target.files, file;
    if (files && files.length > 0) {
        // 获取目前上传的文件
        file = files[0];// 文件大小校验的动作
        // if(file.size > 1024 * 1024 * 2) {
        //     alert('图片大小不能超过 2MB!');
        //     return false;
        // }
        // 获取 window 的 URL 工具
        var URL = window.URL || window.webkitURL;
        // 通过 file 生成目标 url
        var imgURL = URL.createObjectURL(file);
        //用attr将img的src属性改成获得的url
        $("#img-change2").attr("src",imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};
$("#btn2").click(function () {
    $.AjaxFileUpload({
        url: '/imgUpload',
        fileElementId:'file2',
        dataType:'txt',
        secureuri : false,
        success: function (data){
            if(data=="yes"){
                $("#img-alert").css("display","block");
            }
        },
        error:function(data,status,e){
            alert(e);
        }
    });
});