function csrf() {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '' ) {
			var cookies = document.cookie.split(';');
			for (var i=0; i<cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				if (cookie.substring(0, name.length+1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}

			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	function sameOrigin(url) {
		var host = document.location.host;
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;

		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
	}

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
			}
		}
	});
}





function add_input() {
	var elem_id = 1;
	var template_data = {'data': []};
	$('.input_elem').each((index, el) => {
		$(el).on('click', (e) => {
			e.preventDefault();

			var field_id = $(el).attr('field_id');
			
			
			$.ajax({
				method: 'GET',
				dataType: 'json',
				url: '/ajax_add_template/',
				data: {
					'field_id': field_id,
					'elem_id': elem_id
				},
				success: (data) =>{
					$('.workspace_main').append(data['input_html']);


					var html_data = $(data['input_html'])
					var popupId = 'popup' + elem_id;
					
					var popup_el = '<div id="' + popupId + '" class="popup">\
										<div class="popup__body">\
											<div class="popup__content">\
												<a href="#" class="popup__close close-popup">X</a>\
												<div class="popup__title">' + data["field_title"] + '</div>\
												<div class="popup__main">\
													<div class="tabs">\
															<div class="tab current" id="names_tab">Названия</div>\
															<div class="tab" id="properties_tab">Свойства</div>\
															<div class="tab" id="sizes_tab">Размеры</div>\
															<div class="tab" id="content_tab">Наполнение</div>\
													</div>\
													<div class="main_form">\
														<form action="" method="post" class="input_settings_form" elem_id="' + elem_id +'" field_id="' + field_id + '">\
															<div class="modal_settings__input names_tab">\
																<span>Подсказка</span><input type="text" value="" name="input_label">\
															</div>\
															<div class="modal_settings__input names_tab">\
																<span>Начальное значение</span><input type="text" name="input_default">\
															</div>\
															<div class="modal_settings__input properties_tab">\
																<span>Максимальная длина</span><input type="number" name="input_maxlength">\
															</div>\
															<div class="modal_settings__input properties_tab">\
																<span>Максимальное значение</span><input type="number" name="input_maxvalue">\
															</div>\
															<div class="modal_settings__input properties_tab">\
																<span>Минимальное значение</span><input type="number" name="input_minvalue">\
															</div>\
															<div class="modal_settings__input properties_tab">\
																<span>Может быть пустым</span>\
																Да<input type="radio" name="can_blank" value="1">\
																Нет<input type="radio" name="can_blank" value="0" checked>\
															</div>\
															<div class="modal_settings__input sizes_tab">\
																<span>Высота поля в пикселях</span><input type="number" name="input_height">\
															</div>\
															<div class="modal_settings__input content_tab">\
																<span class="choose_options__span">Варианты выбора</span>\
																<div>\
																	<input type="text" value="Some option" class="choose_options__input" name="input_option">\
																	<input type="text" value="Another option" class="choose_options__input" name="input_option">\
																</div>\
																<button class="add_option__btn" elem_id="'+ elem_id +'">+</button>\
															</div>\
															<button type="submit" class="save_changes">СОХРАНИТЬ</button>\
														</form>\
													</div>\
												</div>\
											</div>\
										</div>\
									</div>';
					$('main').append(popup_el);

					// Modal

					const popupLinks = document.querySelectorAll('.popup-link');
					const body = document.querySelector('body');
					const lockPadding = document.querySelectorAll('.lock-padding');

					let unlock = true;

					const timeout = 800;

					if(popupLinks.length > 0) {
						for (let index=0; index < popupLinks.length; index++) {
							const popupLink = popupLinks[index];
							popupLink.addEventListener("click", function(e) {
								const popupName = popupLink.getAttribute('href').replace('#', '');
								const currentPopup = document.getElementById(popupName);
								popupOpen(currentPopup);
								e.preventDefault();
							});
						}
					}

					const popupCloseIcon = document.querySelectorAll('.close-popup');
					if(popupCloseIcon.length > 0) {
						for (let index = 0; index < popupCloseIcon.length; index++) {
							const el = popupCloseIcon[index];
							el.addEventListener('click', function(e) {
								popupClose(el.closest('.popup'));
								e.preventDefault();
							});
						}
					}

					function popupOpen(currentPopup) {
						if (currentPopup && unlock) {
							const popupActive = document.querySelector('.popup.open');
							if (popupActive) {
								popupClose(popupActive, false);
							} else {
								bodyLock();
							}
							currentPopup.classList.add('open');
							currentPopup.addEventListener('click', function(e) {
								if (!e.target.closest('.popup__content')){
									popupClose(e.target.closest('.popup'));
								}
							});
						}
					}

					function popupClose(popupActive, doUnlock = true) {
						if (unlock) {
							popupActive.classList.remove('open');
							if (doUnlock) {
								bodyUnlock();
							}
						}
					}

					function bodyLock() {
						const lockPaddingValue = window.innerWidth - document.querySelector('.wrap').offsetWidth + 'px';

						if (lockPadding.length > 0) {
							for (let index=0; index<lockPadding.length; index++) {
								const el = lockPadding[index];
								el.style.paddingRight = lockPaddingValue;
							}
						}
						body.style.paddingRight = lockPaddingValue;
						body.classList.add('lock');

						unlock = false;
						setTimeout(function() {
							unlock = true;
						}, timeout);
					}

					function bodyUnlock() {
						setTimeout(function() {
							if (lockPadding.length > 0) {
								for (let index = 0; index < lockPadding.length; index++) {
									const el = lockPadding[index];
									el.style.paddingRight = '0px';
								}
							}
							body.style.paddingRight = '0px';
							body.classList.remove('lock');
						}, timeout);

						unlock = false;
						setTimeout(function() {
							unlock = true;
						}, timeout);
					}

					document.addEventListener('keydown', function(e) {
						if (e.which === 27) {
							const popupActive = document.querySelector('.popup.open')
							popupClose(popupActive);
						}
					});


					(function() {
						if (!Element.prototype.closest) {
							Element.prototype.closest = function(css) {
								var node = this;
								while(node) {
									if (node.matches(css)) return node;
									else node = node.parentElement;
								}
								return null;
							};
						}
					})();

					(function() {
						if(!Element.prototype.matches) {
							Element.prototype.matches = Element.prototype.matchesSelector ||
								Element.prototype.webkitMatchesSelector ||
								Element.prototype.mozMatchesSelector ||
								Element.prototype.msMatchesSelector;

						}
					})();

					// Tabs

					const tabs = document.querySelectorAll('.tab');
					for (let index=0; index<tabs.length; index++){
						let tabEl = tabs[index];
						tabEl.addEventListener('click', function(e){
							for(let tab=0; tab<tabs.length; tab++){
								currentTab = tabs[tab];
								if (currentTab.classList.contains('current')) {
									currentTab.classList.remove('current');
								}
							}
							tabEl.classList.add('current');
							var settingsClass = tabEl.id;
							var inputSettingsList = document.querySelectorAll('.modal_settings__input');
				
							for (let input=0; input<inputSettingsList.length; input++){

								if (settingsClass == 'properties_tab') {
									$('.sizes_tab').css('display','none');
									$('.content_tab').css('display','none');
									$('.names_tab').css('display','none');
									$('.properties_tab').css('display','block');
								} else if (settingsClass == 'names_tab') {
									$('.sizes_tab').css('display','none');
									$('.content_tab').css('display','none');
									$('.names_tab').css('display','block');
									$('.properties_tab').css('display','none');
								} else if (settingsClass == 'sizes_tab') {
									$('.sizes_tab').css('display','block');
									$('.content_tab').css('display','none');
									$('.names_tab').css('display','none');
									$('.properties_tab').css('display','none');
								} else {
									$('.sizes_tab').css('display','none');
									$('.content_tab').css('display','block');
									$('.names_tab').css('display','none');
									$('.properties_tab').css('display','none');
								}
							}
							e.preventDefault();
						});
					}

					// Modal window form handling
					var current_option_btn = $('.add_option__btn')[$('.add_option__btn').length-1];
					$(current_option_btn).on('click', (e) =>{
							e.preventDefault();

							let popup_id = $(current_option_btn).attr('elem_id');
							let options_wrap = $('#popup' + popup_id).find('.content_tab div');
							$(options_wrap).append('<input type="text" value="Another option" class="choose_options__input" name="input_option">');
						});	

						

					

					let input_settings_data_def = {
						'field_id': elem_id,
						'elem_id': field_id,
						'attrs': {
							'label': '',
							'default_value': '',
							'maxlength': '',
							'maxvalue': '',
							'minvalue': '',
							'canBeBlank': '0',
							'height': '',
							'options': ['Some option', 'Another option']
						}
					};

 
					template_data['data'].push(input_settings_data_def);
					var all_inputs = $('form.input_settings_form');
					var current_input = all_inputs[all_inputs.length-1];				


					$(current_input).on('submit', (e) => {
						e.preventDefault();
						var label = $(current_input).find('[name="input_label"]').val();
						var default_value = $(current_input).find('[name="input_default"]').val();
						var maxlength = $(current_input).find('[name="input_maxlength"]').val();
						var maxvalue = $(current_input).find('[name="input_maxvalue"]').val();
						var minvalue = $(current_input).find('[name="input_minvalue"]').val();
						var canBeBlank = $(current_input).find('[name="can_blank"]:checked').val();
						var height = $(current_input).find('[name="input_height"]').val();
						var options = [];

						for (let i=0; i<$(current_input).find('.choose_options__input').length; i++) {
							let option = $(current_input).find('.choose_options__input')[i];
							options.push($(option).val());
						}

						let input_settings_data = {
							'field_id': $(current_input).attr('field_id'),
							'elem_id': $(current_input).attr('elem_id'),
							'attrs': {
								'label': label,
								'default_value': default_value,
								'maxlength': maxlength,
								'maxvalue': maxvalue,
								'minvalue': minvalue,
								'canBeBlank': canBeBlank,
								'height': height,
								'options': options
							}
						};


						if (input_settings_data['field_id'] == '1'){
							let input = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							$(input).attr('value', input_settings_data['attrs']['default_value']);
							$(input).attr('maxlength', input_settings_data['attrs']['maxlength']);
							$(input).css('height' ,input_settings_data['attrs']['height'] + 'px');

						} else if(input_settings_data['field_id'] == '2') {
							let input = $('textarea[name="name'+ input_settings_data['elem_id'] +'"]');
							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							$(input).text(input_settings_data['attrs']['default_value']);
							$(input).attr('maxlength', input_settings_data['attrs']['maxlength']);
							$(input).css('height' ,input_settings_data['attrs']['height'] + 'px');

						} else if(input_settings_data['field_id'] == '3'){
							let input = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							$(input).attr('value', input_settings_data['attrs']['default_value']);
							$(input).attr('max', input_settings_data['attrs']['maxvalue']);
							$(input).attr('min', input_settings_data['attrs']['minvalue']);
							$(input).css('height' ,input_settings_data['attrs']['height'] + 'px');

						} else if (input_settings_data['field_id'] == '4'){
							let inputs = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$('label[for="name'+ input_settings_data['elem_id'] +'"]').text(input_settings_data['attrs']['label']);


							var button_wrap = $('.button_wrap[elem_id="'+ input_settings_data['elem_id'] +'"]').empty();
							for (let option=0; option<input_settings_data['attrs']['options'].length; option++){
								$(button_wrap).append('<label class="input_radio_css_label"> \
														<input type=radio class="input_radio_css" name="name'+ input_settings_data['elem_id'] +'" value="'+ input_settings_data['attrs']['options'][option] +'"> \
														<span class="input_radio_css_fake"></span> \
														<span class="text">'+ input_settings_data['attrs']['options'][option] +'</span> \
													</label>');
							}
							inputs = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							for (let input=0; input<inputs.length; input++) {
								if (input_settings_data['attrs']['default_value'] === $(inputs[input]).attr('value')) {
									$(inputs[input]).prop('checked', true);
								} else
									$(inputs[input]).prop('checked', false);

							}

						} else if (input_settings_data['field_id'] == '5'){
							let inputs = $('input[name="name'+ input_settings_data['elem_id'] +'"]');
							$('label[for="name'+ input_settings_data['elem_id'] +'"]').text(input_settings_data['attrs']['label']);


							var button_wrap = $('.button_wrap[elem_id="'+ input_settings_data['elem_id'] +'"]').empty();
							for (let option=0; option<input_settings_data['attrs']['options'].length; option++){
								$(button_wrap).append('<label class="input_checkbox_css_label"> \
														<input type="checkbox" class="input_checkbox_css" name="name'+ input_settings_data['elem_id'] +'" value="'+ input_settings_data['attrs']['options'][option] +'"> \
														<span class="input_checkbox_css_fake"></span> \
														<span class="text">'+ input_settings_data['attrs']['options'][option] +'</span> \
													</label>');
							}
							inputs = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							for (let input=0; input<inputs.length; input++) {
								if (input_settings_data['attrs']['default_value'] === $(inputs[input]).attr('value')) {
									$(inputs[input]).prop('checked', true);
								} else
									$(inputs[input]).prop('checked', false);
							}

						} else if (input_settings_data['field_id'] == '6'){

							var select_label = $('label[for="name'+ input_settings_data['elem_id'] +'"]');
							$(select_label).text(input_settings_data['attrs']['label']);

							var select_options = $(select_label).parent().find('select').empty();
							for (let option=0; option<input_settings_data['attrs']['options'].length; option++){
								$(select_options).append('<option value="'+ input_settings_data['attrs']['options'][option] +'" class="select_option">'+ input_settings_data['attrs']['options'][option] +'</option>');
							}

							let options = $('.select_option');
							for (let i=0; i<options.length; i++){
								if($(options[i]).attr('value')==input_settings_data['attrs']['default_value']){
									$(options[i]).prop('selected', true);
								} else {
									$(options[i]).prop('selected', false);
								}
							}


						} else if(input_settings_data['field_id'] == '7'){
							let input = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							let data_value = input_settings_data['attrs']['default_value']
							let cleanDataValue = data_value.slice(6, 10) + '-' + data_value.slice(3, 5) + '-' + data_value.slice(0, 2);
							$(input).attr('value', cleanDataValue);
							$(input).css('height' ,input_settings_data['attrs']['height'] + 'px');

						} else if (input_settings_data['field_id'] == '8') {
							let input = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							// const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
							// if (re.test(input_settings_data['attrs']['default_value']).toLowerCase()){
							// 	$(input).attr('value', input_settings_data['attrs']['default_value']);
							// }

							$(input).attr('value', input_settings_data['attrs']['default_value']);
							$(input).attr('maxlength', input_settings_data['attrs']['maxlength']);
							$(input).css('height' ,input_settings_data['attrs']['height'] + 'px');

						} else if (input_settings_data['field_id'] == '9') {
							let input = $('input[name="name'+ input_settings_data['elem_id'] +'"]');

							$(input).parent().find('.input_label').text(input_settings_data['attrs']['label']);
							$(input).attr('value', input_settings_data['attrs']['default_value']);
							$(input).attr('max', input_settings_data['attrs']['maxvalue']);
							$(input).attr('min', input_settings_data['attrs']['minvalue']);

						}



						currentElemIndex = input_settings_data['elem_id'] - 1; 
						template_data['data'][currentElemIndex] = input_settings_data;
						let active_popup = document.querySelectorAll('#popup' + input_settings_data['elem_id'])[0];
						popupClose(active_popup);



					});

					


					elem_id += 1;
				}

			});


		});
	});

	
	$('.save_template').on('click', (e) => {
			e.preventDefault();

			var title_val = $('.title_form input').val();
			const requestURL = '';

			var data = JSON.stringify({
				'template_data': template_data,
				'template_title': title_val
			});

			$.ajax({
				method: 'POST',
				dataType: 'text',
				url: '/ajax_save_template/',
				data: {
					'data': data,
					'template_title': title_val
				},
				success: (data) =>{
					window.location.replace("http://127.0.0.1:8000/my-plans");
					

				}
			});
	});
}



function check_undefined() {
	$('.title_form input').on('input', (e) => {
		e.preventDefault();

		var title_val = $('.title_form input').val();
		


		if (title_val == ''){
			$('.title_form input').attr('value', 'untitled');
			$('.title_form input').val('untitled');
		} else {
			$('.title_form input').val(title_val);
		}
	});
}



$(document).ready(() => {
	csrf();
	add_input();
	check_undefined();
});