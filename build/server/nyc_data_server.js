'use strict';

var _require = require('./app'),
    app = _require.app;

var port = 5001;
var server = app.listen(port, function () {
  return console.log('Listening on port ' + port);
});

module.exports = { server: server };