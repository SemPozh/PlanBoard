function changeView(){
	$('.tmp-view').each((index, el) =>{
		$(el).on('click', (e)=>{
			e.preventDefault();

			var new_style = $(el).attr('list_style');

			if (new_style == 'grid'){
				console.log('grid');
			} else{
				console.log('slider');
			}
		});
	})
}


$(document).ready(()=>{
	changeView();
});