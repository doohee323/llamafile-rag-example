<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-12">
        <h2 class="page-header">
        </h2>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6 offset-lg-1">
        <div class="alert ajax-alert alert-dismissable d-none">
          <button aria-hidden="true" class="close" data-dismiss="alert" type="button">&times;</button>
          <p id='ajax-msg'></p>
        </div>
      </div>
    </div>
    <div class="row form-edit-main">
      <div class="col-lg-6 offset-lg-1">
        <form id="file-upload-form" class="require uploader" data-parsley-excluded="input[type=button], input[type=submit], input[type=reset], input[type=hidden], .form-group row:hidden input[type=file]"
              data-parsley-validate enctype="multipart/form-data"
              method="post">
          <div class="form-group row error-handler">
            <label class="col-lg-3" for="file">Upgrade File</label>
            <div class="col-lg-9">
              <div class="input-group">
                <label class="input-group-btn">
                        <span class="btn btn-primary">
                            Choose File...
                            <input id="file" class="uploader-input d-none" name="file" type="file">
                        </span>
                </label>
                <input class="form-control" readonly type="text">
              </div>
              <div>
                <p id="file-info"></p>
              </div>
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-3" for="file-progress"></label>
            <div class="col-lg-9">
              <div class="progress progress-striped progress-bg">
                <div id="file-progress" class="progress-bar active" role="progressbar">
                </div>
              </div>
            </div>
          </div>
          <div class="form-group row">
            <div class="btn-group offset-lg-10">
              <router-link :to="{name: 'aaa'}" class="btn btn-secondary">Cancel</router-link>
              <button id="apply_btn" class="btn btn-primary offset-lg-11 once" type="button" @click="upload">Upload
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>

import $ from 'jquery';
import {showMessage} from '@/assets/forms.js'
import {getCache} from "@/assets/cache";

