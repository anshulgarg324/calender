var form = new FormData();
form.append("location", "ajmer");
form.append("description", "raawan");
form.append("start_date", "2017-07-13");
form.append("end_date", "2017-07-16");

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://127.0.0.1:8000/api/events/",
  "method": "POST",
  "headers": {
    "authorization": "Token  f8528b2767d1bbdd8f03601c7a0d84e3893d2442",
    "cache-control": "no-cache",
  },
  "processData": false,
  "contentType": false,
  "mimeType": "multipart/form-data",
  "data": form
}

$.ajax(settings).done(function (response) {
  console.log(response);
});