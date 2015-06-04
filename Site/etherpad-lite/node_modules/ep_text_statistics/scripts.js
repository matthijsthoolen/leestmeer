exports.eejsBlock_scripts = function (hook_name, args, cb) {
  args.content = args.content + "<script src='../static/plugins/ep_text_statistics/static/js/textStats.js'></script>";
  return cb();
}
