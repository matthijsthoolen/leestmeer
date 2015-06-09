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


connection.onopen = function (sessionLocal) {
	console.log("Connection opened!");
};


/*
 * Start the connection
 */
function start() {
	connection.open();
}


/*
 * Stop the connection
 */
function stop() {
	connection.close();
}


/*
 * Send analyze request to the server
 */
function sendAnalyzeRequest(message) {
	var jsonmessage = JSON.stringify(message);
	
	var session = connection.session;
	
	session.call('com.analyze.async', [jsonmessage]).then(
		function (resp) {
			console.log("Response:", resp);
			//connection.close();
			return JSON.parse(resp);
		},
		function (error) {
			console.log("Call failed:", error);
			//connection.close();
			return false;
		}
	);
}


/*
 * Debug function
 */
function test() {

	start();

	setTimeout(function() {
		console.log('Sending stuff');

		var message = 
		{
			info: { 
				id: 1,
				name: 'My first etherpad'
			},
			overall: [{
				aviscore: '?',
				analytics: {
					words: 1300,
					paragraphs: 5
				}
			}],
			text: [{
				paragraph: 'Lorem ipsum dolor sit amet',
				aviscore: '?',
				analytics: {
					words: 500,
					avgSentence: 5
				},
				changed: true
			},
			{
				paragraph: 'Second Lorem ipsum dolor sit amet',
				aviscore: 40,
				analytics: {
					words: 800,
					avgSentence: 5
				},
				changed: false
			}]
		};

		if (connection.isConnected) {
			sendAnalyzeRequest(message);
		}
	}, 1500);
}