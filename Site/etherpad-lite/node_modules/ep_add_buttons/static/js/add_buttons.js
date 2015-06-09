/*** 
*
* Most of the logic for task lists are done here
*
*/

if(typeof exports == 'undefined'){
  var exports = this['mymodule'] = {};
}

exports.add_buttons = {
  /***
  *
  *  Add button to the editbar and bind a listener
  *
  ***/

  init: function(){ // Write the button to the dom
    var spacer = '<li class="acl-write separator"></li>';
    var buttonHTML = '<li class="acl-write" id="button1"><a class="grouped-left" data-l10n-id="pad.toolbar.add_buttons.title" title="Task list Checkbox"><span class="buttonicon buttonicon-add_buttons"></span></a></li>';
    $('.menu_left').append(spacer);
    $('.menu_left').append(buttonHTML);

    var buttonHTML = '<li class="acl-write" id="button2"><a class="grouped-right" data-l10n-id="pad.toolbar.add_buttons.title" title="Task list Checkbox"><span class="buttonicon buttonicon-add_buttons"></span></a></li>';
    $('.menu_left').append(buttonHTML);

    $('#button1, #button2').click(function(){
      exports.add_buttons.onButton();
    });

  },
  onButton: function(){ // tell server to save pad content to a local text file and open a new window..
    exports.add_buttons.sendMessageToWriteTxtOfPadToFileSystem();
    // window.open(); Disabled for now.
  },
  sendMessageToWriteTxtOfPadToFileSystem: function(){ // Tell file system to write the padId to the server filesytem
    var message = {};
    message.type = 'WRITE_TO_FILESYSTEM';
    message.padId = pad.getPadId();
    if(message){
      pad.collabClient.sendMessage(message);
    }
  }
}

exports.postAceInit = function(hook, context){exports.add_buttons.init()};
