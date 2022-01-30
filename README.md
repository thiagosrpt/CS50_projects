# thiagosrpt

> Distinctiveness and Complexity

I believe my project satisfies the distinctiveness and complexity requirements proposed because the idea is somewhat different from previous projects of this course. It does use some similar concepts, like using emails to invite users to participate like in the email app, but the concept of randomly presenting restaurants/options of food and creating matches based on the "likes" from participants of an event makes it unique and distinct from other projects.

The complexity comes from the ability to create and edit the event and then build all the functions that will interact with the events created by the user. Also in order to execute this idea, different queries must be done to retrieve the necessary data - The restaurants/places presented within an event must consider what the user is planning on, such as dine-in, pick-up, or delivery (it also prioritizes places that were not voted by the logged-in user yet before its starts repeating/presenting the same venue again). The event matches feature was also challenging as I had to understand how I could build a query to calculate the total of "likes" by restaurant within a given event by using the annotate function and properly serializing the output of the QuerySet it returns. JS is mainly used to display the Create/Edit window, it adjusts the screen to make the scroll bar gets positioned where the Create/Edit window is displayed as well as to commit the creation and edits of a new event. I also used JS to ensure the pages are reloaded when an event is created or edited.

> Purpose / App Use Case

"So, what are we eating?" is an app to help people pick a place for them to eat in which every participant can chime in. One user creates an event and invites other users to participate. From there, the app will randomly present users with place options that fit the criteria entered for the event - like a Tinder for restaurants. Maybe they want to get food delivered or picked up, or perhaps find a place where they can all sit down and have a good time. Based on the user votes, the app will show the matches organized by what's closer and with higher ratings (an event will present the full list of all options that have at least one match, but the closest options, with more matches and better rated, will always be at the top of the list - so a second and third option can also be seen on the list as a backup plan).

> File Description and Contributions

The name of the DJANGO Project is Capstone and within it, I created an app called Milestone - I did not know what app I wanted to build initially, but concluding this course certainly is a 'milestone'. The following are the files I have contributed code for and their contents:

>milestone/views.py
  - The code here was entirely written by me. This contains all the necessary functions to render the pages and retrieve the desired information for the 'ALL EVENTS' page and 'USER'S EVENT PAGES'. This also contains the functions that support the randomization of options within each event as well as the logic that summarizes the likes for each restaurant/food option that the user sees after clicking to see the 'matches' of an event.
  - The functions that created and modify an event can also be seen here.

>milestone/urls.py
  - This contains all the URLs the app pings in order to retrieve data, create or update an object.

>milestone/models.py
  - I have created four tables to support the logic I had in mind for this project and those can be found here.

  - 'Food' table/model: This is used to store all the information about the restaurants and food options - In the real world, this data could be supplied by an API, for instance.

  - 'Event' table/module: This contains the details about an event. Event Name, Organizer, Participants, etc.

  - 'Likes' table/module: This contains the likes given for a single food/restaurant within an event. One record is created to represent the like and the record will contain the USER ID who performed the action, the EVENT this action belongs to, and a checkbox that indicates whether it's a true=like or a false=dislike.

  - 'Users' table/module: this remains the same as standard from DJANGO.

  - 'LikeSerializer' Class: This class was created just so the response obtained by the 'views.py > match function could be serialized properly with the 'total_likes' grouped Restaurants that received likes within an event.

>milestone/static/milestone/index.js
  - This contains all the event listers and functions used to access the functions in views.py. There is a listener function that displays a DIV for when an event needs to be created or modified. A function to delete an event and display an event to ensure the user really wants to delete the event, then once the deletion is confirmed the script will refresh the page.

>milestone/static/milestone/style.css
  - This contains all the CSS used to adjust and modify the structure of the pages.

>milestone/templates/milestone/...

  - event.html > This is a single event view where the user can 'like' and 'dislike' the randomly presented options.

  - index.html > This is the main view where events in which the user participates are listed.

  - matches.html > This is the page on which the total likes by a restaurant for a particular event is summarized. Here is where the user can see which event received the most likes, for instance.

  - new_event.html > This is an overlay page that gets displayed over the main page when the user wishes to modify or create an event.

  - login.html > This is the standard login page, but the layout/design has been changed.

  - resgiter.html > This is the standard register page, but the layout/design has been changed, and FIRST and LAST NAME was added to the registration form.

> Python Packages

Django == 4.0.1

django-rest-framework == 0.1.0

djangorestframework == 3.13.1


>Installation
  1. Clone respository's branch:
  - >git clone --branch web50/projects/2020/x/capstone https://github.com/me50/thiagosrpt.git
  3. cd into project folder (capstone)
  4. Install project requirements:
  - >pip install -r requirements.txt
