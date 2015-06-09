try {
	var autobahn = require('autobahn');
} catch (e) {
	// when running in browser, AutobahnJS will
	// be included without a module system
}

var connection = new autobahn.Connection({
	url: 'ws://127.0.0.1:8080/ws',
	realm: 'analyze'}
);

connection.onopen = function (session) {

	var id = 'Me!';
	var message = 
		{
			info: { 
				id: 1,
				name: 'My first etherpad'
			},
			overall: [{
				aviscore: '?',
				analytics: {
					words: 5000,
					paragraphs: 5
				}
			}],
			text: [{
				paragraph: "Lorem ipsum dolor sit amet",
				aviscore: 40,
				analytics: {
					words: 5000,
					paragraphs: 5
				},
				changed: false
			}]
		};
	
	var jsonmessage = JSON.stringify(message);
	
	session.call('com.analyze.async', [jsonmessage]).then(
		function (resp) {
			console.log("Response:", resp);
			connection.close();
		},
		function (error) {
			console.log("Call failed:", error);
			connection.close();
		}
	);
};

connection.open();