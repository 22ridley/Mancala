def chooseMove(Kalah, gnode, maxdepth=6):  # default maxdepth is 6
    # next is a pointer to the chosen child node, so it is set to None after every move
    # each node carries an alpha and beta inherited from above, alpha values only increase and betas only decrease
    # value is the optimal value so far returned from successors

    # alpha and beta: best scores that the other side can acheive

    alpha, beta = (gnode.alpha, gnode.beta)  # inheriting alpha and beta from above
    if gnode.depth < maxdepth and not gnode.over():
        for move in gnode.moves:  # evaluate each possible child node
            nextGnode = Kalah(gnode.board, gnode.player, gnode.depth+1)
            nextGnode.move(move)  # make a new game and make the current possible move
            nextGnode.alpha, nextGnode.beta = (alpha, beta)  # inheriting alpha and beta from above

            chooseMove(Kalah, nextGnode, maxdepth)  # recurse through all possible next moves of nextGnode
            keep = (gnode.next is None)  # if this is the first of the sequence, keep it in case it is the only
            if gnode.player == 'A':  # if it is A's turn (computer or player), you want to maximize value
                if keep or nextGnode.value > gnode.value:  # if this node is better or is the first
                    gnode.value = nextGnode.value
                    gnode.next = nextGnode  # choose this node as the next node
                    gnode.bestMove = move  # choose this move as the next move
                    alpha = max(alpha, gnode.value)
                    if gnode.value >= beta:  # if this option is looking too good, the child node above won't
                        return gnode         # ... choose it because it will be the opposite player, so just return
            else:  # if it is b's turn (computer or player), you want to minimize value
                if keep or nextGnode.value < gnode.value:
                    gnode.value = nextGnode.value
                    gnode.next = nextGnode
                    gnode.bestMove = move
                    beta = min(beta, gnode.value)
                    if gnode.value <= alpha:
                        return gnode
    return gnode