export default {
  data: function () {
    return {
      fileSizeLimit: 200 * 1024 * 1024,
      file_size: 0,
      upload_file: null,
      formData: new FormData(),
      vData: {}
    }
  },
  props: [],
  computed: {
    $form() {
      return $(this.$el).find('form');
    },
  },
  methods: {
    setFileUpload() {
      let $this = this;
      const apply_btn = $('#apply_btn');
      const file_upload = $('#file');
      apply_btn.attr('disabled', true);
      this.upload_file = null;

      function onFileUpload() {
        $.ajaxSetup({
          timeout: 60000
        });

        function fileSelectHandler(e) {
          let files = e.target.files || e.dataTransfer.files;
          for (let i = 0; i < files.length; i++) {
            let f = files[i];
            getFileInfo($this, f);
            apply_btn.attr('disabled', false);
            $this.upload_file = f;
            if (!apply_btn) {
              this.uploadFile(f);
            }
          }
        }

        function getFileInfo($this, a_file) {
          printFileInfo('<strong>' + encodeURI(a_file.name) + '</strong>');
          let fileSize = 0;
          if (a_file.size > 1024 * 1024) {
            fileSize = (Math.round(a_file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
          } else {
            fileSize = (Math.round(a_file.size * 100 / 1024) / 100).toString() + 'KB';
          }
          $this.file_size = a_file.size;
          printFileInfo(a_file.name + ' ' + '(' + fileSize + ')');
          file_upload.closest('.input-group').find('input[type=text][readonly]').val(a_file.name);
        }

        function printFileInfo(msg) {
          if (msg.indexOf(':') > -1) {
            msg = msg.substring(msg.indexOf(':') + 1, msg.length);
          }
          if (msg !== '') {
            $('#file-info').text(msg);
          }
        }

        if (window.File && window.FileList && window.FileReader) {
          if (file_upload.length > 0) {
            file_upload[0].addEventListener('change', fileSelectHandler, false);
          }
        }
      }

      onFileUpload();
    },
    updateProgressbarStatus(progressbarId, val) {
      const $status = $('#' + progressbarId);
      val = Math.round((val || 0) * 100);
      if (progressbarId === 'restart_progress') {
        if (val > 0) {
          try {
            let val2 = $status.html();
            val2 = val2.substring(0, val2.length - 1);
            val2 = parseInt(val2);
            if (val2 > val) {
              val = val2;
            }
          } catch (e) {
            console.log('');
          }
        }
      }
      val = Math.min(100, val);
      let percentage = val + '%';
      $status.html(percentage);
      $status.css('width', percentage);
      if (val >= 1 && $status.hasClass('active')) {
        $status.removeClass('active').addClass('bg-success');
      }
      return val;
    },
    returnError(message) {
      const apply_btn = $('#apply_btn');
      const ajax_msg = $("#ajax-msg");
      console.log(message);
      ajax_msg.text('Failed to upgrade image.');
      showMessage(true, 'danger', 10000);
      this.updateProgressbarStatus('file-progress', 0);
      apply_btn.attr('disabled', false);
    },
    sendFile($this, a_file, callback) {
      try {
        let xhr = new XMLHttpRequest();
        $this.formData.append('size', parseInt($this.file_size));
        $this.formData.append('file', a_file);
        $this.formData.append('filename', a_file.name);
        xhr.onload = function () {
          if (xhr.readyState === 4) {
            if (xhr.status !== 200) {
              return $this.returnError(xhr.statusText);
            }
          }
        };
        xhr.upload.addEventListener("progress", function (e) {
          if (e.lengthComputable) {
            $this.closeSending($this, e, callback);
          }
        });
        xhr.addEventListener("error", function () {
          return $this.returnError(xhr.statusText);
        });
        let apiUrl = getCache('config', 'apiUrl');
        xhr.open('POST', `${apiUrl}/upload`, true);
        xhr.overrideMimeType("application/octet-stream");
        xhr.setRequestHeader("Accept", "*/*");
        xhr.onreadystatechange = function () {
        };
        xhr.send($this.formData);
      } catch (e) {
        return $this.returnError(e.responseText);
      }
    },
    closeSending($this, e, callback) {
      const file_upload = $('#file');
      const file_upload_btn = file_upload.parent();
      const ajax_msg = $("#ajax-msg");
      file_upload.prop('disabled', true);
      file_upload_btn.addClass('disabled');
      $('#file-progress')[0].value = e.loaded;
      $this.updateProgressbarStatus('file-progress', e.loaded / parseInt($this.file_size));
      if (Math.floor(e.loaded / parseInt($this.file_size)) >= 1) {
        file_upload.prop('disabled', false);
        file_upload_btn.removeClass('disabled');
        ajax_msg.text('Successfully uploaded!');
        showMessage(true, 'success', 60000);
        setTimeout(function () {
          callback();
        }, 1000);
      }
    },
    uploadFile(a_file) {
      let $this = this;
      const apply_btn = $('#apply_btn');
      const ajax_msg = $("#ajax-msg");
      $this.formData = new FormData();
      $this.updateProgressbarStatus('file-progress', 0);
      if (!a_file) {
        a_file = $this.upload_file;
      }
      let a_file_size = parseInt($this.file_size);
      if (a_file_size <= $this.fileSizeLimit) {
        $this.sendFile($this, a_file, function () {
            let referer = getCache('session', 'referer');
            if (referer === '') {
                referer = '/';
            }
            $this.$router.push(referer);
        });
      } else {
        ajax_msg.text('Uploaded file is larger than the maximum allowed size.');
        showMessage(true, 'warning');
        $this.updateProgressbarStatus('file-progress', 0);
        apply_btn.attr('disabled', false);
      }
    },
    upload() {
      $('#apply_btn').attr('disabled', true);
      this.uploadFile();
    }
  },
  mounted() {
    const $this = this;
    setTimeout(function () {
      $this.setFileUpload($('#file-upload-form'));
    }, 500);
  },
};

</script>