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

	session.call('com.analyze.async').then(
		function (now) {
			console.log("Current time:", now);
			connection.close();
		},
		function (error) {
			console.log("Call failed:", error);
			connection.close();
		}
	);

	var received = 0;

	function onevent1(args) {
		console.log("Got event:", args[0]);
		received += 1;
		if (received > 5) {
			console.log("Closing ..");
			connection.close();
		}
	}

	session.subscribe('com.analyze.async', onevent1);
};

connection.open();