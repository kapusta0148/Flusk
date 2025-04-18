from flask import Flask, request, jsonify
import chess
import chess.svg
import chess.pgn
import io

app = Flask(__name__)
board = chess.Board()


@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Интерактивные шахматы</title>
        <style>
            #chessboard {
                width: 400px;
                height: 400px;
                margin: 20px;
            }
            .piece {
                cursor: grab;
            }
            .square {
                width: 50px;
                height: 50px;
            }
        </style>
    </head>
    <body>
        <div id="chessboard"></div>
        <div id="status"></div>
        <button onclick="resetGame()">Новая игра</button>

        <script>
            let selectedPiece = null;

            function loadBoard() {
                fetch('/get_board')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('chessboard').innerHTML = data.svg;
                        document.getElementById('status').innerHTML = data.status;
                        addDragAndDrop();
                    });
            }

            function addDragAndDrop() {
                const pieces = document.querySelectorAll('.piece');
                pieces.forEach(piece => {
                    piece.addEventListener('mousedown', startDrag);
                });

                const squares = document.querySelectorAll('.square');
                squares.forEach(square => {
                    square.addEventListener('mouseup', dropPiece);
                });
            }

            function startDrag(e) {
                selectedPiece = e.target;
            }

            function dropPiece(e) {
                if (!selectedPiece) return;

                const fromSquare = selectedPiece.parentElement.getAttribute('data-square');
                const toSquare = e.target.getAttribute('data-square');

                fetch(`/make_move?from=${fromSquare}&to=${toSquare}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            loadBoard();
                        } else {
                            alert(data.message);
                        }
                    });

                selectedPiece = null;
            }

            function resetGame() {
                fetch('/reset_game')
                    .then(() => loadBoard());
            }

            // Загружаем доску при старте
            loadBoard();
        </script>
    </body>
    </html>
    """


@app.route('/get_board')
def get_board():
    svg = chess.svg.board(board=board, size=400)
    status = get_game_status()
    return jsonify({'svg': svg, 'status': status})


@app.route('/make_move')
def make_move():
    from_square = request.args.get('from')
    to_square = request.args.get('to')

    try:
        move = chess.Move.from_uci(f"{from_square}{to_square}")
        if move in board.legal_moves:
            board.push(move)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Недопустимый ход!'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Неверный формат хода'})


@app.route('/reset_game')
def reset_game():
    global board
    board = chess.Board()
    return '', 204


def get_game_status():
    if board.is_checkmate():
        return "Мат! " + ("Белые выиграли" if board.turn == chess.BLACK else "Чёрные выиграли")
    elif board.is_stalemate():
        return "Пат!"
    elif board.is_insufficient_material():
        return "Недостаточно материала для мата"
    elif board.is_check():
        return "Шах! Ход " + ("белых" if board.turn == chess.WHITE else "чёрных")
    else:
        return "Ход " + ("белых" if board.turn == chess.WHITE else "чёрных")


if __name__ == '__main__':
    app.run(debug=True)