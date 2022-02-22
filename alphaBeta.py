def chooseMove(Kalah, gnode, maxdepth=6):  # default maxdepth is 6
    # choose bestMove for gnode along with final value
    if gnode.depth < maxdepth and not gnode.over():
        for move in gnode.moves:  # evaluate each possible move
            nextGnode = Kalah(gnode.board, gnode.player, gnode.depth+1)
            nextGnode.move(move)  # make a new Kalah game and make that possible move
            chooseMove(Kalah, nextGnode, maxdepth)  # recurse through the all the possible next moves
            keep = (gnode.next == None)  # 1st of sequence
            if gnode.player == 'A':  # if the computer is A and it is their turn
                if keep or nextGnode.value > gnode.value:
                    gnode.value = nextGnode.value
                    gnode.next = nextGnode
                    gnode.bestMove = move
            else:  # if the computer is B and it is their turn
                if keep or nextGnode.value < gnode.value:
                    gnode.value = nextGnode.value
                    gnode.next = nextGnode
                    gnode.bestMove = move
    return gnode
