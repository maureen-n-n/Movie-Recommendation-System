"""CSC111 Winter 2021 Final Project:

        create_graph.py

===============================

This Python module contains a modified graph and vertex class which will be the basis of this
project. Each vertex will represent a movie from the IMDB dataset and the graph will contain
every vertex entry. See docstrings for vertex and graph class below for further details and
instance attributes of each class.

Within the graph, vertices will have an edge drawn between them if they are deemed as 'similar'.
See the docstring of the function is_similar for the definition of similarity used throughout
this project.


Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Maureen Navera
"""

from __future__ import annotations
import csv
from typing import Any

###############################################################################
# Making the Movie Graph
###############################################################################

class _Vertex:
    """A vertex in a movie graph which is used to represent a movie entry.

    Instance Attributes:
        - title:
            The name of the movie
        - actors
            A list of the four main actors from the movie
        - director
            The director of the movie
        - genre
            A list of all of the genres of the movie
        - rating
            an integer representing the rating of the movie (0-10)
        - higher_rating
            A set of movie vertices that are 'similar' to this movie and have a higher rating
        - neighbours
            Other movie vertices that this movie has been deemed as 'similar' to.
    Representation Invariants:
        - self.title != ''
        - self.len(actors) == 4
        - self.director != ''
        - self.genre != []
        - 0 <= self.rating <= 10
        - self not in self.neighbours
        - all(movie in self.neighbours for movie in self.higher_rating)
    """
    title: str
    actors: list[str]
    director: str
    genre: list[str]
    rating: int
    higher_rating: set[_Vertex]
    neighbours: set[_Vertex]

    def __init__(self, title: str, actors: list[str], director: str, genre: list[str],
                 rating: int) -> None:
        """Initialize a new vertex with the given title, actors, director, genre and rating.

        This vertex is initialized with no neighbours and no vertices in higher_rating.

        Preconditions:
            - title != ''
            - len(actors) == 4
            - director != ''
            - genre != []
            - 0 <= rating <= 10
        """
        self.title = title
        self.actors = actors
        self.director = director
        self.genre = genre
        self.rating = rating

        self.higher_rating = set()
        self.neighbours = set()


class Graph:
    """A graph used to represent a network of movie data.
    """
    # Private Instance Attributes:
    #     - vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, title: str, actors: list[str], director: str, genre: list[str],
                   rating: int) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if title not in self.vertices:
            self.vertices[title] = _Vertex(title, actors, director, genre, rating)

    def add_edge(self, title1: Any, title2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Add the vertex corresponding to title2 to the vertex of title1's movie's higher_rating
        instance attribute if title2's rating is greater than title1's

        Similarly, add the vertex corresponding to title1 to the vertex of title2's movie's
        higher_rating instance attribute if title1's rating is greater than title2's

        Raise a ValueError if title1 or title2 do not appear as vertices in this graph.

        Preconditions:
            - title1 != title2
        """
        if title1 in self.vertices and title2 in self.vertices:
            v1 = self.vertices[title1]
            v2 = self.vertices[title2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)

            if v1.rating > v2.rating:
                v2.higher_rating.add(v1)
            elif v2.rating < v1.rating:
                v1.higher_rating.add(v2)

        else:
            raise ValueError

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self.vertices:
            v = self.vertices[item]
            return {neighbour for neighbour in v.neighbours}
        else:
            raise ValueError


###############################################################################
# Reading the dataset and Creating a Graph from it
###############################################################################

def extract_data(dataset: str) -> list:
    """ This function reads the given dataset and returns it as a list

    Preconditions:
        - dataset != ''
    """
    movie_data = []
    with open(dataset, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            movie_data.append(row)

    return movie_data


def create_movie_graph(lst: list) -> Graph:
    """ This function creates a graph based on the movie data from the given list.

    Vertices representing each entry in the list (excluding the first which are titles) are
    created and added to a graph which will be returned.

    This function uses the helper function is_similar to determine which vertices to draw
    edges between.
    """
    graph = Graph()
    for entry in lst[1:]:
        title = entry[1]
        actors = [entry[10], entry[11], entry[12], entry[13]]
        director = entry[9]
        genre = entry[5].split(', ')
        rating = round(float(entry[6]))

        graph.add_vertex(title, actors, director, genre, rating)

    is_similar(graph)

    return graph


def is_similar(graph: Graph) -> None:
    """ This function determines whether a two vertices in a given graph are 'similar'

    ---------- Definition of 'similar' ----------
    Two vertices are defined as similar when:
        - they share at least one of the same actors
        OR
        - they share the same director
        OR
        - they share at least one of the same genres
        OR
        - they are equal in rating. If one vertex has a higher rating than another, they
        are still considered to be 'similar', however, the vertex with the higher rating
        will be added to the lower rating vertex's higher_rating instance attribute (this
        will be accomplished when calling Graph.add_edge on those two vertices)

    If two vertices are deemed as similar, then an edge is created between those two
    vertices in the graph.
    """
    vertices = graph.vertices

    for title1 in vertices:
        for title2 in vertices:
            if (actor in vertices.get(title2).actors for actor in vertices.get(title1).actors):
                # At least one same actor
                graph.add_edge(title1, title2)

            elif vertices.get(title1).director == vertices.get(title2).director:
                # Same director
                graph.add_edge(title1, title2)

            elif (genre in vertices.get(title2).genre for genre in vertices.get(title1).genre):
                # At least one same genre
                graph.add_edge(title1, title2)

            elif vertices.get(title1).rating >= vertices.get(title2).rating:
                # Same or greater rating
                graph.add_edge(title1, title2)


python_ta.check_all(config={
    'extra-imports': [],  # the names (strs) of imported modules
    'allowed-io': [],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['E1136']
})
