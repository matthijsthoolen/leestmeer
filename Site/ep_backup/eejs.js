var eejs = require('ep_etherpad-lite/node/eejs/');

exports.eejsBlock_mySettings = function (hook_name, args, cb)
{
  args.content = args.content + eejs.require('ep_text_statistics/templates/text_statistics.ejs', {settings : false});
  return cb();
}

exports.eejsBlock_editbarMenuRight = function(hook_name, args, cb){
  args.content = eejs.require('ep_text_statistics/templates/text_statistics.ejs', {settings : false}) + args.content;
  return cb();
}

