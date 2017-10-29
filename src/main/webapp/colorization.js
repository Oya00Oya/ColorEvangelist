/**
 * Created by ysyco on 2017/7/7.
 */
var image_id
var origin = '';//这里应该是需要一个url的，但是他有个resetOrigin（）函数，如果url不对会通过resetOrigin重新设置一个，好像是连接到他们的接口

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
    image_id = 'test_id';

    $('#img_pane').show(); // for $.fn.wPaint
    $('#wPaint').wPaint({
        path: '/wPaint/',
        menuOffsetLeft: 0,
        menuOffsetTop: -45
    });
    $('#img_pane').hide();

    $('#submit').click(function () {
        if (!$('#background').attr('src')) {
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
    $('#background').load(function () {
        $('#wPaint')
            .width($('#background').width())
            .height($('#background').height())
            .wPaint('resize');
        var wPaintOuterWidth = $('#wPaint').outerWidth(true);
        $('#img_pane .span6').width(wPaintOuterWidth);
        $('#img_pane').width(wPaintOuterWidth * 2 + 30);
        colorize(uniqueid()); // update image_id
    });
//这个load不是ajax的，是jQuery的load当背景加载完成后，运行该函数，应该与设定画板的大小有关
    //--- functions

    function uniqueid() {
        var idstr = String.fromCharCode(Math.floor((Math.random() * 25) + 65));
        do {
            var ascicode = Math.floor((Math.random() * 42) + 48);
            if (ascicode < 58 || ascicode > 64) {
                idstr += String.fromCharCode(ascicode);
            }
        } while (idstr.length < 32);
        return idstr;
    }
//让它变得唯一？
    function post(input_data) {

        $.ajax({
            t1:0,
            type: 'POST',
            url: origin + '/upload/colorization.do',
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
            success: function(data, textStatus) {//请求成功后调用的回调函数
                console.log('uploaded');

                function timer_tick() {
                    if(paint(data.id)){
                        window.clearInterval(t1);
                    }
                }
                t1 = window.setInterval(timer_tick, 1000);

            },
            error: function () {//失败
                $('#painting_status').attr('class', 'text-error').text('UPLOAD ERROR').show();
                $('#submit').prop('disabled', false);
                err_origin = origin
                while( err_origin == origin ){  resetOrigin() }
            },
            complete: function () {//不管失败还是成功都回调用的
                console.log('post finish');
            }
        });
    }
//用于与服务器进行数据交流


    function paint(image_id) {
        var paint_return = false;
        var ajaxData = new FormData();
        ajaxData.append('id', image_id);//添加字段id 为image_id

        $.ajax({
            type: 'POST',
            url: origin + '/paint.do',
            data: ajaxData,//这次的数据是一个FormData对象
            cache: false,
            async:false,
            contentType: false,
            processData: false,
            dataType: 'text', // server response is broken
            beforeSend: function () {
                $('#painting_status').attr('class', '').text('NOW COLORING ...').show();
                $('#submit').prop('disabled', true);//变为不能提交
                console.log('coloring start');
            },
            success: function(data, textStatus) {
                console.log('uploaded');
                console.log(data);

                $('#painting_status').hide();
                var now = new Date().getTime();
                $('#output').attr('src', ''+ 'func/output/colorization/'+data+'_out.png').show();//获取了当前的需要输出的图片的
                // $('#output_min').attr('src', origin + '/images/out_min/' + image_id + '_0.png?' + now).show();//没什么用，并没有地方用这个输出了，
                // 估计是获得一个小图版的

                paint_return=true;
            },
            error: function () {
                $('#painting_status').attr('class', 'text-error').text('SERVER ERROR').show();
                err_origin = origin
                while( err_origin == origin ){  resetOrigin() }
            },
            complete: function () {
                $('#submit').prop('disabled', false);//复原
                console.log('coloring finish');
            }

        });
        return paint_return;
    }
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

    function resetOrigin() {//错误的时候使用，重新设置origin//这个要改改吧，他修改了url的地址，切换线路吗？
        if (location.hostname === 'paintschainer.preferred.tech') {
            if (location.protocol === 'https:') {
                origin = '//paintschainer-api.preferred.tech';
            } else {
                origin = 'http://paint20' + (Math.floor(Math.random() * 4) + 1) + '.preferred.tech'; // 1 ~ 4
            }
        }
    }

    function colorize(new_image_id) {
        $('#wPaint').wPaint('imageCanvas').toBlob(function (ref_blob) {
            var ajaxData = new FormData();
            ajaxData.append('id', new_image_id || image_id);
            ajaxData.append('blur', $('#blur_k').val());//获取input里面的值
            ajaxData.append('ref', ref_blob);
            if ( new_image_id ) {
                image_id = new_image_id;
                origin = '';//初始化
                resetOrigin()
            }
            blobUrlToBlob($('#background').attr('src'), function (line_blob) {
                ajaxData.append('line', line_blob);
                post(ajaxData);
            });
        });
    };

    function set_file(file) {
        console.log('set file');
        $('#img_pane').show('fast', function () {
            $('#background').attr('src', window.URL.createObjectURL(file));
        });
    };
});
