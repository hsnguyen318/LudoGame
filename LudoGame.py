# Author: Hoang Son Nguyen
# GitHub username: hsnguyen318
# Date: 07/29/2022
# Description: Create the Ludo Game

class LudoGame:
    """
    Represents the Ludo Game class. It will start game play by adding participating players to the game based on
    the list players passed as parameter to the play_game method. It then calls the priority method to decide which
    token to move as the player rolls the dice. Along the way this method also checks if a token can kick another token
    off the board and if two tokens are stacked. After all turns are played, a list of position of players' tokens
    are printed.
    """

    def __init__(self):
        """Initialize the class"""
        self._player_list = {}      # empty list to store objects of participating players
        self._players = []          # players list to be passed as parameter to the play_game method
        self._turns = []            # turns list to be passed as parameter to the play_game method

    def play_game(self, players, turns):
        """
        Start game, passing players and turns arguments, add participating player to player_list dictionary,
        iterate through turns list to move tokens, return list of token position of all players at the end.
        """

        self._players = players     # pass players list to class data member
        self._turns = turns         # pass turns list to class data member

        # default parameters of possible players
        player_a = Player('A', 1, 50, 'HOME', 'HOME', 'IS_PLAYING')
        player_b = Player('B', 15, 8, 'HOME', 'HOME', 'IS_PLAYING')
        player_c = Player('C', 29, 22, 'HOME', 'HOME', 'IS_PLAYING')
        player_d = Player('D', 43, 36, 'HOME', 'HOME', 'IS_PLAYING')

        # if player found in players list, add player object to player list dictionary
        if 'A' in self._players:
            self._player_list['A'] = player_a
        if 'B' in self._players:
            self._player_list['B'] = player_b
        if 'C' in self._players:
            self._player_list['C'] = player_c
        if 'D' in self._players:
            self._player_list['D'] = player_d

        # call and pass parameters to move_token
        for turn in self._turns:
            self.priority(self.get_player_by_position(turn[0]), turn[1])
        # return result of tokens' position
        result = list()
        for player in self._player_list.values():
            result.append(player.get_space_p())
            result.append(player.get_space_q())
        return result

    def check_to_kick(self, player, steps):
        """Method to check if a kick is possible. Parameters are player object and number of steps based on roll."""
        # create variables to store the new space of player's token if it moves steps steps
        # + 1 is added to account for 'H' and 'R' space which are the first two spaces in a player's map list
        # whereas get_token_p(q)_step_count method is the distance from space 'R'
        player_new_space_p = player.get_map()[player.get_token_p_step_count() + steps + 1]
        player_new_space_q = player.get_map()[player.get_token_q_step_count() + steps + 1]

        # iterate through player list for other player object
        for other_player in self._player_list.values():
            # exclude player's self
            if other_player != player:
                # variables to store current space on the board of opponents' tokens
                oppo_space_p = other_player.get_space_p()
                oppo_space_q = other_player.get_space_q()
                # if the new space of any tokens of player is the same with the
                # current space of any other players' tokens - return True, else - False
                if player_new_space_p == oppo_space_p or player_new_space_p == oppo_space_q or \
                        player_new_space_q == oppo_space_p or player_new_space_q == oppo_space_q:
                    return True
                else:
                    return False

    def kick(self, player, steps):
        """
        If the check_to_kick method is True, player's token kicks another player's token in steps.
        Passed parameters are player object and number of steps based on roll.
        """
        # if check_to_kick method is True:
        if self.check_to_kick(player, steps) is True:
            # iterate through player list for other player objects:
            for other_player in self._player_list.values():
                # ensure player does not kick his own token
                if other_player != player:
                    # variables for player and opponents token space to simplify code
                    # current space of opponents' tokens
                    oppo_space_p = other_player.get_space_p()       # Op = Opponent's p token
                    oppo_space_q = other_player.get_space_q()       # Oq = Opponent's q token
                    # new spaces of player's tokens if they move steps steps
                    # + 1 is added to account for 'H' and 'R' space which are the first two spaces in a player's map
                    # whereas get_token_p(q)_step_count method is the distance from space 'R'
                    # Pnp = Player token p new space
                    player_new_space_p = player.get_map()[player.get_token_p_step_count() + steps + 1]
                    # Pnq = Player token q new space
                    player_new_space_q = player.get_map()[player.get_token_q_step_count() + steps + 1]

                    # if space name on player map of current step count of token p + steps (roll) matches with
                    # the space name from the other player map, move player token by steps (execute the kick)
                    # and move the opponent's token home

                    # if Pnp = Pnq = Op = Oq:
                    if oppo_space_p == player_new_space_p and oppo_space_q == player_new_space_p and \
                            oppo_space_p == player_new_space_q and oppo_space_q == player_new_space_q:
                        player.move_token_p(steps)      # move player token p by steps
                        player.move_token_q(steps)      # move player token q by steps
                        other_player.kick_home_p()      # send other player token p home
                        other_player.kick_home_q()      # send other player token q home

                    # If Pnp = Pnq = Op (if player's tokens are stacked):
                    elif oppo_space_p == player_new_space_p and oppo_space_p == player_new_space_q:
                        player.move_token_p(steps)      # move player token p by steps
                        player.move_token_q(steps)      # move player token q by steps
                        other_player.kick_home_p()      # send other player token p home

                    # If Pnp = Pnq = Oq (if player's tokens are stacked):
                    elif oppo_space_q == player_new_space_p and oppo_space_q == player_new_space_q:
                        player.move_token_p(steps)      # move player token p by steps
                        player.move_token_q(steps)      # move player token q by steps
                        other_player.kick_home_q()      # send other player token q home

                    # If Pnp = Op and Pnp = Oq (if opponent's tokens are stacked)
                    elif oppo_space_p == player_new_space_p and oppo_space_q == player_new_space_p:
                        player.move_token_p(steps)      # move player token p by steps
                        other_player.kick_home_p()      # send other player token p home
                        other_player.kick_home_q()      # send other player token q home

                    # If Pnq = Op and Pnq = Oq (if opponent's token are stacked)
                    elif oppo_space_p == player_new_space_q and oppo_space_q == player_new_space_q:
                        player.move_token_q(steps)
                        other_player.kick_home_p()      # send other player token p home
                        other_player.kick_home_q()      # send other player token q home

                    # If Pnp = Op:
                    elif oppo_space_p == player_new_space_p:
                        player.move_token_p(steps)      # move player token p by steps
                        other_player.kick_home_p()      # send other player token p home

                    # If Pnp = Oq:
                    elif oppo_space_q == player_new_space_p:
                        player.move_token_p(steps)      # move player token p by steps
                        other_player.kick_home_q()      # send other player token q home

                    # If Pnq = Op:
                    elif oppo_space_p == player_new_space_q:
                        player.move_token_q(steps)      # move player token q by steps
                        other_player.kick_home_p()      # send other player token p home

                    # If Pnq = Oq:
                    elif oppo_space_q == player_new_space_q:
                        player.move_token_q(steps)      # move player token q by steps
                        other_player.kick_home_q()      # send other player token q home

        # if check_to_kick method is not True, pass:
        else:
            pass

    def move_token(self, player, token_name, steps):
        """
        Move token p or q depending on the priority method which runs the priority rule.
        """
        # If token name is p:
        if token_name == 'p':
            # variable to store current index of token p on the map, for example space 1 of player A has an index of 2
            player_p_token_index = player.get_map().index(player.get_space_p())
            # if index + steps > 57, which means token will bounce back from E (index of A6, for example, is 57)
            if player_p_token_index + steps > 57:
                # variable for the distance between current space and 'E'
                dist_to_end = player.get_map().index('E') - player.get_map().index(player.get_space_p())
                # bounce back token
                player.move_token_p(2 * dist_to_end - steps)
            else:
                # else, move token by steps
                player.move_token_p(steps)

        # If token name is q:
        if token_name == 'q':
            # variable to store current index of token q on the map, for example space 1 of player A has an index of 2
            player_q_token_index = player.get_map().index(player.get_space_q())
            # if index + steps > 57, which means token will bounce back from E (index of A6, for example, is 57)
            if player_q_token_index + steps > 57:
                # variable for the distance between current space and 'E'
                dist_to_end = player.get_map().index('E') - player.get_map().index(player.get_space_q())
                # bounce back token
                player.move_token_q(2 * dist_to_end - steps)
            else:
                # else, move token by steps
                player.move_token_q(steps)

    def priority(self, player, steps):
        """
        Set priority rule to decide which token to move based on player's dice rolls.
        Parameters are player objects and number of steps based on roll.
        """
        # if player has finished game, pass
        if player.get_completed() is True:
            pass
        # Else, if player is still playing
        else:
            # if two tokens are stacked:
            if player.get_space_p() != 'H' and player.get_space_p() == player.get_space_q() and \
                    player.get_space_p() != 'R':
                # situation of rolling 6 is not needed because since tokens are stacked, they must not be home

                # if neither token is Home, get them to E space if it's an exact roll if possible
                if player.get_token_p_step_count() + steps == 57:
                    self.move_token(player, 'p', steps)
                    self.move_token(player, 'q', steps)
                # attempt to kick other tokens if possible
                elif self.check_to_kick(player, steps) is True:
                    self.kick(player, steps)
                # else, move tokens
                else:
                    self.move_token(player, 'p', steps)  # move player token p by steps
                    self.move_token(player, 'q', steps)  # move player token q by steps

            # else if tokens are not stacked
            else:
                # if steps = 6:
                if steps == 6:
                    # 1st rule, get any remaining token out of Home
                    if player.get_space_p() == 'H':
                        self.move_token(player, 'p', 1)
                    elif player.get_space_q() == 'H':
                        self.move_token(player, 'q', 1)
                    # 2nd rule, if neither token is Home, get them to E space if it's an exact roll
                    elif player.get_token_p_step_count() == 51:
                        self.move_token(player, 'p', 6)
                    elif player.get_token_q_step_count() == 51:
                        self.move_token(player, 'q', 6)
                    # 3rd rule, kick an opponent if possible
                    elif self.check_to_kick(player, 6) is True:
                        self.kick(player, 6)
                    # 4th rule, move the token with the lower step count
                    else:
                        if player.get_token_p_step_count() < player.get_token_q_step_count():
                            self.move_token(player,'p', steps)
                        else:
                            self.move_token(player,'q', steps)
                # if roll is not 6:
                elif steps != 6:
                    # if both tokens are home, pass since player can't move
                    if player.get_space_p() == 'H':
                        if player.get_space_q() == 'H':
                            pass
                        # if p is home but q is not:
                        elif player.get_space_q() != 'H':
                            # move p to 'E' if possible
                            if player.get_token_q_step_count() + steps == 57:
                                self.move_token(player,'q', steps)
                            # else, kick opponent's token
                            elif self.check_to_kick(player, steps) is True:
                                # if there is no exact move to E, kick an opponent if possible
                                self.kick(player, steps)
                            # else, move q
                            else:
                                self.move_token(player,'q', steps)
                    # if p is not home:
                    elif player.get_space_p() != 'H':
                        # and if q is home:
                        if player.get_space_q() == 'H':
                            # move p to 'E' on exact roll if possible
                            if player.get_token_p_step_count() + steps == 57:
                                self.move_token(player,'p', steps)
                            # else, kick opponent's token if possible
                            elif self.check_to_kick(player, steps) is True:
                                # if there is no exact move to E, kick an opponent if possible
                                self.kick(player, steps)
                            # else, move p
                            else:
                                self.move_token(player,'p', steps)
                        # if q is not home (both tokens are active)
                        elif player.get_space_q() != 'H':
                            # move token p or q to 'E' on exact roll
                            if player.get_token_p_step_count() + steps == 57:
                                self.move_token(player,'p', steps)
                            elif player.get_token_q_step_count() + steps == 57:
                                self.move_token(player, 'q', steps)
                            # else, kick opponent's token if possible
                            elif self.check_to_kick(player, steps) is True:
                                # if there is no exact move to E, kick an opponent if possible
                                self.kick(player, steps)
                            # else, move token with lower step count
                            elif player.get_token_p_step_count() <= player.get_token_q_step_count():
                                self.move_token(player,'p', steps)
                            else:
                                self.move_token(player,'q', steps)

    def get_player_by_position(self, player_pos):
        """Return player object based on position."""
        if player_pos in self._player_list:
            return self._player_list[player_pos]
        else:
            return 'Player not found!'


