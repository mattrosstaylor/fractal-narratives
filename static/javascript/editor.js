$(document).ready(function() {
	// change fractal classes
	$('.fractal_indent').toggleClass('fractal_indent editor_indent');
	$('.fractal_element').toggleClass('fractal_element editor_element');

	// add textarea elements to elements
	$('.editor_element').each(function(index, value) {
		$(this).html('<textarea class="expand">' + $(this).html() + '</textarea>');
		$(this).TextAreaExpander();
	});

	// convert the fractal_empty elements
	$('.fractal_empty').each(function(index, value) {
		var elementid = $(this).attr("id");
		$(this).removeAttr("id");
		$(this).toggleClass('fractal_empty editor_indent');
		$(this).html("<div id='"+elementid+"' class='new_empty'>Click here to insert</div>");

		$(".new_empty").click(insert);
		$(".new_empty").toggleClass("new_empty editor_empty");
	});

	// convert the fractal_empty elements
	$('.fractal_missing').each(function(index, value) {
		$(this).toggleClass("fractal_missing editor_missing");
		$(this).html("missing fragment - click here to insert");
		$(this).click(insert);
	});



	// set events
	$('textarea').blur(blurTextArea);
	$('textarea').keyup(keyupTextArea);

	$('#title').keyup(somethingChanged);
	$('#published').change(somethingChanged);
	$('textarea').keyup(somethingChanged);

	// remove blur event from description
	$('#description').unbind('blur');

	// set initial button state
	setButtonActive(false);
});

function insert(event) {
	var parentElement = $(this).parent();
	$(this).unbind("click", insert);

	if ($(this).hasClass("editor_empty")) {
		var elementid = $(this).attr("id");
		log("Inserted "+ elementid);
		parentElement.html("<div class='editor_indent'><div id='" +elementid+ "1' class='new_empty'></div></div><div id='" +elementid+ "' class='editor_element'><textarea class='new_textarea' autocomplete='off'></textarea></div><div class='editor_indent'><div id='" +elementid+ "2' class='new_empty'></div></div>");

		$('.new_empty').click(insert);
		$('.new_empty').html("click here to insert");
		$('.new_empty').hide();
		$('.new_empty').toggleClass("new_empty editor_empty");
	}
	else {
		$(this).toggleClass("editor_missing editor_element");
		$(this).html("<textarea class='new_textarea' autocomplete='off'></textarea>");
	}
	$('.new_textarea').addClass("expand");
	$('.new_textarea').TextAreaExpander();
	$('.new_textarea').blur(blurTextArea);
	$('.new_textarea').keyup(keyupTextArea);
	$('.new_textarea').keyup(somethingChanged);

	$('.new_textarea').focus();
	$('.new_textarea').removeClass("new_textarea");

}

function blurTextArea(event) {
	var value = jQuery.trim( $(this).val() );

	var parentElement = $(this).parent();
	var elementid = parentElement.attr('id');

	if ((value) == "") {
		var parentIndent = parentElement.parent();

		if (parentIndent.find('.editor_empty').length > 2 || parentElement.is(".fractal_root")) {
			log("Emptied "+ elementid);

			$(this).remove();
			parentElement.html("missing fragment - click here to insert");
			parentElement.toggleClass("editor_element editor_missing");
		}
		else {
			log("Removed "+ elementid);

			$(this).remove();
			parentElement.html("Click here to insert");
			parentElement.toggleClass("editor_element editor_empty");
			parentIndent.children(".editor_indent").remove();
		}
		parentElement.click(insert);

	}
	else {
		log("Changed " +elementid+ " to " +value);
	}	
}

function keyupTextArea() {
	if ($(this).parent().hasClass("fractal_root")) { return; }

	var value = jQuery.trim( $(this).val() );
	if (value == "") {
		$(this).parent().parent().children(".editor_indent").children(".editor_empty").slideUp("slow");
	}
	else {
		$(this).parent().parent().children(".editor_indent").children(".editor_empty").slideDown("slow");
	}
}

function parse(element, elementName) {
	var output ="<" + elementName + ">";

	element.children().each(function(index) {
		var c = $(this);		

		if (c.is(".editor_indent")) {
			if (c.children(".editor_empty").length == 0) {
				output += parse(c, "fractal");
			}
		}
		else if (c.is(".editor_element")) {
			output += "<text>" + xmlEncode(c.children(":first").val()) + "</text>";
		}
		else if (c.is(".editor_missing")) {
			output += "<text></text>";
		}

	});

	output +="</" + elementName + ">";
	return output;
}

function save() {
	log("Saving");
	$.post("/story/save/", {
			id: $("#story_id").val(),
			title: $("#title").val(),
			description: $("#description").val(),
			published: $("#published").prop("checked"),
			xml: parse($("#editor:first"), "story"),
		},
		function(data) {
			setButtonActive(false);
			log(data);
		}
	);

}

function somethingChanged(event) {
	setButtonActive(true);
}

function setButtonActive(state) {
	if (state == false) {
	    $('#save_button').attr("disabled", "true");
	}
	else {
	    $('#save_button').removeAttr("disabled");
	}
}

