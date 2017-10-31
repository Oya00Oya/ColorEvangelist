<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PaintsPytorch</title>

    <!-- Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">

    <!--自己的样式文件 -->
    <link href="mystyle.css" rel="stylesheet">
    <!-- font-awesome -->
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <!--////////////////////////////////////////////////////////////////////////////////////////;-->
    <!-- Canvas toBlob polyfill -->
    <script src="https://cdn.bootcss.com/javascript-canvas-to-blob/3.6.0/js/canvas-to-blob.min.js"></script>
    <!-- jQuery -->
    <script src="https://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"></script>
    <script src="ajaxfileupload.js"></script>
    <!-- jQuery Cookie -->
    <script src="https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
    <!-- jQuery UI -->
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
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
<nav class="navbar navbar-default navbar-static-top navbar-fixed-top" role="navigation">
    <div class="container-fluid">
        <div class="navbar-header nav-title">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <span class="navbar-brand">
                <img src="imgs/search_cat_128px_1141878_easyicon.net.png" style=" display: inline;width: 24px">
                <a href="index.jsp">PaintsPytorch</a>
                <a href="deblur.html">Deblur</a>
            </span>
        </div>
        <div class="collapse navbar-collapse navbar-right is-collapse">
            <ul class="nav navbar-nav">
                <li><a href="#intro">Introduction</a></li>
                <li><a href="#howto">How to</a></li>
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
</nav><!--nav-->
<div class="jumbotron" id="intro">
    <div class="container">
        <h1>Welcome to use PaintsPytorch</h1>
        <hr>
        <p> It automatically applies the semantic features of an existing painting to an unfinished sketch.</p>
        <p>Two different functions can provide you with magical colouring experience!</p>
        <a href="#start">
            <button class="btn btn-primary btn-lg " id="IntroHD">START NOW!!!</button>
        </a>
    </div>
</div><!--onepage-->
<div class="twopage" id="fourp">
    <div class="container" style="width: 70%">
        <div class="twopagetext">
            <h1>Gallery</h1>
            <P>Different style of paintting can be made with this method </P>
        </div>
        <div style="margin: 0 auto">
            <div id="carousel-example-grneric" class="carousel slide" data-interval="3000" style="height: 350px;"
                 data-ride="carousel">
                <ol class="carousel-indicators" style="margin-top: 200px">
                    <li data-target="#carousel-example-grneric" data-slide="1" class="active"></li>
                    <li data-target="#carousel-example-grneric" data-slide="2" class=""></li>
                    <li data-target="#carousel-example-grneric" data-slide="3" class=""></li>
                </ol>
                <div class="carousel-inner" role="listbox">
                    <div class="item active">
                        <div class="row">
                            <div class="piccc">
                                <img class="col-md-6  hidden-xs" src="imgs/rem.jpg" style="position: relative;"/>
                                <img class="col-md-6 visible-xs-block" src="imgs/remb.jpg" style="position: relative;"/>
                            </div>
                        </div>
                        <div class="carousel-caption">
                            <h1>Rem</h1>
                            <p>Easy to get different style of Rem</p>
                            <a href="#" class="btn btn-lg btn-primary" role="button">Try now!!!</a>
                        </div>
                    </div>
                    <div class="item ">
                        <div class="row">
                            <div class="piccc">
                                <img class="col-md-6 hidden-xs" src="imgs/mikunnnnn.jpg" style="position: relative;"/>
                                <img class="col-md-6 visible-xs-block" src="imgs/mikunnnnnb.jpg"
                                     style="position: relative;"/>
                            </div>
                        </div>
                        <div class="carousel-caption">
                            <h1>Hatsune Miku</h1>
                            <p>Easy to get Pink Miku, Snow Miku or others</p>
                            <a href="#" class="btn btn-lg btn-primary" role="button">Try now!!!</a>
                        </div>
                    </div>
                    <div class="item ">
                        <div class="row">
                            <div class="piccc">
                                <img class="col-md-6 hidden-xs" src="imgs/megumin04.jpg" style="position: relative;"/>
                                <img class="col-md-6 visible-xs-block" src="imgs/migumin04b.jpg"
                                     style="position: relative;"/>
                            </div>
                        </div>
                        <div class="carousel-caption">
                            <h1>Other characters</h1>
                            <p>Also easy to create other characters,even your original.</p>
                            <a href="#" class="btn btn-lg btn-primary" role="button">Try now!!!</a>
                        </div>
                    </div>
                </div>
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
<div class="threepage well" id="howto">
    <div class="container">
        <h3>How to</h3>
        <ul id="myTab" class="nav nav-tabs">
            <li class="active"><a href="#step1" data-toggle="tab">Step1</a></li>
            <li><a href="#step2" data-toggle="tab">Step2</a></li>
            <li><a href="#step3" data-toggle="tab">Step3</a></li>
        </ul>
        <div id="myTabcontent" class="tab-content">
            <div class="tab-pane fade in active" id="step1">
                <div>
                    <h1>Step 1</h1>
                    <p>
                        Please read the introduction First.
                        <br>
                        It will automatically colour after selecting the sketch.
                    </p>
                </div>
                <div>
                    <img src="imgs/delivery_cat_72px_1141867_easyicon.net.png" height="72" width="72"/></div>
                <div>

                </div>
            </div>
            <div class="tab-pane fade" id="step2">
                <div>
                    <h1>Step 2</h1>
                    <P>
                        You can choose colors from the palette to add color prompt colors to the sketch.
                        <br>
                    </P>
                </div>
                <div>
                    <img src="imgs/phone_cat_72px_1141875_easyicon.net.png" height="72" width="72"/></div>
            </div>
            <div class="tab-pane fade" id="step3">
                <div>
                    <h1>Step 3</h1>
                    <P>
                        Click the 'colorize' button,if you want to colour again.
                        <br>
                    </P>
                </div>
                <div>
                    <img src="imgs/review_cat_72px_1141877_easyicon.net.png" height="72" width="72"/></div>
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
                    <img id="output_sketch" style="max-width:100%;margin-top: 34px" src="" alt="You will get your Picture here.">
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
                <p style="color: white">©2017 PaintsTorch <a href="#" target="_blank" title="">-- QiStudio</a></p>
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