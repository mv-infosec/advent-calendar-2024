import socket

def init_chessboard():
    board = [[" " for _ in range(8)] for _ in range(8)]
    board[0][0] = "BR"
    board[0][1] = "BN"
    board[0][2] = "BB"
    board[0][3] = "BQ"
    board[0][4] = "BK"
    board[0][5] = "BB"
    board[0][6] = "BN"
    board[0][7] = "BR"

    for i in range(8):
        board[1][i] = "BP"

    board[7][0] = "WR"
    board[7][1] = "WN"
    board[7][2] = "WB"
    board[7][3] = "WQ"
    board[7][4] = "WK"
    board[7][5] = "WB"
    board[7][6] = "WN"
    board[7][7] = "WR"

    for i in range(8):
        board[6][i] = "WP"

    return board

def send_packet(sock: socket.socket, dst, move, is_white, name): 
    pkt = b"\x80\xcc\x00\x03"
    if is_white:
        pkt += b"\x00\x00\x00\x01"
    else:
        pkt += b"\x00\x00\x00\x00"
    pkt += name.encode("utf8")
    pkt += move.encode("utf8")
    sock.sendto(pkt, dst)

def move_board(board, from_, to):
    from_row = "abcdefgh".index(from_[0])
    from_col = 8 - int(from_[1])

    to_row = "abcdefgh".index(to[0])
    to_col = 8 - int(to[1])

    board[to_col][to_row] = board[from_col][from_row]

    board[from_col][from_row] = " "

def print_board(board):
    for row in board:
        print(*row, sep = "\t")


chess_board = init_chessboard()

is_white = input("White or black? ").lower() == "white"
name = input("Name: ")[:4]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if is_white == True:
    sock.bind(("", 5001))
    peer = input("Peer > ")
    dst = (peer, 2007)
else:
    sock.bind(("", 2007))
    peer = input("Peer > ")
    dst = (peer, 5001)

is_my_move = is_white
print_board(chess_board)

while True:
    if is_my_move:
        move = input("Move (e.g. d2d4): ")
        from_ = move[:2]
        to = move[2:]
        send_packet(sock, dst, move, is_white, name)
        move_board(chess_board, from_, to)
        print_board(chess_board)
    else:
        move = sock.recvfrom(16)[0][12:].decode("utf8")
        from_ = move[:2]
        to = move[2:]
        move_board(chess_board, from_, to)
        print_board(chess_board)
    is_my_move = not is_my_move