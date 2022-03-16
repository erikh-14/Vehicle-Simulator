console.log("Running display_vehicle.js")


function get_vehicle(){

    //API key for connection
    console.log("get_vehicle() is called!");
    var url = '/api/backend?vehicle-all=1';
    https://supply.team12.softwareengineeringii.com/api/cs?vehicle-all=1



    //making a bridge to the web server
    var request = new XMLHttpRequest();

    request.open('GET',  url, true);
    request.send();



    request.onreadystatechange = function() {
    //good response
    if (this.readyState == 4 && this.status == 200) {
        var obj = JSON.parse(this.responseText);
        for(var key in obj){

          if(obj.hasOwnProperty(key)){

            console.table('Key : ' + key + ', Value:' + obj[key]._id)

          }


          var vehicle_output = "";

          for (var i = 0; i < obj.length; ++i) {

// If the object contains corresponding values, output it along with their labels
              if(obj.hasOwnProperty(i)){
             vehicle_output = vehicle_output.concat("Availability: " + obj[i].is_available + "<br>" +
               "ID: " + obj[i]._id + "<br>" +
               "VIN: " + obj[i].vin + "<br>" +
               "Vehicle Name: " + obj[i].vehicle_name + "<br>" +
               "Vehicle Type: " + obj[i].vehicle_type + "<br>" +
               "Vehicle Color: " + obj[i].vehicle_color + "<br>" +
               "vehicle_position" + obj[i].vehicle_position + "<br>" +
                obj[i].vehicle_status  + "<br>" + "<br>");

              }
              var col = [];
            for (var i = 0; i < obj.length; i++) {
                for (var key in obj[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }
            var table = document.createElement("table");

            var tr = table.insertRow(-1);                   // TABLE ROW.

        for (var i = 0; i < col.length; i++) {
            var th = document.createElement("th");      // TABLE HEADER.
            th.innerHTML = col[i];
            tr.appendChild(th);
        }
        for (var i = 0; i < obj.length; i++) {

           tr = table.insertRow(-1);

           for (var j = 0; j < col.length; j++) {
               var tabCell = tr.insertCell(-1);
               tabCell.innerHTML = obj[i][col[j]];
           }
       }
       var divContainer = document.getElementById("response");
        divContainer.innerHTML = "";
        divContainer.appendChild(table);

          }











        }
    }
};

}








    //initializing request to the web server



        //request get sent out!
