var io = require('socket.io')(8080);

console.log('Server started!');

io.on('connection', function(socket) {
	io.emit('this', {will: 'be received by everyone'});
	
	console.log('Hello There!');
	
	socket.on('private message', function (from, msg) {
    console.log('I received a private message by ', from, ' saying ', msg);
  });

  socket.on('disconnect', function () {
    io.emit('user disconnected');
  });
});