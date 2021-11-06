$(document).ready(function(){

	$('.slider').slick({
		arrows: true,
		dots:true,
		slidesToShow: 3,
		slidesToScroll: 3,
		speed: 500,
		infinite: false,
		responsive: [
		{
			breakpoint: 1025,
			settings:{
				slidesToShow: 2,
				slidesToScroll: 2
			}
		}, 
		{
			breakpoint: 769,
			settings:{
				slidesToShow: 1,
				slidesToScroll: 1
			}
		}
		]
	});
});