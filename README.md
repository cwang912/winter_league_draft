Web application for 2016 Winter League draft
=======================

This web application is built using Flask and Python. The players entering the draft (including baggages, ratings, captains, gender, etc.) are read from a CSV file using the pandas library, and are drafted into 8 teams by a user. As of now there is no method of exporting the results of the draft, but that functionality is a planned feature.

## Features

On the top left of the page are sortable totals for each team, sums of male, female, and team ratings. The team with the lowest total at each section of the draft (predraft, women's, and men's) should be auto-selected as the team to draft on the right, however a dropdown menu allows the user to select the drafting team, either in case of ties or logic failure.

There is a sortable/searchable list of draftable players and baggages, clicking on a player is required to select the next pick, and a draft button adds the player to the team.

On the bottom, taking up the most space, are the team rosters.

## Technologies

Most of this is built with Flask in Python, using HTML for the webpage, and a dose of jQuery for the sortable tables. Teams are stored in a class with functionality to add, subtract, or list team members, and with lots of probably inefficient pandas checks for names and player IDs. The page redirects to the same page after drafting, since the form submission is used to add players. It is likely possible to do this without having to reload a page, but not as it is currently built. Determining a more efficient way of transferring data from the user to the back-end logic would be great for me to work on and understand.

Additionally, reloading the page will undo the draft picks, so be careful.


## Deployment

It is currently available on a Heroku instance, see https://winter-league-2016.herokuapp.com/winter-league
