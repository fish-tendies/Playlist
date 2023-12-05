# An initial file for the project.
from argparse import ArgumentParser
from itertools import islice
import json
import random
import re
import sys


class Song:
    """Represents a song that olds various musical properties.

    Attirbutes:
        artists(str): the artists involved in the song
        album_name(str): the name of the album the song is under
        track_name(str): the name of the song

        _popularity(int): the rating of popularity based on the dataset
        _duration_ms(int): how long the song is in milliseconds
        _explicit(bool): if the song is explicit or not
        _tempo(int): the song's tempo
        _track_genre(str): The genre that the song belongs in.
    """

    def __init__(self, artists, track_name):
        """Initializes a Song object based on attached dataset's column names.

        Args:
            artists(str): the artists involved in the song
            album_name(str): the name of the album the song is under
            track_name(str): the name of the song


        Side effects:
            Sets attributes for each argument.

        """

        self.artists = artists
        self.track_name = track_name

        # filterable properties
        self.properties = {
            "popularity": 0,
            "duration": 0,
            "explicit": False,
            "tempo": 0,
            "genre": '',
            "album_name": ''
        }

    def __str__(self):
        """Returns an informal string representation of the song,

        Returns:
            str: A string representation of the song.
        """
        return f"'{self.track_name}' by {self.artists}"

    def __repr__(self):
        """Returns a formal string representation for the song.

        Returns:
            str: A formal string representation of the song.
        """
        return f"Song({repr(self.track_name)}, {repr(self.artists)})"


class Playlist:
    """Represents a playlist of songs.

    Attributes:
        song_list(list): a list containing Song objects present in the Playlist.
    """

    def __init__(self):
        """Initializes a Playlist object.

        Args:
            song_list(list): A list of Songs present in the Playlist.

        Side effects: Sets attributes for 'song_list'.
        """
        self.song_list = []
        self.name = ""

    def __str__(self):
        """ Returns an informal string representation of the playlist

        Returns:
            str: A string representation of the playlist.
        """
        playlist = "Playlist: \n"
        for song in self.song_list:
            playlist += f"{song.track_name} by {song.artists}\n"

        return playlist

    def __repr__(self):
        """ Returns a formal string representation of the playlist
        """
        playlist = f"Playlist({self.playlist_name})"

    def __add__(self, other):
        """ Adds two playlists together

        Returns:
            set: A set of songs that are in both playlists.
        """
        new = set(self.song_list) | set(other.song_list)
        new_playlist = Playlist()
        new_playlist.song_list = list(new)
        return new_playlist

    def generate_name(self):  # Devon
        """ Generates a name for the Playlist based off of the shared genre
        properties of Songs in the Playlist.

        Side effects: 
            Updates the value of 'name'.
        """
        genre_set = {}
        for song in self.song_list:
            genre_set.update(song.properties.get("genre"))

        name = f"{max(genre_set)} Mix"

    def add_song(self, song=None, artists=None, track_name=None):  # Ethan
        """
        Adds a song to the playlist

        Args:
            song (obj): the existing song
            artists (str): the artists involved in the song
            track_name (str): the name of the song
        """
        if song is None and artists is None and track_name is None:
            raise ValueError("No values inputted (song, artists, track_name)")
        existing_songs = [song.track_name for song in self.song_list]
        if track_name in existing_songs:
            print(f"The song '{track_name}' already exists in the playlist.")
        else:
            if artists is not None and track_name is not None:
                new_song = Song(artists, track_name)
                self.song_list.append(new_song)
                print("Your song has been added to the Playlist!")
            elif song is not None:
                self.song_list.append(song)

    def remove_song(self, song=None, artists=None, track_name=None, ):
        """
        Remove a song from the Playlist

        Args:
            artists (str): the artists involved in the song
            song (obj): the existing song
            track_name (str): the name of the song
        """
        if song is None and artists is None and track_name is None:
            raise ValueError("No values inputted (song, artists, track_name)")
        existing_songs = [song.track_name for song in self.song_list]
        if track_name in existing_songs:
            if song is not None:
                song = Song(artists, track_name)
                self.song_list.remove(song)
                print(f"'{track_name}' have been removed from the Playlist!")
            else:
                self.song_list.remove(song)
        else:
            raise ValueError("The song is not in the Playlist!")

    def sort_by_popularity(self, ascending=True):
        """ This method can sort the songs by popularity
        Args:
            ascending (bool): If True, sort in ascending order; otherwise, sort in decending order,
        """
        # Sorting the songs based on the populairty attribute of each songs
        self.song_list.sort(key=lambda song: song.popularity,
                            reverse=not ascending)

