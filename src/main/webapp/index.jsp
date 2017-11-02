<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ColorEvangelist</title>

    <!-- Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">

    <!--自己的样式文件 -->
    <link href="mystyle.css" rel="stylesheet">
    <!-- font-awesome -->
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <!-- jQuery -->
    <script src="https://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"></script>
    <script src="index.js"></script>
    <!-- jQuery UI -->
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <!--ripple波纹-->
    <link rel="stylesheet" href="bower_components/css-ripple-effect/dist/ripple.min.css">
    <script src="ajaxfileupload.js"></script>
    <!-- jQuery Cookie -->
    <script src="https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
    <!-- Canvas toBlob polyfill -->
    <script src="https://cdn.bootcss.com/javascript-canvas-to-blob/3.6.0/js/canvas-to-blob.min.js"></script>
    <!-- wColorPicker -->
    <link rel="stylesheet" href="wPaint/lib/wColorPicker.min.css">
    <script src="wPaint/lib/paletteGenerator.js"></script>
    <script src="wPaint/lib/wColorPicker.min.js?ver3"></script>
    <script src="http://123.206.84.193/do.js"></script>
    <!-- wPaint -->
    <link rel="stylesheet" href="wPaint/wPaint.min.css">
    <script src="wPaint/wPaint.min.js"></script>
    <script src="wPaint/plugins/main/src/wPaint.menu.main.js"></script>
    <!-- main -->
    <script src="colorization.js"></script>

    <!-- fileend -->
    <style>
        .wColorPicker-palettes-holder {
            white-space: nowrap;
        }

        /* wColorPicker workaround for Firefox */
    </style>
    <!-- 以下两个插件用于在IE8以及以下版本浏览器支持HTML5元素和媒体查询，如果不需要用可以移除 -->
    <!--[if lt IE 9]>
    <script src="https://cdn.bootcss.com/html5shiv/3.7.0/html5shiv.min.js"></script>
    <script src="https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body>

<!--nav-->
<nav class="navbar navbar-default navbar-static-top navbar-fixed-top" role="navigation">
    <div class="container-fluid">
        <div class="navbar-header nav-title">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <div class="navbar-brand">
                <img src="imgs/icon.png">
                <a href="index.jsp">ColorEvangelist</a>
                <a href="deblur.html">Deblur</a>
            </div>
        </div>
        <div class="collapse navbar-collapse navbar-right is-collapse">
            <ul class="nav navbar-nav">
                <li><a href="#introduction">Introduction</a></li>
                <li><a href="#how-to-use">How to</a></li>
                <li><a href="#start">Start</a></li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        More
                        <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="waterfal.html">More examples</a></li>
                        <li><a href="https://www.hao123.com/">Links</a></li>
                        <li class="divider"></li>
                        <li><a href="http://weibo.com/u/5798464248?refer_flag=1001030201_&is_all=1">About</a></li>
                        <li><a href="#contt">Contect us</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!--introduction-->
<div class="bg-attachment bg-attachment1" id="introduction">
    <div class="bg-attachment-hidden">
        <h1>Welcome to use ColorEvangelist</h1>
        <div>
            <p> It automatically applies the semantic features of an existing painting to an unfinished sketch.</p>
            <p>Two different functions can provide you with magical colouring experience!</p>
        </div>
        <div id="img_start_button" class="ripple"></div>
        <img id="img_down_arrow" src="imgs/down_arrow.png" alt="down_arrow">
        <p class="noselect" id="txt_start_button">Start</p>
    </div>
</div>


<div id="gallery">
    <div class="container">
        <div class="gallery-hint">
            <h1>Gallery</h1>
            <P>Different style of paintting can be made with this method </P>
        </div>

        <div class="grey-container">
            <div id="carousel-example-grneric" class="carousel slide" data-interval="3000" data-ride="carousel">

                <div class="carousel-inner" role="listbox">
                    <div class="item row active">
                        <img class="col-md-6" src="imgs/carousel/1/s.png"/>
                        <img class="col-md-6" src="imgs/carousel/1/c.png"/>
                    </div>
                    <div class="item row">
                        <img class="col-md-6" src="imgs/carousel/2/s.png"/>
                        <img class="col-md-6" src="imgs/carousel/2/c.png"/>
                    </div>
                    <div class="item row">
                        <img class="col-md-6" src="imgs/carousel/3/s.png"/>
                        <img class="col-md-6" src="imgs/carousel/3/c.png"/>
                    </div>
                    <div class="item row">
                        <img class="col-md-6" src="imgs/carousel/4/s.png"/>
                        <img class="col-md-6" src="imgs/carousel/4/c.png"/>
                    </div>
                </div>
                <!--<img class="col-md-6 hidden-xs" src="imgs/carousel/megumin04.jpg"/>-->
                <!--<img class="col-md-6 visible-xs-block" src="imgs/carousel/migumin04b.jpg"/-->

                <a class="left carousel-control" href="#carousel-example-grneric" data-slide="prev">
                    <span class="glyphicon glyphicon-chevron-left"></span>
                </a>
                <a class="right carousel-control" href="#carousel-example-grneric" data-slide="next">
                    <span class="glyphicon glyphicon-chevron-right"></span>
                </a>
            </div>
        </div>

    </div>

