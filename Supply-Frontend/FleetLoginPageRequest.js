console.log("Running loginPageRequest.js!");

function toPython( param1 ){
  //API key for connection
  console.log("toPython() is called!");
  var url = 'api/cs/login';
  var jsonObject = JSON.stringify(param1);

  //making a bridge to the web server
  var request = new XMLHttpRequest();
  //initializing request to the web server
  request.open('POST',  url, true);
  //Setting the header of the API request
  request.setRequestHeader("Content-type", "application/json");

  //do something with the data being processed
  request.onload = function()
  {
	 console.log("request.onload is called!");
    //JSON function to parse data from the api
    // var info = JSON.parse(param1)
    //making a request body:
    //var body = context.proxyRequest.body.asJSON.param1;

    //if the request is good and valid
    //no problem would happen
    if (request.status >= 200 && request.status < 400){
      console.log("Request is sent!");
      console.log("Response: " + request.response);
      console.log(request.statusText);
      goToPage("loginSuccessful.html");
    }

    else {
      //Error handling
      const errorMessage = document.createElement('error');
      errorMessage.textContent = "Connection Error!";
      console.log(request.status);
      alert ("Login error: " + request.status + " (" + request.response +  ")");
    }
  }

  	//request get sent out!
	request.send(jsonObject);
}
