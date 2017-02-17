HOMEPAGE URL
http://127.0.0.1:8000/api/index/ (local server)

DESCRIPTION

This is the code repo for a online calender synced with google calender. It uses Google APIs.
Using this app you can create, update and post events from the google calender
and sync the events with your calender and vice versa

KEY_FEATURES

Used Django REST framework with token based authentication system
Implemented Google OAUTH
API's are RESTFUL and they use rest protocol to it's best

Create a Django Super User

API_ENDPOINTS
http://127.0.0.1:8000/api/gsignup -- Googe Sign Up
	method "GET"

After gsignup login to your django admin and copy your token

http://127.0.0.1:8000/api/sync -- Synchronise calender with google calender
    method : "GET"
    Headers : Authorization Token

http://127.0.0.1:8000/api/dateevents -- return events with respect to a date
    method : "POST"
    Headers : Authorization Token
    body : 
    	date : string format YYYY-MM-DD

http://127.0.0.1:8000/api/events -- post events on your calender
    method : "POST"
    Headers : Authorization Token
    body: 
    	location: string
    	description: string
    	start_date: string format YYYY-MM-DD
    	end_date: string format YYYY-MM-DD

http://127.0.0.1:8000/api/events/pk -- put and update events on your calender based on the pk of event
    method : "PUT"
    Headers : Authorization Token
    body:
    	location: string
    	description: string
    	start_date: string format YYYY-MM-DD
    	end_date: string format YYYY-MM-DD

    method : "DELETE"
    Headers : Authorization Token

Insatllation
Setting a virtual environment for your code.
Running makemigrations and migrate command by going into the root directory
Start your local Django server

FLOW
Go to the homepage url described above
sign in to the gogle to confirm authentication
It will redirect you to the main page of the application
CLick on the date button twice to see the Add Event dialog box 
AS u will click on the date events related to the date will be shown in the sidebar
You can see the results of your calls in the console as the UI is not as much efficient based on the design
You can also use postman to verify the apis

UI may not be as efficient Testing through postman is recommended