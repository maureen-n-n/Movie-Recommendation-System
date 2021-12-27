"""CSC111 Winter 2021 Final Project:

        menu.py

===============================

This Python module contains the code to display a menu using the tkinter library.
This menu will allow users to input which characteristics of certain movies they want to
narrow their search down to in order to create a list of recommended movies based on
the IMDB top 1000 movies dataset.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Maureen Navera
"""

import tkinter as tk
from reccomend_movies import IdealMovie
from create_graph import create_movie_graph, extract_data, Graph

GRAPH = create_movie_graph(extract_data('imdb_top_1000.csv'))
ideal_movie = IdealMovie(graph=GRAPH, actors=[], director='', genre=[], rating=0)


class MovieReviewApplication(tk.Tk):
    """ A class which represents a tkinter menu
    """

    def __init__(self, *args, **kwargs, ) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Movie Review App')

        # Create the container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing the frames as an empty set
        self.frames = {}

        menu = tk.Menu(container)

        # Add a submenu
        submenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(menu=submenu, label="Category")
        submenu.add_command(label="Home", command=lambda: self.show_frame(Startpage))
        submenu.add_command(label="Actors",
                            command=lambda: self.show_frame(Actors))
        submenu.add_command(label="Director",
                            command=lambda: self.show_frame(Director))
        submenu.add_command(label="Rating",
                            command=lambda: self.show_frame(Rating))
        submenu.add_command(label="Genre",
                            command=lambda: self.show_frame(Genre))

        tk.Tk.config(self, menu=menu)

        # iterate through a tuple of all of the pages that have been made
        for F in (Startpage, Actors, Director, Rating):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Startpage)

    def show_frame(self, cont) -> None:
        """ Displays a given frame/page to the user
        """
        frame = self.frames[cont]
        frame.tkraise()


###############################################################################
# The Frames
###############################################################################

class Startpage(tk.Frame):
    """ The starting page that the user will see when they start the application.
    It displays the instructions on how to use the application.
    """

    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to the Movie Recommendation Application!")

        label.pack()
        line = tk.Label(self, text="--------------------------------------------------------")
        line.pack()

        label2 = tk.Label(self, text="In this application, you can specify which attributes"
                                     " of certain movies appeal to you the most")
        label2.pack()

        label3 = tk.Label(self, text="and you will be returned with a list of movies"
                                     "which suit your preferences!")
        label3.pack()
        line2 = tk.Label(self, text="--------------------------------------------------------")
        line2.pack()

        label4 = tk.Label(self, text="To start, click on the top left of this screen and"
                                     " choose a category of a movie ")
        label4.pack()

        label5 = tk.Label(self, text="that you would like to specify and read the instructions"
                                     "on the page that pops up.")
        label5.pack()
        line3 = tk.Label(self, text="--------------------------------------------------------")
        line3.pack()

        label6 = tk.Label(self, text="When you are done, come back to this page by pressing the"
                                     " 'Home' button on each Category page")
        label6.pack()

        label7 = tk.Label(self, text="or by pressing 'Home' on the dropdown menu.")
        label7.pack()
        line4 = tk.Label(self, text="--------------------------------------------------------")
        line4.pack()

        label7 = tk.Label(self, text="Exit the application to find out which movies you"
                                     " should watch next!")
        label7.pack()

        # results = ideal_movie.find_recommendations()
        # result_label = tk.Label(self, text=results)
        #
        # show_results = tk.Button(self, text="Show my results",
        #                          command=result_label.pack())
        # show_results.pack()
        # results = tk.Label(self, text=(ideal_movie.find_recommendations()))
        # results.pack()


class Actors(tk.Frame):
    """ The page that will allow users to choose which actors they are interested in based on
    a specific movie they have specified.
    """

    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.display()

    def display(self) -> None:
        """ Displays the screen containing instructions and input widgets for the user."""
        # Directions for the user
        directions = tk.Label(self,
                              text="Please enter a movie which your actor plays a lead role in:")
        directions.pack()

        movie_frame = tk.Frame(self)
        movie_frame.pack()

        movie = tk.Entry(movie_frame)
        movie.pack()

        label = tk.Label(self)
        label.pack(pady=10)

        def movie_entry() -> None:
            enable = {}

            for actor in GRAPH.vertices[movie.get()].actors:
                enable[actor] = 0

            for actor in enable:
                enable[actor] = tk.IntVar()
                button = tk.Checkbutton(self, text=actor, variable=enable[actor],
                                        command=actor_entry(self, enable=enable, actor=actor))
                button.pack()

        def actor_entry(self, enable, actor) -> None:
            if enable[actor].get() == 1:
                ideal_movie.actors.append(actor)

            label.configure(text="Please select which actors you are interested from "
                                 + movie.get())

        button = tk.Button(movie_frame, text='get entry', command=movie_entry)
        button.pack(pady=10)


