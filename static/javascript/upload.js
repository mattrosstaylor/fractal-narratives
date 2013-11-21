$(document).ready(function() {
	var options = {
		target: '#output',
		beforeSubmit:  showRequest,
		success:       showResponse
	};

	$('#upload').submit(function() {
		$(this).ajaxSubmit(options); 
		return false;
	});
});

function showRequest(formData, jqForm, options) {
	$('#output').html("Uploading...");
	$('.story_illustration').attr("src", "/static/images/ajax-loader.gif");
	return true;
};


 
// post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  {
//	alert('status: ' + statusText + '\n\nresponseText: \n' + responseText + '\n\nThe output div should have already been updated with the responseText.');
	var id = $('#story_id').val();
	
	$('.story_illustration').attr("src", "/static/illustrations/" +id +".jpg?time="+ new Date().getTime());
} 
