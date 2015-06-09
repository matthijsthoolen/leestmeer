var eejs = require('ep_etherpad-lite/node/eejs/');

exports.eejsBlock_scripts = function (hook_name, args, cb) {
  args.content = args.content + "<script src='../static/plugins/ep_add_buttons/static/js/add_buttons.js'></script>";
  return cb();
}

exports.eejsBlock_styles = function (hook_name, args, cb) {
  args.content = args.content + "<link href='../static/plugins/ep_add_buttons/static/css/button.css' rel='stylesheet'>";
  return cb();
}

