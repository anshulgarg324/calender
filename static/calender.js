$(document).ready(function(){
    console.log("sfsd");
    if (localStorage.getItem('token') == null){
      console.log("fff"); 
      window.location = "http://localhost:8000/api/gsignup/"
    }
    $("#next").click(function(){
        var currentMonth = $("#month").html();
        var currentYear = $("#year").html();
        $("#month").html(parseInt(currentMonth)+1);
    });

    
    // $("add_ev").click(function() {
    //               var form = new FormData();
    //         form.append("location", "ajmer");
    //         form.append("description", "raawan");
    //         form.append("start_date", "2017-07-13");
    //         form.append("end_date", "2017-07-16");

    //         var settings = {
    //         "async": true,
    //         "crossDomain": true,
    //         "url": "http://127.0.0.1:8000/api/events/",
    //         "method": "POST",
    //         "headers": {
    //             "authorization": "Token  f8528b2767d1bbdd8f03601c7a0d84e3893d2442",
    //             "cache-control": "no-cache",
    //             "postman-token": "f29d9218-af7c-47d0-3f25-9a5ca40f97fd"
    //             },
    //         "processData": false,
    //         "contentType": false,
    //         "mimeType": "multipart/form-data",
    //         "data": form
    //         }

    //         $.ajax(settings).done(function (response) {
    //                               console.log(response);
    //                               });

    //         function desc() {
    //             document.getElementById("desc").style.display = "inline";
    //         }
    // })
    $('#sync').click(function(){
      console.log("hi");
      var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://127.0.0.1:8000/api/sync/",
        "method": "GET",
        "headers": {
          "authorization": "Token " + localStorage.getItem('token'),
        }
      };

      $.ajax(settings).done(function (response) {
        if(response.response.success === true) {
          alert("Successfully synchronized!");  
          }
        else
        {
          alert("Sync Unsuccessful!");
        }
        console.log(response);
      });
    });

    $("#cal").datepick({
    	dateFormat: 'yyyy-mm-dd',
      onSelect: function (date) {
        $("#put").empty();
        var token = 'f8528b2767d1bbdd8f03601c7a0d84e3893d2442';
        // console.log('display:date: ',date, token);
        var date_ = date[0];
        var form = new FormData();
        var date = date_.getDate();
        var month = date_.getMonth() + 1;
        if(month < 10) {
          month = "0" + month.toString();
        }
        var year = date_.getYear() + 1900;
        // console.log(date, month, year);
        form.append("date",  `${year}-${month}-${date}`);

        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://127.0.0.1:8000/api/dateevents/",
          "method": "POST",
          "headers": {
            "authorization": "Token " + localStorage.getItem('token'),
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": form
        }

        $.ajax(settings).done(function (response) {
          localStorage.setItem('events', JSON.stringify(JSON.parse(response).events));
          console.log(JSON.stringify(JSON.parse(response).events))
          var events = JSON.parse(response).events.map(function(event, index) {
            return `<div id="${event.pk}">
                    <p style="color: black;">
                      Event description
                    </p>
                    <p>`+event.description+`<br/><br/></p>
                    <p style="color:black;">Location</p>
                    <p>`+event.location+`<br/><br/></p>
                    <p style="color:black;">Start Date </p>
                    <p>`+event.start_date+`<br/><br/></p>
                    <p style="color:black;">End Date</p>
                    <p>`+event.end_date+`<br/><br/></p>
                    <button class="delete_event" value="` +event.pk+`"name="${index}">delete</button> &nbsp;&nbsp;
                    <button class="pq" value="put" name="${index}">put</button>`+"<br/>"+
                    "</div>";
          });
          $("#events").empty();
          $("#events").append(events);
          $(".delete_event").click( function(e) {
            var pk = $(this).val();
            var this_jq = this;
          // console.log($(this).val());

          // e.stopPropagation();
            var events = JSON.parse(localStorage.getItem('events'));
            // console.log(events)
            var settings = {
              "async": true,
              "crossDomain": true,
              "url": "http://127.0.0.1:8000/api/events/" + pk + "/",
              "method": "DELETE",
              "headers": {
                "authorization": "Token " + localStorage.getItem('token')
                  }
            }

            $.ajax(settings).done(function (response) {
              if(response.success === true) {

              alert("Successfully deleted!");  
              }
              else
              {
                alert("Deletion failed!");
              }
              // console.log(response.success);
              // var data = JSON.parse(response)
              // console.log($(this_jq));
              $("#"+pk).remove();
            });
    }); 

    $("button.pq").click( function(e) {
      console.log("put!")
      $("#put").empty();
      $("#put").append(`<h2 id="add_ev">Update Event</h2>`);
      $("#put").append(`
                <form>
                <textarea id="desc_update" placeholder="Description"></textarea>
                <br/>
                <textarea id="loc_update" placeholder="Location"></textarea>
                <br/><br/>
                <label style="color:white;"> Start Date </label><input id="sdate_update" type="date" placeholder="start-date"/>
                <br><br>
                <label style="color:white;"> End Date </label> <input id="edate_update" type="date" placeholder="end-date"/>
                <br><br>
               <input id ="update" type="button" value="Update"/><br>
            </form> `);
      // console.log("put selected_dsfdgfs");
        // e.stopPropagation();
        var events = JSON.parse(localStorage.getItem('events'));
        // console.log(events)



        $("#update").click(function(){
                  var form = new FormData();
                  console.log($("#sdate_update").val())
        form.append("location", $("#loc_update").val());
        form.append("description", $("#desc_update").val());
        form.append("start_date", $("#sdate_update").val());
        form.append("end_date", $("#edate_update").val());
        form.append("all_day", "False");

        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://127.0.0.1:8000/api/events/" + events[0].pk +"/",
          "method": "PUT",
          "headers": {
            "authorization": "Token " + localStorage.getItem('token')
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": form
        }


        $.ajax(settings).done(function (response) {
          var data = JSON.parse(response)
          alert(data.msg);
          $("#put").empty();
          // console.log(response);

        });
        // console.log($("#desc_update").val(), $("#loc_update").val(), $("#sdate_update").val(), $("#edate_update").val())
        });
    }); 


        });
  	    // if ($(this).hasClass('active')){
       //                   $('.dialog').fadeOut(200);
       //        $(this).removeClass('active');
       //    } else {
       //                   $('.dialog').delay(300).fadeIn(200);
       //        $(this).addClass('active');
       //    }
         
         }
   });

    $('.add').click(function(e){
     e.stopPropagation();
     if ($(this).hasClass('active')){
        $('.dialog').fadeOut(200);
        $(this).removeClass('active');
    } else {
        $('.dialog').delay(300).fadeIn(200);
        $(this).addClass('active');
    }
    });
    function closeMenu(){
      $('.dialog').fadeOut(200);

      $('.add').removeClass('active');
  }
  
//   $(document.body).click( function(e) {
//    closeMenu();0
// });

  $(".dialog").click( function(e) {
    e.stopPropagation();
    });

    $("#create").click( function(e) {
        e.stopPropagation();
        var form = new FormData();
        if($('#sdate').val().length === 0) {
          alert('invalid start date!');
          return;
        }
        if($('#edate').val().length === 0) {
          alert('invalid end date!');
          return;
        }
        form.append("description", $('#desc').val());
        form.append("location", $('#loc').val());
        form.append("start_date", $('#sdate').val());
        form.append("end_date", $('#edate').val());

            // form.append("location", "ajmer");
            // form.append("description", "raawan");
            // form.append("start_date", "2017-07-13");
            // form.append("end_date", "2017-07-16");

            var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://127.0.0.1:8000/api/events/",
            "method": "POST",
            "headers": {
                "authorization": "Token " + localStorage.getItem('token')
                },
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            "data": form
            }

        $.ajax(settings).done(function (response) {
          var data = JSON.parse(response)
          alert(data.msg);
          console.log(response);
        });
    });
      
});

    

//fuction to call API