# Lexin


class User:
    """ A class for users with playlists
    """

    def __init__(self, username):
        self.name = username
        self.playlist = Playlist()

        # A dict of the user's preferences for the playlist
        self.preferences = {

            "popularity": None,
            "duration": None,
            "explicit": None,  # True or False or Unknown
            "genre": None,

        }

    # Sets the user's preferences for the playlist based on dataset column names
    def user_preferences(self, popularity=None,
                         duration=None, explicit=None,
                         genre=None):

        self.preferences["popularity"] = popularity
        self.preferences["duration"] = duration
        self.preferences["explicit"] = explicit
        self.preferences["genre"] = genre

    def generate_queue(self, preference=None, rev=False):  # Devon
        """ Shuffles the order of Songs in the User's Playlist. Can be shuffled 
        randomly or sorted with a user preference and reversed.

        Args:
            preference(str): A preference to sort the Playlist by. 
            Defaults to None.
            reverse(bool): Reverses the order of the newly sorted/shuffled 
            songs. Defaults to False.

        Side effects:
            Updates the value of 'playlist'.
        """
        queue = []
        if (preference is not None):
            queue = sorted(self.playlist.song_list, key=lambda s: s.properties.get(
                preference), reverse=rev)
        else:
            queue.shuffle(self.song_list)
        self.playlist.song_list = queue

# Justin
    def filtered_songs(self, user_preferences):
        """Filters the list of songs based on user-provided criteria

        Returns:
            A refined list of songs that match the user's criteria
        """

        filtered_results = []
        with open("spotifydata.txt") as file:
            for line in file:
                song_data = line.strip().split(',')
                artists, track_name = song_data[0], song_data[2]
                song = Song((artists, track_name))

                if song.song_matches_preferences(song):
                    filtered_results.append(song)
        return filtered_results


def read_songs(filepath):
    """Reads a file and generates Songs.

    Args:
        filepath (str): The path to the file containing raw text data.
    """

    with open("spotifydata.txt") as file:
        for line in islice(file, 1, None):

            pass


def main():
    """The main function of the program.
    """

    print("*" * 20 + "Creating Songs" + "*" * 20)
    song1 = Song("Ariana Grande", "Positions")
    song2 = Song("Ariana Grande", "34+35")
    print(repr(song1))
    print(repr(song2))
    print("*" * 40)

    print("*" * 20 + "Creating Playlist" + "*" * 20)
    playlist = Playlist()
    playlist.add_song(song1)
    playlist.add_song(song2)
    playlist.add_song(artists="Ariana Grande", track_name="POV")
    print(playlist)
    print("*" * 40)
    
    print("*" * 20 + "Creating Playlist 2" + "*" * 20)
    playlist2 = Playlist()
    playlist2.add_song(track_name='Dynamite', artists='BTS')
    playlist2.add_song(track_name='Fake Love', artists='BTS')
    print(playlist2)
    print("*" * 40)
    
    print("*" * 20 + "Adding two playlists" + "*" * 20)
    print(playlist + playlist2)

def parse_args(arglist):
    """ Parses command-line arguments

    Args:
        arglist (list): a list of command-line arguments.
    """
    # parser = ArgumentParser()
    # parser.add_argument("user", help="The user using the Playlist function")
    # parser.add_argument("preferences", help="The user's preferences")
    # parser.add_argument("file_path", help="The path to the raw song data")
    # args = parser.parse_args(arglist)
    # return args


if __name__ == "__main__":
    main()
    # args = parse_args(sys.argv[1:])
    # main(args.user, args.preferences, args.file_path)
