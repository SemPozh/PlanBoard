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

				


function bodyLock(lockPadding=document.querySelectorAll('.lock-padding'), body=document.querySelector('body'), timeout=800, unlock) {
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
	const popupLinks = document.querySelectorAll('.popup-link');
	let unlock = true;
	const lockPadding = document.querySelectorAll('.lock-padding');
	const timeout = 800;
	const body = document.querySelector('body');
	const lockPaddingValue = window.innerWidth - document.querySelector('.wrap').offsetWidth + 'px';
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


function popup_esc(){
	document.addEventListener('keydown', function(e) {
		if (e.which === 27) {
			const popupActive = document.querySelector('.popup.open')
			popupClose(popupActive);
		}
	});
}


function popupOpen(currentPopup, unlock) {
	if (currentPopup && unlock) {
		const popupActive = document.querySelector('.popup.open');
		if (popupActive) {
			popupClose(popupActive, unlock, doUnlock=false);
		} else {
			bodyLock(unlock);
		}
		currentPopup.classList.add('open');
	}
}

function popupClose(popupActive, unlock, doUnlock=true) {
	if (unlock) {
		popupActive.classList.remove('open');
		if (doUnlock) {
			bodyUnlock(unlock);
		}
	}
}


function choose_template(){
	var all_templates = $('.template_card');
	var current_template = $(all_templates[0]);
	if (all_templates.length > 0){
		$(all_templates[0]).addClass('choosed_template');
	} else {
		$('.add_plan').css('display', 'none');
	}

	$('.template_card').each((index, el)=>{
		$(el).on('click', (e)=>{
			e.preventDefault();

			
			all_choosed = $('.choosed_template');
			if (all_choosed.length > 0){
				for(let i=0; i<all_choosed.length; i++){
					$(all_choosed[i]).removeClass('choosed_template');
				}
			}

			$(el).addClass('choosed_template');
			current_template = $(el);
			current_template_id = $(current_template).attr('template_id');
			$('.popup-link').prop('href', '#popup'+$(current_template).attr('template_id'));

			$.ajax({
				method: 'GET',
				dataType: 'text',
				url: 'api_get_plans_by_template_id/',
				data: {
					'template_id': current_template_id
				},
				success: (data) =>{
					fields = JSON.parse(data)['data'];
					rows_count = Math.ceil((fields.length)/3);

					var html = '';
					for (let i=0; i<fields.length; i++){
						html += "<div class='plan_card' plan_id='" + fields[i][0] + "'>\
						<i class='fas fa-trash-alt'></i>\
						<a href='#redact-popup" + fields[i][0] + "' class='redact-plan'><img src='../static/images/svg/pencil.svg' alt='' class='redact_card_icon'></a>";
						for(key in fields[i][1]['plan_data']){
							html += "<div class='input_data'>" + fields[i][1]['plan_data'][key] + "</div>"
						};

						html += "</div>";
					}
					$('.plan_wrapper').empty().append(html);
					redact_plan();
					$('.fa-trash-alt').off('click');
					delete_plan();
					$('.sort_by_select').empty();

					let select = $('.sort_by_select');
					$(select).append('<option value="default">Сортировать по</option>');
					for (let index=0; index < JSON.parse(data)['fields']['data'].length; index++){
						$(select).append('<option value="'+ (index+1) +'">field '+ (index+1) +'</option>')
					}
					sort_plans();
					$('.add_plan').off('click');
					add_plan();
				}
			});


		});
	});
}

function redact_template_link(){
	$('.redact_template__link').each((index, el)=>{
		$(el).on('click', (e)=>{
			e.preventDefault();
			
			url = $(el).prop('href');
			document.location.href = url;
		});
	});
}

function add_plan(){
	var current_template = $('.choosed_template');
	$('.add_plan').on('click', (e)=>{
		e.preventDefault();
		var template_id = $(current_template).attr('template_id');
		$.ajax({
			method: 'GET',
			dataType: 'json',
			url: '/my-plans/ajax_add_plan/',
			data: {
				'template_id': template_id
			},
			success: (data)=>{
				var current_popup = $('#popup' + template_id);
				if ($(current_popup).find('.main_form').children().length == 1){
					for (let i=0; i< data['data'].length; i++){
						let current_form = $(current_popup).find('.main_form');
						$(current_form).append(data['data'][i]);
					}
				}



				// Modal
				const popupLinks = document.querySelectorAll('.popup-link');
				const body = document.querySelector('body');
				const lockPadding = document.querySelectorAll('.lock-padding');



				let unlock = true;

				const timeout = 800;


				var popup_current = document.querySelectorAll('#popup' + template_id)[0];
				popupOpen(popup_current, unlock);


				const popupCloseIcon = document.querySelectorAll('.close-popup');
				if(popupCloseIcon.length > 0) {
					for (let index = 0; index < popupCloseIcon.length; index++) {
						const el = popupCloseIcon[index];
						el.addEventListener('click', function(e) {
							popupClose(el.closest('.popup'), unlock);
							e.preventDefault();
						});
					}
				}


				create_plan();
			}
		});

	});
}


function get_plan_data(main_form){
	var children1 = $(main_form).children().first();
	if ($(children1).prop('type') == 'hidden'){
		var all_inputs = $(main_form).children().slice(2, $(main_form).children().length);
	} else{
		var all_inputs = $(main_form).children().slice(1, $(main_form).children().length);
	}


	var currentTemplateId = $(main_form).attr('template_id');
	var currentPopup = document.querySelectorAll('#popup' + currentTemplateId);
	var plan_data = {}

	for(let i=0; i< all_inputs.length; i++){
		let field_id = $(all_inputs[i]).attr('field_id');
		if (['1', '3', '7', '8', '9'].indexOf(String(field_id)) != -1){
			let input_value = $(all_inputs[i]).find('input').val();
			if (input_value == ''){
				input_value = 'Пусто'
			}
			plan_data['field' + (i+1)] = input_value;

		} else if (String(field_id) == '2'){
			let input_value = $(all_inputs[i]).find('textarea').val();
			if (input_value == ''){
				input_value = 'Пусто'
			}
			plan_data['field' + (i+1)] = input_value;

		} else if(['4', '5'].indexOf(String(field_id)) != -1){
			let input_value = $(all_inputs[i]).find('input:checked');

			if (input_value.length > 1){
				input_value_list = [];
				for(let index=0; index<input_value.length; index++){
					input_value_list.push($(input_value[index]).val());
				}
				plan_data['field' + (i+1)] = input_value_list;

			} else if(input_value.length < 1){
				plan_data['field' + (i+1)] = 'Пусто'
			} else{
				plan_data['field' + (i+1)] = input_value.val();
			}


		} else if (field_id == '6'){
			let input_value = $(all_inputs[i]).find('option:selected').text();
			plan_data['field' + (i+1)] = input_value;

		}
	}

	var data = JSON.stringify({
		'plan_data': plan_data,
	});

	return data;
}

function create_plan(){
	$('.main_form').off('submit');
	$('.main_form').each((index, el)=>{
		$(el).on('submit', (e)=>{
			e.preventDefault();

			var currentTemplateId = $(el).attr('template_id');
			var currentPopup = document.querySelectorAll('#popup' + currentTemplateId);
			var data = get_plan_data($(el));

			$.ajax({
				method: 'POST',
				dataType: 'json',
				url: '/my-plans/ajax_create_plan/',
				data: {
					'data': data,
					'template_id': currentTemplateId
				},
				success: (data)=> {

					var plan_html = ''
					plan_html = plan_html + "<div class='plan_card' plan_id='"+ data['plan_id'] +"'>\
					<i class='fas fa-trash-alt'></i>\
					<a href='#redact-popup"+ data['plan_id'] +"' class='redact-plan'><img src='../static/images/svg/pencil.svg' alt='' class='redact_card_icon'></a>";
					for (key in data['plan']['plan_data']){
						plan_html += "<div class='input_data'>" + data['plan']['plan_data'][key] + "</div>";
					}

					plan_html += "</div>";

					$('.plan_wrapper').append(plan_html);


					$('.redact-plan').off('click');
					var csrftoken = csrf();
					let modal = '<div id="redact-popup' + data["plan_id"] + '" class="popup">\
					<div class="popup__body">\
					<div class="popup__content">\
					<a href="#" class="popup__close close-popup">X</a>\
					<div class="popup__main">\
					<form class="main_form" action="#" method="POST" template_id="'+ currentTemplateId +'" plan_id="'+ data['plan_id'] +'">\
					<input type="hidden">\
					<button type="submit" class="save_changes">Сохранить</button>\
					</form>\
					</div>\
					</div>\
					</div>\
					</div>';
					$('main').append(modal);
					redact_plan();
					$('.fa-trash-alt').off('click');
					delete_plan();

				}
			});

			currentPopup[0].classList.remove('open');
			bodyUnlock();
		});
	});
}


function redact_plan(){
	$('.redact-plan').each((index, el)=>{
		$(el).on('click', (e)=>{
			e.preventDefault();
			var plan_id = $(el).attr('href').slice(13);
			$.ajax({
				method: 'GET',
				dataType: 'json',
				url: 'api_get_plan_data/',
				data: {
					'plan_id': plan_id
				},
				success: (data)=>{
					
					const popupLinks = document.querySelectorAll('.popup-link');
					let unlock = true;

					if(popupLinks.length > 0) {

						const popupLink = $(el);
						const popupName = popupLink.attr('href').replace('#', '');
						const currentPopup = document.getElementById(popupName);
						if ($(currentPopup).find('.main_form').children().length == 2){
							for (let i=0; i< data['fields_html'].length; i++){
								let current_form = $(currentPopup).find('.main_form');
								$(current_form).append(data['fields_html'][i]);
							}
						}



						popupOpen(currentPopup, true);
						e.preventDefault();
					}



					const popupCloseIcon = document.querySelectorAll('.close-popup');
					if(popupCloseIcon.length > 0) {
						for (let index = 0; index < popupCloseIcon.length; index++) {
							const el = popupCloseIcon[index];
							el.addEventListener('click', function(e) {
								popupClose(el.closest('.popup'), unlock);
								e.preventDefault();
							});
						}
					}


					$('.main_form').off('submit');
					$('.main_form').each((index, el)=>{
						$(el).on('submit', (e)=>{
							e.preventDefault();


							var currentPlanId = $(el).attr('plan_id');
							var currentPopup = document.querySelectorAll('#redact-popup' + currentPlanId);
							var data = get_plan_data($(el));

							$.ajax({
								method: 'POST',
								dataType: 'json',
								url: '/my-plans/ajax_redact_plan/',
								data: {
									'data': data,
									'plan_id': plan_id
								},
								success: (data)=>{
									var plan_card = $('div[plan_id="'+ plan_id +'"]').empty();
									var html = "<i class='fas fa-trash-alt'></i><a href='#redact-popup"+ currentPlanId +"' class='redact-plan'><img src='../static/images/svg/pencil.svg' alt='' class='redact_card_icon'></a>";
									for(key in data['data']['plan_data']){
										html += '<div class="input_data">'+ data['data']['plan_data'][key] +'</div>'
									}
									
									$(plan_card).append(html);
									popupClose(currentPopup[0], true, doUnlock=true);
									$('.fa-trash-alt').off('click');
									redact_plan();
									$('.fa-trash-alt').off('click');
									delete_plan();
									$('.sort_by_select').off('change');
									sort_plans();
								}
							});
						});
					});
				}
			});
		});
	});
}


function delete_plan(){
	$('.fa-trash-alt').each((index, el)=>{
		$(el).on('click', (e)=>{
			e.preventDefault();

			var plan_card = $(el).parent();
			var plan_id = $(plan_card).attr('plan_id');

			$.ajax({
				method: 'POST',
				dataType: 'json',
				url: '/my-plans/ajax_delete_plan/',
				data:{
					'plan_id': plan_id
				},
				success: (data)=>{
					if (data['data'] == 'success'){
						$(plan_card).remove();
					}
				}
			});
		});
	});
}


function sort_plans(){
	$('.sort_by_select').each((index, el)=>{
		$(el).on('change', (e)=>{
			e.preventDefault();

			var sort_field = $(el).val()

			var cards = $('.plan_card');
			for (let i=0; i < cards.length; i++){
				for (let j=0; j < cards.length - i - 1; j++){
					let current_card = $(cards[j]);
					let next_card = $(cards[j+1]);
					if ($(current_card.children()[1 + Number(sort_field)]).text() > $(next_card.children()[1 + Number(sort_field)]).text()){
						let next_card_content = $(next_card).html();
						let current_card_content = $(current_card).html();
						$(next_card).html(current_card_content);
						$(current_card).html(next_card_content);

					}
				}
			}
			delete_plan();
			redact_plan();
		});
	});
}


$(document).ready(()=>{
	csrf();
	redact_template_link();
	choose_template();
	add_plan();
	redact_plan();
	delete_plan();
	sort_plans();

});