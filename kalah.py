from copy import copy

class Kalah:
    nextTag = 1

    def __init__(self, board, player, depth=0):  # default depth is 0
        # Board is python list of 14 ints
        self.board = copy(board)
        self.stones = sum(self.board)
        self.half = self.stones / 2.0  # more than half wins
        self.player = player
        self.depth = depth
        self.alpha = -9999  # You want to maximize alpha
        self.beta = 9999  # You want to minimize beta
        self.ivalue = 0  # Initial calculated value
        self.value = 0  # Propagated back from successors
        self.next = None  # Set by func chooseMove
        self.bestMove = None  # Set by func chooseMove
        self.legalMoves()
        self.eval()
        self.tag = Kalah.nextTag
        Kalah.nextTag += 1

    def move(self, index):
        # Clear all locations but put finalVal into last one
        if self.player == 'A':
            myKalah, theirKalah = (0, 7)
        else:
            myKalah, theirKalah = (7, 0)
        board = self.board
        pebbles = board[index]  # get the number of pebbles at the chosen pot
        board[index] = 0  # set the pot you chose to have 0 pebbles
        inMyPots = True  # if the current index is on my side of the board
        while pebbles:  # while there are pebbles left to distribute
            index += 1
            if index > 13:
                index = 0
            if index == theirKalah:
                inMyPots = True
                index += 1  # skip it
            if index == myKalah:
                inMyPots = False
            board[index] += 1  # distribute the pebbles
            pebbles -= 1

        self.legalMoves()  # fill self.moves with possible moves

        if not self.moves:  # if there are no possible moves, like at the end of the game --> capture rest to my kalah
            board[myKalah] += sum(board[myKalah + 1:myKalah + 7])
            board[myKalah + 1:myKalah + 7] = [0] * 6  # set everything else to zero
        elif index == myKalah:  # if the last index is the kalah
            pass  # get to go again
        else:  # if last pebble hits empty
            # that pebble and the opposite are captured and placed into my kalah
            opp = 14 - index  # the opposite index
            if inMyPots:  # if I'm on my own side
                if board[index] == 1 and board[opp] > 0:  # if the index only has one pebble (which is should) and the opposite has more than 0
                    board[myKalah] += board[index] + board[opp]  # add the pebbles to my kalah
                    board[index] = board[opp] = 0  # set index and opposite index to 0
            self.player = self.other()  # now it is the next player's turn

        self.legalMoves()  # fill self.moves with possible moves
        self.eval()

    def other(self):  # set the turn to the opposite letter
        if self.player == 'A':
            return 'B'
        else:
            return 'A'

    def over(self):
        board = self.board
        return (board[0] + board[7] == self.stones) or (self.moves is None)
        # all pebbles are in kalahs or there are no moves left

    def eval(self):
        # if A ahead - positive values, if B ahead - negative
        # kalah A has more than half
        if self.board[0] > self.half:
            val = 100  # Kalah a
        # kalah B has more than half
        elif self.board[7] > self.half:
            val = -100  # Kalah b
        # how far A is ahead of B
        else:
            val = self.board[0] - self.board[7]
        self.ivalue = self.value = val # basically telling you how things are going

    def legalMoves(self):  # populates a list of possible moves
        moves = []
        firstPot = (1, 8)[self.player == 'A']  # if it is A's turn: firstPot is 8, if it is B's turn: firstPot is 1
        for i in range(6):
            if self.board[firstPot + i] > 0:  # if the index has at least one pebble, it is a possible move
                moves.append(firstPot + i)
        self.moves = tuple(moves)