class Player:
    """
    Represent the player class. This class contains key information that define a player: chosen position (‘A’, ‘B’),
     start and end space (i.e. 1 and 50 for player at position A), current position of token p and q (‘HOME’ or
     ‘READY’), player map showing which space on the board the player can step into, which is different for each player,
      and dictionary to match a player to the corresponding map.
      """
    def __init__(self, chosen_pos, start_space, end_space, curr_pos_p, curr_pos_q, curr_state):
        self._chosen_pos = chosen_pos       # like 'A', 'B'....
        self._start_space = start_space     # 1 for player A, 15 for player B...
        self._end_space = end_space         # 50 for player A, 8 for player B
        self._curr_pos_p = curr_pos_p       # 'HOME'
        self._curr_pos_q = curr_pos_q       # 'HOME'
        self._curr_space_p = 'H'
        self._curr_space_q = 'H'
        self._curr_state = curr_state       # 'IS_PLAYING'
        self._a_map = ['H', 'R', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                       '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                       '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                       '50', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'E', '*', '*', '*', '*', '*', '*']
        self._b_map = ['H', 'R', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                       '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46',
                       '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '1', '2', '3', '4', '5', '6', '7',
                       '8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'E', '*', '*', '*', '*', '*', '*']
        self._c_map = ['H', 'R', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
                       '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '1', '2', '3', '4', '5',
                       '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                       '22', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'E', '*', '*', '*', '*', '*', '*']
        self._d_map = ['H', 'R', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '1', '2',
                       '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                       '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
                       '35', '36', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'E', '*', '*', '*', '*', '*', '*']

        self._map_match = {'A': self._a_map, 'B': self._b_map, 'C': self._c_map, 'D': self._d_map}

    def get_map(self):
        """Return the map corresponding to the player with player object as the parameter."""
        return self._map_match[self._chosen_pos]

    def get_space_p(self):
        """Return current space of token p on board."""
        return self._curr_space_p

    def get_space_q(self):
        """Return current space of token q on board."""
        return self._curr_space_q

    def kick_home_p(self):
        """Reset space of token p to 'H' if it was kicked off the board."""
        self._curr_space_p = 'H'        # reset space to 'H'
        self._curr_pos_p = 'HOME'       # reset position to 'HOME'

    def kick_home_q(self):
        """Reset space of token q to 'H' if it was kicked off the board."""
        self._curr_space_q = 'H'        # reset space to 'H'
        self._curr_pos_q = 'HOME'       # reset position to 'HOME'

    def get_completed(self):
        """Return True if the player has finishes the game, False if not"""
        if self._curr_space_p == 'E' and self._curr_space_q == 'E':
            self._curr_state = 'FINISHED'
            return True
        else:
            return False

    def get_token_p_step_count(self):
        """Get the steps taken by token p."""
        if self._curr_space_p == "H":     # if current space is Home, step count = -1
            return -1
        if self._curr_space_p == "R":     # if current space is Ready to go, step count = 0
            return 0
        # else, steps taken equal to index of current space minus index of 'R' on the map corresponding to the player
        else:
            return self._map_match[self._chosen_pos].index(self._curr_space_p) \
                   - self._map_match[self._chosen_pos].index('R')

    def get_token_q_step_count(self):
        """Get the steps taken by token q."""
        if self._curr_space_q == "H":     # if current space is Home, step count = -1
            return -1
        if self._curr_space_q == "R":     # if current space is Ready to go, step count = 0
            return 0
        # else, steps taken equal to index of current space minus index of 'R' on the map corresponding to the player
        else:
            return self._map_match[self._chosen_pos].index(self._curr_space_q) \
                   - self._map_match[self._chosen_pos].index('R')

    def move_token_p(self, steps):
        """Move token p by steps."""
        # increment current space of token p to the value in corresponding player map by steps
        self._curr_space_p = self._map_match[self._chosen_pos][
            self._map_match[self._chosen_pos].index(self._curr_space_p) + int(steps)]
        # update current position of token to home, ready, on board or end based on position on the player map
        if self._map_match[self._chosen_pos].index(self._curr_space_p) == 0:
            self._curr_pos_p = 'HOME'
        elif self._map_match[self._chosen_pos].index(self._curr_space_p) == 1:
            self._curr_pos_p = 'READY'
        elif self._map_match[self._chosen_pos].index(self._curr_space_p) <= 57:
            self._curr_pos_p = 'ON_BOARD'
        else:
            self._curr_pos_p = 'END'

    def move_token_q(self, steps):
        """Move token q by steps."""
        # increment current space of token q to the value in corresponding player map by steps
        self._curr_space_q = self._map_match[self._chosen_pos][
            self._map_match[self._chosen_pos].index(self._curr_space_q) + steps]
        # update current position of token to home, ready, on board or end based on position on the player map
        if self._map_match[self._chosen_pos].index(self._curr_space_q) == 0:
            self._curr_pos_q = 'HOME'
        elif self._map_match[self._chosen_pos].index(self._curr_space_q) == 1:
            self._curr_pos_q = 'READY'
        elif self._map_match[self._chosen_pos].index(self._curr_space_q) <= 57:
            self._curr_pos_q = 'ON_BOARD'
        else:
            self._curr_pos_q = 'END'

    def get_space_name(self, total_steps):
        """Return token's space name based on steps taken."""
        # Return the item at index + 1 position on the player map, as the first two positions are 'H' & 'R'
        # For example, at total steps = 3, the function will return the space at index 4, which is space '3'
        return self._map_match[self._chosen_pos][total_steps + 1]

# try calling these steps
players = ['A', 'B']
turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4), ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
game = LudoGame()
current_tokens_space = game.play_game(players, turns)
player_A = game.get_player_by_position('A')
print(player_A.get_completed())
print(player_A.get_token_p_step_count())
print(current_tokens_space)
player_B = game.get_player_by_position('B')
print(player_B.get_space_name(55))
