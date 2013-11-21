$(document).ready(function() {

	// change the fractal classes for fun
	$('.fractal_indent').addClass('explorer_indent');
	$('.fractal_element').addClass('explorer_element');
	$('.fractal_empty').remove();
	$('.fractal_missing').addClass('explorer_missing');

	$('.fractal_indent').removeClass('fractal_indent');
	$('.fractal_element').removeClass('fractal_element');
	$('.fractal_missing').removeClass('fractal_missing');

	// set initial element visibility
	$('.explorer_element').hide();
	$('.fractal_root').show();
	
	// add expander buttons
	$('.explorer_indent').each( function(index, value) {		
		$(this).append('<span class="explorer_expander"><img src="/static/images/explore-small.png"/> click here to read more</span>');
	});

	// add expander event and set visibility
	$('.explorer_expander').each( function(index, value) {	
		$(this).parent().hide();
		$(this).click(expand);
	});

	// add contract event
	$('.explorer_element').each( function(index, value) {
		$(this).click(contract);
	});

	// remove contract event for root
	$('.fractal_root').unbind('click');

	// show the first expander if it exists
	$('#explorer > .explorer_indent').show();
});

function expand(event) {
	$(this).hide();
	$(this).parent().children('.explorer_element').fadeIn('slow');
	$(this).parent().children('.explorer_indent').fadeIn("slow");
	log("expanded " + $(this).parent().children('.explorer_element').attr('id'));
}

function contract(event) {
	$(this).hide();
	$(this).parent().children('.explorer_expander').fadeIn('slow');
	$(this).parent().children('.explorer_indent').hide();

	log("contracted " + $(this).attr('id'));
}