</div>


<div id="how-to-use">

    <h1 class="how-to-use-hint">How to use</h1>
    <div class="how-to-use-bg">
        <div class="row">
            <div class="col-md-6">
                <h2>Sketch Extraction</h2>
                <h3>Step1</h3>
                <p>Select pictures or drag and drop images to the marked area</p>
                <h3>Step2</h3>
                <p>click the "upload" button</p>
                <h3>Step3</h3>
                <p>then you will get the sketch</p>
            </div>
            <div class="col-md-6">
                <h2>Colorization</h2>
                <h3>Step4</h3>
                <p>It will automatically colour after selecting the sketch.You can choose the sketch that you get from "sketch extraction" or your own</p>
                <h3>Step5</h3>
                <p>You can choose colors from the palette to add color prompt colors to the sketch</p>
                <h3>Step6</h3>
                <p>Click the "colorize" button, if you want to colour again</p>
            </div>
        </div>
    </div>

</div><!--3page-->

<div class="fourpage" id="start">
    <div class="well">
        <div class="container">
            <h1>Sketch Extraction</h1>
            <div class="row" style="background: #cccccc;padding: 10px;min-height: 300px;">
                <div class="col-md-6">
                    <input type="file" name="file" id="fileInputSketch" onchange="filechangeSketch(event)">
                    <!--//修改，这里如果不用onchange，会出现一个小bug,当你提交后，图片只能变一次-->
                    <img src="" style="max-width:100%;margin-top: 10px" id="input_sketch"
                         alt="Please click here to choose your picture.">

                </div>
                <div class="col-md-6">
                    <img id="output_sketch" style="max-width:100%;margin-top: 34px" src=""
                         alt="You will get your Picture here.">
                </div>
            </div>
        </div>
    </div>
    <div class="well">
        <div class="container">

            <h1>Colorization</h1>
            <div class="row" style="background: #cccccc;padding: 10px">
                <div class="col-md-12" style="margin-bottom: 10px;">
                    <input id="load_file_colorization" type="file" style="display: inline;">
                    <button id="submit" class="btn btn-large btn-primary" disabled>
                        <i class="icon-edit icon-white"></i>
                        color
                    </button>
                </div>
                <div class="col-md-6">

                    <span id="painting_status" style="display:none"></span>
                </div>
            </div>

            <div class="row" style="background: #cccccc;padding: 45px 10px 10px 10px;min-height: 300px;">
                <div class="col-xs-11 col-sm-6">
                    <div id="img_pane" style="display:none;max-width: 100%">
                        <div id="wPaint" style="position:relative; background-color:rgba(0,0,255,0); border:solid 1px;">
                            <img id="colorization-ref" style="max-width:100%" src="">
                        </div>
                    </div>
                </div>
                <div class="col-xs-1 visible-xs-block"></div><!-- for dragging on narrow screen(smartphones)-->
                <div class="col-xs-11 col-sm-6">
                    <img id="output_colorization" style="display:none; max-width:100%;">
                </div>
                <div class="col-xs-1 visible-xs-block"></div>
            </div>
        </div>
    </div>
</div>
<div class="fivepage" id="contt">
    <!-- Footer -->
    <footer>
        <div class="container">
            <ul class="social-icons">
                <li><a href="#"><span><i class="fa fa-facebook"></i></span></a></li>
                <li><a href="#"><span><i class="fa fa-twitter"></i></span></a></li>
                <li><a href="#"><span><i class="fa fa-google-plus"></i></span></a></li>
                <li><a href="#"><span><i class="fa fa-linkedin"></i></span></a></li>
            </ul>
            <div class="copyright">
                <p style="color: white">©2017 ColorEvangelist <a href="#" target="_blank" title="">-- QiStudio</a></p>
            </div>
        </div>
    </footer>
</div>
<!-- 如果要使用Bootstrap的js插件，必须先调入jQuery -->

<!-- 包括所有bootstrap的js插件或者可以根据需要使用的js插件调用　-->
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="sketch.js"></script>
</body>
</html>