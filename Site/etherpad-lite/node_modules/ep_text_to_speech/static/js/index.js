var _, $, jQuery;
var $ = require('ep_etherpad-lite/static/js/rjquery').$;

exports.postAceInit = function(name, context){

  $.getScript('../../static/plugins/ep_text_to_speech/static/js/mespeak/mespeak.js', function(){
    // Be prepared...
    meSpeak.loadConfig("../../static/plugins/ep_text_to_speech/static/js/mespeak/mespeak_config.json");
    meSpeak.loadVoice("../../static/plugins/ep_text_to_speech/static/js/mespeak/voices/en/en-us.json");
  });

  $('#ep_text_to_speech_play').click(function(){
    context.ace.callWithAce(function(ace){
      var rep = ace.ace_getRep();
      if(rep.selStart[1] !== rep.selEnd[1]){
        var line = rep.lines.atIndex(rep.selStart[0]);
        var text = line.text.substring(rep.selStart[1], rep.selEnd[1]);
      }else{
        var text = rep.alltext;
      }

      // speak the text
      meSpeak.speak(text);

    }, 'text_to_speech', true);
  });

  $('#ep_text_to_speech_stop').click(function(){
    meSpeak.speak(""); // stops playback - only works on IOS FEHHHH
  });
  
}

