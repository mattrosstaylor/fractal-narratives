$(document).ready(function() {

	// change the fractal classes for fun
	$('.fractal_indent').addClass('randomiser_indent');
	$('.fractal_element').addClass('randomiser_element');
	$('.fractal_empty').remove();
	$('.fractal_missing').addClass('randomiser_missing');

	$('.fractal_indent').removeClass('fractal_indent');
	$('.fractal_element').removeClass('fractal_element');
	$('.fractal_missing').removeClass('fractal_missing');

	// hide everything!!
	$('.randomiser_element').hide();
	// wait, not everything ;-)
	$('.fractal_root').show();

	// randomise the story
	randomise($('#randomiser > .randomiser_indent'),0.9);

});

function randomise(element, probability) {
	element.show();
	if (Math.random()<probability) {
		element.children().each(function(index, value) {
			randomise($(this), probability*0.8);
		});
	}
}
