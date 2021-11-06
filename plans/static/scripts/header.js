
function underline_header(){
	const pageUrl = window.location.href;
	var li_elems = $('li.menu_el');
	for(let i=0; i<li_elems.length; i++){
		$(li_elems[i]).removeClass('active');
	}

	if (pageUrl == "http://127.0.0.1:8000/"){
		$(li_elems[0]).addClass('active');
	} else if (pageUrl.includes('/my-plans/')){
		$(li_elems[1]).addClass('active');

	} else if (pageUrl.includes('/help/')) {
		$(li_elems[2]).addClass('active');

	}
	
}

$(document).ready(()=>{
	underline_header();
});