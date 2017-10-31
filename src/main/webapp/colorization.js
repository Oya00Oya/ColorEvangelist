/**
 * Created by ysyco on 2017/7/7.
 */


// cf. https://github.com/websanova/wPaint/blob/master/src/wPaint.js#L243
$.fn.wPaint.extend({
    getImageCanvas: function (withBg) { // getCanvas is bad name (conflict).
        var canvasSave = document.createElement('canvas'),
            ctxSave = canvasSave.getContext('2d');

        withBg = withBg === false ? false : true;

        $(canvasSave)
            .css({display: 'none', position: 'absolute', left: 0, top: 0})
            .attr('width', this.width)
            .attr('height', this.height);

        if (withBg) { ctxSave.drawImage(this.canvasBg, 0, 0); }
        ctxSave.drawImage(this.canvas, 0, 0);

        return canvasSave;
    }
});
//这个是用来延伸出那个canvas的画板的

$(function () {

    $('#img_pane').show(); // for $.fn.wPaint
    $('#wPaint').wPaint({
        path: '/wPaint/',
        menuOffsetLeft: 0,
        menuOffsetTop: -45
    });
    $('#img_pane').hide();

    $('#submit').click(function () {
        if (!$('#colorization-ref').attr('src')) {
            alert('select a file');
        } else {
            colorize();
        }
    });

    $('#load_file_colorization').on('change', function (e) {
        var file = e.target.files[0];
        if (file.type.indexOf('image') < 0) {
            console.log("not a pic!!!")
            return false;
        }

        set_file(file);
    });
//改变背景的图片
    $('#colorization-ref').load(function () {
        $('#wPaint')
            .width($('#colorization-ref').width())
            .height($('#colorization-ref').height())
            .wPaint('resize');
        colorize(); // update image_id
    });
//这个load不是ajax的，是jQuery的load当背景加载完成后，运行该函数，应该与设定画板的大小有关

    //--- functions
    function post(input_data) {

        $.ajax({
            t1:0,
            type: 'POST',
            url: '/upload/colorization.do',
            data: input_data,//这个data是发到服务器的数据
            cache: false,
            contentType: false,
            processData: false,//false表示不想被转化为对象
            dataType: 'text', // server response is broken//返回纯文本字符串
            beforeSend: function () {//在发送请求前修改XMLHttpRequest对象的函数
                $('#painting_status').attr('class', '').text('NOW UPLOADING ...').show();//给对应id的span元素的class元素的值修
                // 改为空（不知为什么要空的class），添加文本
                $('#submit').prop('disabled', true);//取消提交按钮的disable属性
                console.log('coloring start');
            },
            success: function(outputFileName, textStatus) {//请求成功后调用的回调函数
                console.log('uploaded:'+outputFileName);
                $('#output_colorization').attr('src', ''+ 'func/output/colorization/'+outputFileName).show();
                $('#painting_status').hide();
            },
            error: function () {//失败
                $('#painting_status').attr('class', 'text-error').text('UPLOAD ERROR').show();
                $('#submit').prop('disabled', false);
            },
            complete: function () {//不管失败还是成功都回调用的
                $('#submit').prop('disabled', false);//复原
                console.log('post finish');
            }
        });
    }
//用于与服务器进行数据交流

//这个应该是获取到返回的输出图片
    function blobUrlToBlob(url, fn) {
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            fn(xhr.response);
        };
        xhr.open('GET', url);//初始化http请求参数但是并不发起请求
        xhr.responseType = 'blob';
        //在Ajax操作中，如果xhr.responseType设为blob，接收的就是二进制数据
        xhr.send();
        //发送 HTTP 请求，使用传递给 open() 方法的参数，以及传递给该方法的可选请求体
    }

    function colorize() {
        $('#wPaint').wPaint('imageCanvas').toBlob(function (ref_blob) {
            var ajaxData = new FormData();
            ajaxData.append('ref', ref_blob);
            blobUrlToBlob($('#colorization-ref').attr('src'), function (line_blob) {
                ajaxData.append('line', line_blob);
                post(ajaxData);
            });
        });
    }

    function set_file(file) {
        console.log('set file');
        $('#img_pane').show('fast', function () {
            //先重设wpaint大小，避免图片越变越小
            $('#wPaint')
                .css("width","100%")
                .wPaint('resize');
            $('#colorization-ref').attr('src', window.URL.createObjectURL(file));
        });
    }
});
