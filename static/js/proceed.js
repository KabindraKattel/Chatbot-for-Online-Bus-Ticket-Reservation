  parent = window.parent;
	function sendback() {

  parent.document.getElementById('textInput').value = document.getElementById('buttonInput').value;
               parent.getBotResponse();
  };

      $("#buttonInput").click(function() {
           sendback()
           });
