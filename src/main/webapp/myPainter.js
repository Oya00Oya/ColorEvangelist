var image_id; // for debug

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

// fix wPaint menu
['rectangle', 'ellipse', 'line', 'bucket', 'fillStyle', 'lineWidth'].forEach(function (name) {
  delete $.fn.wPaint.menus.main.items[name];
});

$(function () {
  // initialize wPaint
  var img_pane_visiblity = $('#img_pane').is(':visible');
  $('#img_pane').show();
  $('#wPaint').wPaint({
    path: '/wPaint/',
    menuHandle: false,
    menuOffsetLeft: 0,
    menuOffsetTop: -45,
    imageStretch: true
  });
  $('#img_pane').toggle(img_pane_visiblity);

  // upload image
  $('#load_line_file_top,#load_line_file').on('change', function (e) {
    var file = e.target.files[0];
    if (file.type.indexOf('image') < 0) {
      return false;
    }
    setImageFile(file);
  });

  // uploaded image
  $('#background').load(function () {
    $(window).resize();
    image_id = null; // reset image_id
    $('#submit').prop('disabled', false).click();
  });

  // start colorize
  $('#submit').click(function () {
    if (!$('#background').attr('src')) {
      alert('Select a image file');
    } else if (true || !image_id) { // If you set true, it will always upload
      image_id = uniqueid();
      uploadImage(image_id);
    } else {
      // Implement after support differential upload
    }
  });

  $(window).resize(function () {
    if (!$('#background').attr('src')) return;
    var $wPaint = $('#wPaint');
    var image = $wPaint.wPaint('image');
    $wPaint
      .width('auto').height('auto');
    $wPaint
      .width($('#background').width())
      .height($('#background').height())
      .wPaint('resize');
    $wPaint
      .wPaint('image', image, '', false, true);
  });

  // --- operations

  function setImageFile(file) {
    console.log('set file', file.name);
    $('#img_pane').show('fast', function () {
      $('#background').attr('src', window.URL.createObjectURL(file));
    });
  }

  function uploadImage(id) {
    var ajax_data = new FormData();
    ajax_data.append('id', id);
    ajax_data.append('blur', $('#blur_k').val());
    $('#wPaint').wPaint('imageCanvas').toBlob(function (ref_blob) {
      ajax_data.append('ref', ref_blob);
      blobUrlToBlob($('#background').attr('src'), function (line_blob) {
        ajax_data.append('line', line_blob);
        if (line_blob.size > 1000000) {
           alert('Image too large to colorize');
           return;
        }
        uploadImageToApiServer(ajax_data);
      });
    });
  }

  function colorImage(id) {
    var ajax_data = new FormData();
    ajax_data.append('id', id);
    colorImageToApiServer(ajax_data);
  }

  function uploadImageToApiServer(data) {
    $.ajax({
      type: 'POST',
      url: '//paintschainer-api.preferred.tech/v1/post',
      data: data,
      cache: false,
      contentType: false,
      processData: false,
      dataType: 'text', // server response is broken
      beforeSend: function () {
        console.log('upload start');
        $('#painting_status').attr('class', '').text('NOW UPLOADING ...').show();
        $('#submit').prop('disabled', true);
      },
      success: function () {
        console.log('uploaded');
        colorImage(image_id);
      },
      error: function () {
        console.log('upload failure');
        $('#painting_status').attr('class', 'text-error').text('UPLOAD ERROR').show();
        $('#submit').prop('disabled', false);
      },
      complete: function () {
        console.log('upload finish');
      }
    });
  }

  var PAINT_API_URLS = {
    tanpopo: '//paintschainer-api.preferred.tech/v1/paint/1',
    satsuki: '//paintschainer-api.preferred.tech/v1/paint/2'
  };

  function colorImageToApiServer(data) {
    $.ajax({
      type: 'POST',
      url: PAINT_API_URLS[$('#paint-mode input[name="mode"]:checked').val()],
      data: data,
      cache: false,
      contentType: false,
      processData: false,
      dataType: 'text', // server response is broken
      beforeSend: function () {
        console.log('colorize start');
        $('#painting_status').attr('class', '').text('NOW COLORING ...').show();
        $('#submit').prop('disabled', true);
      },
      success: function () {
        console.log('colorized');
        $('#painting_status').hide();
        var now = new Date().getTime();
        $('#output').attr('src', '//paintschainer-api.preferred.tech/images/out/' + image_id + '_0.jpg?' + now).show();
        $('#output_min').attr('src', '//paintschainer-api.preferred.tech/images/out_min/' + image_id + '_0.png?' + now).show();
      },
      error: function () {
        $('#painting_status').attr('class', 'text-error').text('SERVER ERROR').show();
      },
      complete: function () {
        $('#submit').prop('disabled', false);
        console.log('colorize finish');
      }
    });
  }

  // --- functions

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

  function blobUrlToBlob(url, fn) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
      fn(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
  }
});
