"""CSCA08: Fall 2022 -- Assignment 1: What's that Phrase?

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020-2022 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.

"""
import constants
from constants import (POINTS_PER_GUESS, COST_OF_VOWEL, BONUS_POINTS,
                       PLAYER_ONE, PLAYER_TWO, GUESS, BUY, SOLVE,
                       QUIT, SINGLE_PLAYER, PVP, PVE, EASY, HARD,
                       ALL_CONSONANTS, ALL_VOWELS,
                       PRIORITY_CONSONANTS, MYSTERY_CHAR)


# This function is provided as an example.
def winning(mystery_phrase: str, view: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination. That is, if and only if mystery_phrase and view are
    the same.

    >>> winning('parachute', 'parachute')
    True
    >>> winning('game-winner', 'g^^e-w^nner')
    False

    """

    return mystery_phrase == view


# This function is partially provided as an example of calling another
# function as helper.
def game_over(mystery_phrase: str, view: str, move: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination or move is QUIT.

    >>> game_over('center', 'center', 'G')
    True
    >>> game_over('penguin', 'pen^^^n', "Q")
    True
    >>> game_over('men', 'm^^', 'S')
    False

    """

    return move == QUIT or winning(mystery_phrase, view)


def one_player(game_type: str) -> bool:
    """Return True iff game_type is a single player game.

    >>> one_player(SINGLE_PLAYER)
    True
    >>> one_player(PVP)
    False
    >>> one_player(PVE)
    False

    """
    return game_type == SINGLE_PLAYER


# This function is partially provided as an example of using constants
# in the docstring description and specific values in docstring
# examples.
def is_player(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human player
    in a game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is SINGLE_PLAYER, PVP, or PVE.

    In a SINGLE_PLAYER game or a PVP game, a player is always a human
    player. In a PVE game, PLAYER_ONE is a human player and PLAYER_TWO
    is the environment.

    >>> is_player('Player One', 'SP')
    True
    >>> is_player('Player Two', 'PVE')
    False
    >>> is_player('Player Two', 'PVP')
    True

    """

    if game_type == PVP:
        return True
    if game_type == PVE:
        return current_player == PLAYER_ONE
    return game_type == SINGLE_PLAYER


def current_player_score(p1_score: int, p2_score: int,
                         current_player: str) -> int:
    """Return the score of current_player.

    >>> current_player_score(2, 3, PLAYER_ONE)
    2
    >>> current_player_score(2, 3, PLAYER_TWO)
    3

    """

    if current_player == PLAYER_ONE:
        return p1_score
    return p2_score


def adds_points(letter: str, mystery_phrase: str, view: str) -> bool:
    '''Return True if letter is a consonant that is contained in
    mystery_phrase that is also unrevealed in current_view. This determines
    whether letter is awarded bonus points.

    >>> adds_points("c", "car", "^^r")
    True
    >>> adds_points("r", "elephant", "elepha^^")
    False

    '''
    if letter in ALL_CONSONANTS and letter in mystery_phrase:
        if letter not in view:
            return True
    return False


def update_view(mystery_phrase: str, view: str, index: int, guess: str) -> str:
    '''Return the revealed character in mystery_phrase if the guess is correct.

    >>> update_view('lemon', 'le^^^', 2, 'm')
    'm'
    >>> update_view("marriage", "^a^^iage", 0, "n")
    '^'

    '''

    if mystery_phrase[index] == guess and guess not in view:
        view = view[:index] + guess + view[index + 1:]
    return view[index]


def compute_score(current_score: int, revealed_char: int,
                  player_move: str) -> int:
    '''Return the player's new score based on revealed_char and player_move.

    >>> compute_score(3, 2, "G")
    5
    >>> compute_score(4, 1, "B")
    3

    '''

    if player_move == GUESS:
        current_score = (revealed_char * POINTS_PER_GUESS) + current_score
    if player_move == BUY:
        current_score = current_score - COST_OF_VOWEL
    return current_score


def next_turn(current_player: str, revealed_char: int, game_type: str) -> str:
    '''Return who plays the next turn based on current_player and game_type.

    >>> next_turn("Player Two", 3, "PVP")
    'Player Two'
    >>> next_turn("Player One", 0, "PVE")
    'Player Two'
    >>> next_turn('Player Two', 0, 'PVP')
    'Player One'

    '''
    if game_type == SINGLE_PLAYER:
        return PLAYER_ONE
    if revealed_char > 0:
        return current_player
    if revealed_char == 0 and current_player == PLAYER_ONE:
        return PLAYER_TWO
    return PLAYER_ONE


def is_mystery_char(char_index: int, mystery_phrase: str,
                    current_view: str) -> bool:
    '''Return True if char_index in current_view is a mystery
    character.

    >>> is_mystery_char(2, "table", "^^ble")
    False
    >>> is_mystery_char(1, "leg", "l^^")
    True
    >>> is_mystery_char(3, "kettle", 'ket^le')
    False

    '''

    if current_view[char_index] == MYSTERY_CHAR:
        if mystery_phrase[char_index] not in current_view:
            return True
    return False


def environment_solves(current_view: str, game_difficulty: str,
                       consonants_left: str) -> bool:
    '''Return if the environment solves the word based on
    game_difficulty and current_view.

    >>> environment_solves("ast^o^aut", "E", "rn")
    False
    >>> environment_solves("^ang^", "H", "m")
    True
    >>> environment_solves("^a^^oo^", "H", "crtn")
    False
    '''

    if game_difficulty == HARD:
        return half_solved(current_view) or consonants_left == ""
    return game_difficulty == EASY and consonants_left == ""


def delete(string: str, index: int) -> str:
    '''Return string with the letter at index removed.

    >>> delete("men", 2)
    'me'
    >>> delete("lap", 4)
    'lap'

    '''

    if index >= 0:
        return string[:index] + string[index + 1:]
    return string


# This functio
# n is provided as a helper for one of the required functions.
def half_solved(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_solved('')
    True
    >>> half_solved('x')
    True
    >>> half_solved('^')
    False
    >>> half_solved('a^,^c!')
    True
    >>> half_solved('a^b^^e ^c^d^^d')
    False
    """

    num_mystery_chars = view.count(MYSTERY_CHAR)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_mystery_chars


if __name__ == '__main__':
    import doctest

    doctest.testmod()