class Director(tk.Frame):
    """ The page that will allow users to choose which director they are interested in.
    """
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.display()

    def display(self) -> None:
        """ Displays the screen containing instructions and input widgets for the user."""
        # Directions for the user
        directions = tk.Label(self, text='Please choose a movie that was directed by your director'
                                         ' of choice')
        directions.pack()

        movie_frame = tk.Frame(self)
        movie_frame.pack()

        movie = tk.Entry(movie_frame)
        movie.pack()

        label = tk.Label(self, text="")
        label.pack(pady=10)

        def movie_entry() -> None:
            """ Gets the user input from the label and either returns if that movie is
            in the dataset or not. If so, it configures ideal_movie's director Instance
            Attribute to the director of the movie the user put in.
            """
            title = movie.get()

            if title not in GRAPH.vertices:
                # make new label to say we don't have data for that movie
                warning = tk.Label(self, text="This movie is not in our database! Please choose"
                                              " something else!")
                warning.pack()
            else:
                movie_vertex = GRAPH.vertices[title]
                ideal_movie.director = movie_vertex.director

                label.configure(text="The director you are searching for is "
                                     + movie_vertex.director)

        button = tk.Button(movie_frame, text='get entry', command=movie_entry)
        button.pack(pady=10)


class Rating(tk.Frame):
    """ The page that will allow users to choose the minimum rating of the movie
    """
    def __init__(self, parent, controller) -> None:
        self.entry_frame = self
        tk.Frame.__init__(self, parent)
        self.display()

    def display(self) -> None:
        """ Displays the screen containing instructions and input widgets for the user."""
        # Directions for the user
        directions = tk.Label(self,
                              text="Please choose the minimum score you'd like the movie to have"
                                   " between 1 and 10:")
        directions.pack()

        rating_frame = tk.Frame(self)
        rating_frame.pack()

        rating = tk.Entry(rating_frame)
        rating.pack()

        label = tk.Label(self, text="")
        label.pack()

        def rating_entry() -> None:
            """Gets the user input from the label and either returns if it is a
            valid number or not (0-10). If so, it configures ideal_movie's rating Instance
            Attribute to that number.
            """
            ideal_movie.rating = rating.get()
            warning = tk.Label(self, text="Please enter a number between 0 and 10.")
            if rating.get().isalpha():
                warning.pack()
            elif 0 > int(rating.get()) or int(rating.get()) > 10:
                warning.pack()
            else:
                ideal_movie.rating = int(rating.get())
                label.configure(text="The movie you are searching for must have a rating "
                                     "of at least " + rating.get())

        button = tk.Button(rating_frame, text='get entry', command=rating_entry)
        button.pack(pady=10)


class Genre(tk.Frame):
    """ The page that will allow users to choose which genres they are interested in.
    """
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.display()

    def display(self) -> None:
        """ Displays the screen containing instructions and input widgets for the user."""
        # Directions for the user
        directions = tk.Label(self,
                              text="Please enter a movie with the genre(s)"
                                   " you are interested in watching:")
        directions.pack()

        movie_frame = tk.Frame(self)
        movie_frame.pack()

        movie = tk.Entry(movie_frame)
        movie.pack()

        label = tk.Label(self, text="Hey, welcome to this my GUI")
        label.pack(pady=10)

        def movie_entry() -> None:
            enable = {}

            for genre in GRAPH.vertices[movie.get()].genre:
                enable[genre] = 0

            for genre in enable:
                enable[genre] = tk.IntVar()
                button = tk.Checkbutton(self, text=genre, variable=enable[genre],
                                        command=genre_entry(self, enable=enable, actor=genre))
                button.pack()

        def genre_entry(self, enable, actor) -> None:
            if enable[actor].get() == 1:
                ideal_movie.actors.append(actor)

        button = tk.Button(movie_frame, text='get entry', command=movie_entry)
        button.pack(pady=10)


