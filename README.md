# thiagosrpt

- Purpose -

"So, what are we eating?" is an app to help people pick a place for them to eat in which every participant can chime in. One user creates an event and invites other users to participate. From there, the app will randomly present users with place options that fit the criteria entered for the event - like a Tinder for restaurants. Maybe they want to get food delivered or picked up, or perhaps find a place where they can all sit down and have a good time. Based on the user votes, the app will show the matches organized by what's closer and with higher ratings (an event will present the full list of all options that have at least one match, but the closest options, with more matches and better rated will always be at the top of the list - so a second and third option can also be seen on the list as a backup plan).

- Complexity -

The complexity comes from the ability to crate and edit the event. Also in order to execute this idea, different queries must be done to retrieve the necessary data - The restaurantes/places presented within an event must consider what the user is planning on, such as: dine-in, pick-up, or delivery (it also prioritizes places that were not voted by the logged-in user yet before its starts repeating/presenting the same venue again). The event matches feature was also challeing as I had to understand how I could build a query to calculate the total of "likes" by venue/restaurant within a given event by using the annotate fucntion and properly serialize the output of the queryset it returns. JS is mainly used to display the Create/Edit window, it  adjusts the screen to make the scroll bar gets positoned where the Create/Edit window is displaued  as well as to commit the creation and edits of a new event. I also used JS to ensure the pages is reloaded the event is created or edited.

