function formAjaxSubmit(modal, action, cbAfterLoad, cbAfterSuccess) {
	var form = modal.find('.modal-body form');
	var header = $(modal).find('.modal-header');

	var btn_save = modal.find('.modal-footer .btn-save');
	if (btn_save) {
		btn_save.off().on('click', function(e) {
			modal.find('.modal-bosy form').submit();
		});
	}

	if (cbAfterLoad) { cbAfterLoad(modal); }
	
	modal.find('form input:visible').first().focus();

	$(form).on('submit', function(e) {
		e.preventDefault();

		var url = $(this).attr('action') || action;

		$.ajax({
			type: $(this).attr('method'),
			url: url,
			data: $(this).serialize(),
			success: function(xhr, ajaxOptions, thrownError) {

				$(modal).find('.modal-body').html(xhr);

				if ($(xhr).find('.has-error').length > 0) {
					formAjaxSubmit(modal, url, cbAfterLoad, cbAfterSuccess);
				} else {
					$(modal).modal('hide');
					if (cbAfterSuccess) { cbAfterSuccess(modal); }
				}
			},
			error: function(xhr, ajaxOptions, thrownError) {
			}
		});
	});
}

$(document).on('click', '.panel-heading span.clickable', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.addClass('panel-collapsed');
        $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.removeClass('panel-collapsed');
        $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('click', '.panel div.clickable', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.addClass('panel-collapsed');
        $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.removeClass('panel-collapsed');
        $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).ready(function () {
    $('.panel-heading span.clickable').click();
    $('.panel div.clickable').click();
});