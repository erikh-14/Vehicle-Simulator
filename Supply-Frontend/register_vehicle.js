console.log("Running register_vehicle.js")

/*
//Whenever the submit button is click, the vehicle will be registered
//a json object and send to the python server


//Getting the submit button for an event listener
var submit = document.getElementById("submit");

//event listenter:
submit.addEventListener( 'submit', function(e) {
    const
})
*/

function generate_vehicle() {
  console.log("register vehicle's register_vehicle() is called!");
  var url = '/api/backend/generatevehicle';
  //making a bridge to the web server
  var request = new XMLHttpRequest();
  //initializing request to the web server
  request.open('POST', url, true);
  //Setting the header of the API request

  request.onload = function () {
    console.log("request.onload is called!");

    // Good response
    if (request.status >= 200 && request.status < 400) {
      console.log("Response: " + request.response);
      console.log(request.statusText);
      alert("Response: " + request.response);
    }

    else {
      //Error handling
      const errorMessage = document.createElement('error');
      errorMessage.textContent = "Connection Error!";
      alert(request.status + " FAILED: Registration of vehicle failed!");
      console.log(request.status);
    }
  }

  //request get sent out!
  request.send();
}

function register_vehicle(vehicle_dictionary) {
  console.log("register vehicle's register_vehicle() is called!");
  var url = '/api/backend/registervehicle';

  var json_object = JSON.stringify(vehicle_dictionary);
  console.log(json_object);

  //making a bridge to the web server
  var request = new XMLHttpRequest();
  //initializing request to the web server
  request.open('POST', url, true);
  //Setting the header of the API request
  request.setRequestHeader("Content-type", "application/json");

  //do something with the data being processed

  request.onload = function () {
    console.log("request.onload is called!");

    // Good response
    if (request.status >= 200 && request.status < 400) {
      console.log("Request is sent!");
      console.log("Response: " + request.response);
      console.log(request.statusText);
      alert("Registration of vehicle " + vehicle_dictionary['vehicle_name'] + " successful!");
      load_page("dashboard.html");
    }

    else {
      //Error handling
      const errorMessage = document.createElement('error');
      errorMessage.textContent = "Connection Error!";
      alert(request.status + " FAILED: Registration of vehicle " + vehicle_dictionary['vehicle_name'] + " failed! (" + request.response + ")");
      console.log(request.status);
    }
  }

  //request get sent out!
  request.send(json_object);
}
