function formAjaxSubmit(modal, action, cbAfterLoad, cbAfterSuccess) {
	var form = modal.find('.modal-body form');
	var header = $(modal).find('.modal-header');

	var btn-save = modal.find('.modal-footer .btn-save');
	if (btn-save) {
		btn-save.off().on('click', function(e) {
			modal.find('.modal-body form').submit();
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

				if ($(xhr).find('.hasd-error').length > 0) {
					formAjaxSubmit(modal, url, cbAfterLoad, cbAfterSuccess);
				} else {
					$(modal).modal('hide');
					if (cbAfterSuccess) { cbAfterSuccess(modal); }
				}
			},
			error: function(xhr, ajaxOptions, thrownError) {
				console.log('Server Error': + thrownError)
			}
		});
	});
}