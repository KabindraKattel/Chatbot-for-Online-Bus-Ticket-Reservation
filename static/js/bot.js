  function getBotResponse() {
          var rawText = document.getElementById('textInput').value;
          var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
          document.getElementById('textInput').value="";
          $("#chatbox").append(userHtml);
          document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
          $.get("/get", { msg: rawText }).done(function(data) {
            var botHtml = '<p class="botText"><span>' + data + '</span></p>';
            $("#chatbox").append(botHtml);
          });
        }
        $("#textInput").keypress(function(e) {
            if(e.which == 13) {
                getBotResponse();
            }
        });
        $("#buttonInput").click(function() {
          getBotResponse();
        })
