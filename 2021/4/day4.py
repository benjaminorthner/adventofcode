with open("input.dat", "r") as file:
    lines = [line for line in file.readlines()]

#load boards
numbers = []
boards = []
current_board = []
cn = "999"

def winner(board):
    for row in range(5):
        if all(list(map(lambda x: x == cn,board[row]))):
            return True

    for col in range(5):
        if all(list(map(lambda x: x==cn, [board[i][col] for i in range(5)]))):
            return True

    return False


for i, line in enumerate(lines):
    line.strip()

    if i == 0:
        numbers = line.split(",")

    line = line.split()

    # if line empty
    if line == [] and i > 1:
        boards.append(current_board)
        current_board = []

    elif i > 1:
        current_board.append(line)

loop_breaker = False
for n in numbers:

    if loop_breaker:
        break

    for board in boards:
        for row in range(5):
            for col in range(5):
                if board[row][col] == n:
                    board[row][col] = cn
    
    # look for winner
    for board in boards:
        if winner(board):
            sum = 0
            for row in range(5):
                for col in range(5):

                    if board[row][col] != cn:
                        sum += int(board[row][col])
            
            print("winner:", int(n) * sum)
            loop_breaker = True
            break


# PART 2
for n in numbers:
    for board in boards:
        for row in range(5):
            for col in range(5):
                if board[row][col] == n:
                    board[row][col] = cn
    
    # look for winner
    for ib, board in enumerate(boards):
        if winner(board) and len(boards) > 1:
            del boards[ib]
            continue

        elif winner(board):
            sum = 0
            for row in range(5):
                for col in range(5):

                    if board[row][col] != cn:
                        sum += int(board[row][col])
            
            print("last winner:", int(n) * sum)
            exit()