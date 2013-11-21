function deleteStory(story_id) {
	if (confirm("Really delete this story? This action cannot be undone.")) {
		$.post("/story/delete/", {
			id: story_id,
		},
		function(data) {
			window.location.reload(true);
		});
	}
}
