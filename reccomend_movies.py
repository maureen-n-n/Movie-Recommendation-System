"""CSC111 Winter 2021 Final Project:

        create_graph.py

===============================

This Python module contains a class much like the Vertex class from the create_graph module
called IdealMovie which represents an ideal movie with attributes based on the user inputs
from the menu module. This class haas a function in which it returns a list of recommended
movies which is what will be the final return of the application.

Within the graph, vertices will have an edge drawn between them if they are deemed as 'similar'.
See the docstring of the function is_similar for the definition of similarity used throughout
this project.


Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Maureen Navera
"""
from __future__ import annotations
from create_graph import Graph


class IdealMovie:
    """ This class represents an ideal movie with elements that the user chose
    in menu.py.
    """
    graph = Graph
    actors: list[str]
    director: str
    genre: list[str]
    rating: int

    def __init__(self, graph: Graph, actors: list[str], director: str, genre: list[str],
                 rating: int) -> None:
        """Initialize a new vertex with the given title, actors, director, genre and rating.

        Preconditions:
            - len(actors) == 4
            - director != ''
            - genre != []
            - 0 <= rating <= 10
        """
        self.graph = graph
        self.actors = actors
        self.director = director
        self.genre = genre
        self.rating = rating

    def find_one_movie(self) -> list:
        """ddd
        """
        recommended = []
        categories = self._specified_categories()

        # Go through the graph and find ONE movie which fits the first specification:
        for title in self.graph.vertices:
            vertex = self.graph.vertices[title]
            if 'actors' in categories:
                if any(vertex.actors) in self.actors:
                    recommended.append(vertex)
                    if len(recommended) == 1:
                        break

            elif 'director' in categories:
                if vertex.director in self.director:
                    recommended.append(vertex)
                    if len(recommended) == 1:
                        break

            elif 'genre' in categories:
                if any(self.genre) in vertex.genre:
                    recommended.append(vertex)
                    if len(recommended) == 1:
                        break

            elif 'rating' in categories:
                if vertex.rating >= self.rating:
                    recommended.append(vertex)
                    if len(recommended) == 1:
                        break
        return recommended

    def find_recommendations(self, recommended) -> list:
        """ Returns a list of recommended movies based on the instance attributes
        of an instance of the IdealMovie class."""
        categories = self._specified_categories()

        if recommended == []:
            neighbours = []
        else:
            neighbours = list(self.graph.get_neighbours(recommended[0].title))

        # iterate through the list of neighbours
        for vertex in neighbours:
            if 'actors' in categories:
                if all(self.actors) in vertex.actors:
                    recommended.append(vertex)
            else:
                recommended.append(vertex)

        for vertex in recommended:
            if 'director' in categories:
                if vertex.director in self.director:
                    pass
                else:
                    recommended.remove(vertex)

        for vertex in recommended:
            if 'genre' in categories:
                if any(self.genre) in self.graph.vertices[vertex].genre:
                    pass
                else:
                    recommended.remove(vertex)

        for vertex in recommended:
            if 'rating' in categories:
                if vertex.rating >= self.rating:
                    pass

                else:
                    recommended.remove(vertex)

        return [vertex.title for vertex in recommended]

    def _specified_categories(self) -> list:
        """asfs"""
        specified_categories = []

        if self.actors == []:
            pass
        else:
            specified_categories.append('actors')

        if self.director == '':
            pass
        else:
            specified_categories.append('director')

        if self.genre == []:
            pass
        else:
            specified_categories.append('genre')

        if self.rating == 0:
            pass
        else:
            specified_categories.append('rating')

        return specified_categories


