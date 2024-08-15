const
    $ = require('jquery');

export let $forms;

window.ParsleyConfig = {
    classHandler: function (f) {
        return f.$element.closest('.error-handler');
    },
    errorClass: "is-invalid",
    errorsContainer: function (f) {
        return f.$element.closest('.error-handler');
    },
    errorsWrapper: "<ul class='list-unstyled help-block is-invalid col-lg-12'></ul>",
    excluded: "input[type=button], input[type=submit], input[type=reset], input[type=hidden], [disabled], :hidden:not(.modal *)",
    trigger: "change keyup select"
};

export function showMessage(isShow, status, _show_time) {
    const ajax_alert = $(".ajax-alert");
    const ajax_msg = $("#ajax-msg");
    if (isShow) {
        ajax_alert.removeClass('d-none').css('display', '');
        let show_time = 3000;
        if (!status) {
            ajax_alert.addClass('alert-success');
        } else {
            show_time = 5000;
            ajax_alert.addClass('alert-' + status);
        }
        if (_show_time) {
            show_time = _show_time;
        }
        setTimeout(function () {
            ajax_msg.text('');
            ajax_alert.addClass('d-none').removeClass('alert-danger alert-warning alert-info');
        }, show_time);
    } else {
        ajax_msg.text('');
        ajax_alert.addClass('d-none');
    }
}
