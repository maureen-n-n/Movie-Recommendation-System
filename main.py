"""CSC111 Winter 2021 Final Project:

        main.py

===============================
This module imports and calls all the files and functions that are needed to
to run the project from start to finish. When run, the other modules will
load necessary files from the datasets that have been downloaded,
perform computations with these datasets, and produce an interactive menu
for the user to navigate.

-------------------NAVIGATING THE MENU-------------------
When this module is run, you will be met with a menu (using pygame's menu library)
that prompts you to choose whether you want to display a graph which represents
CO2eq Emissions per year, a graph which represents the percent change in CO2eq
Emissions per year, or a graph which compares the percent change in CO2eq per year
for a given industry for all of the Regions looked at in this project.
The label under the buttons also explains the buttons and what kinds of graphs they
will display.



Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Maureen Navera
"""
from menu import MovieReviewApplication, ideal_movie
from reccomend_movies import IdealMovie


app = MovieReviewApplication()
app.geometry("700x700")
app.mainloop()
print(ideal_movie.find_recommendations(ideal_movie.find_one_movie()))
