function customStart()
{
	//define your javascript here
	//jquery is available - except index.js
	//you can load extra scripts with $.getScript http://api.jquery.com/jQuery.getScript/

	// Add the sidebar, from: http://www.dustindiaz.com/add-and-remove-html-elements-dynamically-with-javascript/
	var ni = document.getElementById('editorcontainerbox');

	// Make sidebar and add to the page
	var sidebar = document.createElement('div');
	var divIdName = 'sidebar';
	sidebar.setAttribute('id',divIdName);
	sidebar.innerHTML = "<div id='sidebarInner'>Hallo Kees </a>";
	ni.appendChild(sidebar);
		
		
}
