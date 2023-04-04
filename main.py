import json
import threading
import pygame
import socketio

from game.constansts import BALL_SPEED_X, BALL_SPEED_Y, BLACK, LEFT_PADDLE_X, PADDLE_HEIGHT, RIGHT_PADDLE_X, SCREEN_HEIGHT, SCREEN_WIDTH
from game.drawing import draw_paddle, draw_text

isGameReady = False


paddle_positions = {
    0: (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, # Left paddle
    1: (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2  # Right paddle
}

is_player_0 = False

left_score: int = 0
right_score: int = 0


# Create a SocketIO client instance
sio = socketio.Client()

def send_player_move(isUp: bool):
    sio.emit('on_player_move', json.dumps({
        'player': 0 if is_player_0 else 1,
        'isUp': isUp
    }))

# Define the game loop function
def game_loop():
    global isGameReady

    # Initialize Pygame
    pygame.init()
    font = pygame.font.SysFont(None, 48)
    fontA = pygame.font.SysFont(None, 20)

    # Set the dimensions of the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set the title of the window
    pygame.display.set_caption("Pong")

    clock = pygame.time.Clock()

    while True:
        if not isGameReady:
            screen.fill(BLACK)
            draw_text('Esperando Jugador...', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, screen, fontA)
            # Update the screen
            pygame.display.flip()
            continue
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameReady = False
                sio.disconnect()
        
        # Move the paddles based on input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            send_player_move(True)
        if keys[pygame.K_DOWN]:
            send_player_move(False)

        # Clear the screen
        screen.fill(BLACK)

        # Draw the paddles and ball
        left_paddle_y = paddle_positions[0]
        right_paddle_y = paddle_positions[1]

        draw_paddle(LEFT_PADDLE_X, left_paddle_y, screen)
        draw_paddle(RIGHT_PADDLE_X, right_paddle_y, screen)
        # draw_ball(ball_x, ball_y)

        # Draw the score
        draw_text(str(left_score), SCREEN_WIDTH // 4, 10, screen, font)
        draw_text(str(right_score), 3 * SCREEN_WIDTH // 4, 10, screen, font)

        # Update the screen
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)
        


# Define the SocketIO client thread function
def socketio_thread():
    @sio.on('on_player_connected')
    def on_connect(data):
        global is_player_0

        response = json.loads(data)
        is_player_0 = response['player'] == 0

        print('You are player {}'.format(response['player']))
        print('You are connected to the server')

    @sio.on('on_game_is_ready')
    def handle_game_is_ready(_):
        global isGameReady
        isGameReady = True

    @sio.on('on_player_possition_update')
    def handle_player_possition_update(data):
        global paddle_positions
        """
        response = {
            'player': 0,
            'Y_possition': 0,
        }
        """
        response = json.loads(data)
        paddle_positions[response['player']] = response['Y_possition']
        

    # Connect to the SocketIO server
    sio.connect('http://localhost:5000')
    sio.wait()

# Start the game loop on the main thread
threading.Thread(target=game_loop).start()

# Start the SocketIO client thread on a separate thread
threading.Thread(target=socketio_thread).start()
