import pygame
import random
import time
# Initialize Pygame
pygame.init()

# Constants for toast message
TOAST_COLOR = (255, 255, 0)  # Yellow color for the toast message background
TOAST_WIDTH = 400  # Width of the toast message box
TOAST_HEIGHT = 50  # Height of the toast message box
Total_move=0

# Set up the game window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Red Blue Number Game")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Font
font = pygame.font.Font(None, 36)
# Global arrays to store the generated permutation and elements of two types

global_filtered_elements1 = []
global_filtered_elements2 = []

# Function to generate a random permutation of balls and filter elements
def generate_permutation(num_balls):
    global global_permutation, global_filtered_elements1, global_filtered_elements2

    ball_radius = 30
    permutation = []
    filtered_elements1 = []
    filtered_elements2 = []
    while True:
        permutation = random.sample(range(1, num_balls + 1), num_balls)
        filtered_elements1 = [num for num, ind in enumerate(permutation) if num != ind + 1]
        filtered_elements2 = [num for num, ind in enumerate(permutation) if num != num_balls - ind]
        if any(filtered_elements1) and any(filtered_elements2):
            break
    colors = [RED] * num_balls
    ball_centers = [(ball_radius + i * 2 * ball_radius, window_height // 2) for i in range(num_balls)]

    # Assign the generated permutation and filtered elements to the global variables
    global_permutation = permutation
    global_filtered_elements1 = filtered_elements1
    global_filtered_elements2 = filtered_elements2
    
    #toast(f"Filtered Elements 1: {global_filtered_elements1}", BLUE, 350)
    #toast(f"Filtered Elements 2: {global_filtered_elements2}", BLUE, 350)

    return permutation, colors, ball_radius, ball_centers


# Function to draw the balls on the screen
def draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls):
    max_columns = 11  # Maximum number of columns in the grid
    spacing = 10  # Spacing between balls

    num_balls = len(permutation)
    num_rows = (num_balls + max_columns - 1) // max_columns

    for i, (num, center) in enumerate(zip(permutation, ball_centers)):
        column = i % max_columns
        row = i // max_columns
        x = column * (2 * ball_radius + spacing) + ball_radius
        y = window_height // 2 + row * (2 * ball_radius + spacing)

        if colors[i] == BLUE:
            pygame.draw.circle(screen, BLUE, (x, y), ball_radius)
            if i in selected_balls:
                pygame.draw.circle(screen, GRAY, (x, y), ball_radius - 2)
        else:
            pygame.draw.circle(screen, RED, (x, y), ball_radius)

        text = font.render(str(num), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

# Game state variables
num_balls = None  # Number of balls
permutation = []  # Permutation of balls
colors = []  # Colors of balls
ball_radius = 0  # Radius of the balls
ball_centers = []  # Centers of the balls
game_started = False  # Flag to indicate if the game has started
selected_balls = []  # List to store the indices of selected blue balls
swap_button_visible = False  # Flag to indicate if the swap button is visible
ai_player = False  # Flag to indicate if it's the AI player's turn

# Create the input field
input_field_width = 200
input_field_height = 50
input_field_x = (window_width - input_field_width) // 2
input_field_y = (window_height - input_field_height) // 2
input_rect = pygame.Rect(input_field_x, input_field_y, input_field_width, input_field_height)
input_text = ""
active = False

# Create the confirm button
button_width = 100
button_height = 50
button_x = (window_width - button_width) // 2
button_y = input_field_y + input_field_height + 20
confirm_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Create the swap button
swap_button_width = 100
swap_button_height = 50
swap_button_x = (window_width - swap_button_width) // 2
swap_button_y = button_y + button_height + 20
swap_button_rect = pygame.Rect(swap_button_x, swap_button_y, swap_button_width, swap_button_height)

# Function to handle button click event
def button_callback():
    global num_balls, permutation, colors, ball_radius, ball_centers, game_started, ai_player
    num_balls = int(input_text)  # Get the number of balls from the input field
    permutation, colors, ball_radius, ball_centers = generate_permutation(num_balls)
    game_started = True
    ai_player = False  # Reset AI player flag
def ball_click_handler(pos):
    global colors, selected_balls, swap_button_visible, global_filtered_elements1, global_filtered_elements2

    max_columns = 11  # Maximum number of columns in the grid
    spacing = 10  # Spacing between balls

    num_balls = len(permutation)
    num_rows = (num_balls + max_columns - 1) // max_columns

    for i, (num, center) in enumerate(zip(permutation, ball_centers)):
        column = i % max_columns
        row = i // max_columns
        x = column * (2 * ball_radius + spacing) + ball_radius
        y = window_height // 2 + row * (2 * ball_radius + spacing)

        if pygame.Rect(x - ball_radius, y - ball_radius, 2 * ball_radius, 2 * ball_radius).collidepoint(pos):
            if colors[i] == RED:
                colors[i] = BLUE

                # Update filtered elements
                if i in global_filtered_elements1:
                    global_filtered_elements1.remove(i)
                    #toast(f"Filtered Elements 1: {global_filtered_elements1}", BLUE, 350)
                if i in global_filtered_elements2:
                    global_filtered_elements2.remove(i)
                    #toast(f"Filtered Elements 1: {global_filtered_elements1}", BLUE, 350)

                # AI Move
                ai_move()

            elif colors[i] == BLUE:
                if i in selected_balls:
                    selected_balls.remove(i)
                    colors[i] = BLUE
                else:
                    selected_balls.append(i)
                    colors[i] = BLUE
            elif colors[i] == GRAY:
                colors[i] = BLUE

    if len(selected_balls) == 2:
        if global_filtered_elements1:
            swap_button_visible = False  # Disable the swap button
            toast("You need to make all necessary positions Blue", BLUE, 200)
        else:
            swap_button_visible = True  # Enable the swap button
    else:
        swap_button_visible = False


# Function to handle swap button click event
def swap_button_callback():
    global permutation, colors, selected_balls, swap_button_visible

    # Swap the positions of the selected blue balls
    index1, index2 = selected_balls
    permutation[index1], permutation[index2] = permutation[index2], permutation[index1]
    colors[index1], colors[index2] = colors[index2], colors[index1]

    # Clear the selected balls list and hide the swap button
    selected_balls = []
    swap_button_visible = False


# Function to display a toast message
def show_toast_message(message):
    toast_width = 250
    toast_height = 50
    toast_x = (window_width - toast_width) // 2
    toast_y = (window_height - toast_height) // 2
    toast_rect = pygame.Rect(toast_x, toast_y, toast_width, toast_height)

    pygame.draw.rect(screen, BLACK, toast_rect)
    toast_text = font.render(message, True, WHITE)
    toast_text_rect = toast_text.get_rect(center=toast_rect.center)
    screen.blit(toast_text, toast_text_rect)
    pygame.display.flip()
    time.sleep(2)  # Display the toast message for 2 seconds
    
# Function to display a toast message
def toast(message, color, width):
    toast_font = pygame.font.Font(None, 24)
    toast_surface = toast_font.render(message, True, color)
    toast_rect = pygame.Rect((window_width - width) // 2, window_height - 40, width, 30)
    pygame.draw.rect(screen, WHITE, toast_rect)
    pygame.draw.rect(screen, BLACK, toast_rect, 2)
    toast_rect.x += 5
    screen.blit(toast_surface, toast_rect)
    pygame.display.update(toast_rect)
    pygame.time.delay(1500)
    pygame.draw.rect(screen, WHITE, toast_rect)
    pygame.display.update(toast_rect)
def hide_balls(s):
    # Set the width and height of the game window
    width = 800
    height = 600
    # Create the game window
    window = pygame.display.set_mode((width, height))
    # Set the font and size
    font = pygame.font.Font(None, 36)
    # Create a text surface
    text_surface = font.render(s, True, (0, 0, 0))
    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect()
    # Position the text in the center of the screen
    text_rect.center = (width // 2, height // 2)
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
        # Clear the screen
        window.fill((255, 255, 255))  # Fill the window with white color        
        # Blit the text surface onto the screen
        window.blit(text_surface, text_rect)        
        # Update the display
        pygame.display.flip()

flag=0
def ai_move():
    global permutation, colors, selected_balls, global_filtered_elements1, global_filtered_elements2
    
    global Total_move
    Total_move+=2
    toast(f"Total Move: {Total_move}", RED, 350)      
    # Check if there are any elements in global_filtered2 - global_filtered1
    remaining_blue_balls = [i for i in global_filtered_elements2 if i not in global_filtered_elements1]
    
    if permutation == sorted(permutation):
        hide_balls("You Won!")
        return

    # Check if the permutation is in descending order
    if permutation == sorted(permutation, reverse=True):
        hide_balls("You Lost!")
        pygame.display.set_caption("You Lost!")
        return
        #pygame.quit()
    if Total_move>=num_balls*num_balls:
        hide_balls("Draw!")
        pygame.display.set_caption("Draw!")
        return

    # Turn one ball from global_filtered2 - global_filtered1 into blue
    if remaining_blue_balls:
        ball_index = remaining_blue_balls[0]
        colors[ball_index] = BLUE
        if ball_index in global_filtered_elements2:
            global_filtered_elements2.remove(ball_index)
        if ball_index in global_filtered_elements1:
            global_filtered_elements1.remove(ball_index)
        toast(f"AI turned ball {permutation[ball_index]} blue", BLUE, 220)
        return
    
    # Turn one ball from global_filtered2 into red
    if global_filtered_elements2:
        ball_index = global_filtered_elements2[0]
        colors[ball_index] = BLUE
        if ball_index in global_filtered_elements2:
            global_filtered_elements2.remove(ball_index)
        if ball_index in global_filtered_elements1:
            global_filtered_elements1.remove(ball_index)
        
        toast(f"AI turned ball {permutation[ball_index]} BLUE", BLUE, 220)
        return
    
    # Swap balls where n - a[ind] = ind
    for i in range(len(permutation)):
        if (num_balls - permutation[i]) != i:
            for j in range(i + 1, len(permutation)):
                if (num_balls - permutation[j]) != j:
                    permutation[i], permutation[j] = permutation[j], permutation[i]
                    colors[i], colors[j] = colors[j], colors[i]
                    toast(f"AI swapped balls {permutation[i]} and {permutation[j]}", BLUE, 280)
                        # Check if the permutation is in ascending order
                    if permutation == sorted(permutation):
                        hide_balls("You Won!")
                        pygame.display.set_caption("You Win!")
                        #pygame.quit()

                    # Check if the permutation is in descending order
                    if permutation == sorted(permutation, reverse=True):
                        hide_balls("You Lost!")
                        pygame.display.set_caption("You Lost!")
                        #pygame.quit()

                    return
    
    # Display toast message for the final arrangement
    #toast("AI arranged the balls in descending order", BLUE, 280)

# Game loop
running = True

while running:
    screen.fill(WHITE)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif confirm_button_rect.collidepoint(event.pos):
                    button_callback()
                    active = False
                else:
                    active = False
            else:
                if swap_button_visible and swap_button_rect.collidepoint(event.pos):
                    swap_button_callback()
                    # Call the AI move function after the user clicks the swap button
                    ai_move()
                else:
                    ball_click_handler(event.pos)
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if not game_started:
        # Draw the input field and confirm button
        pygame.draw.rect(screen, BLUE if active else WHITE, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = font.render(input_text, True, WHITE)
        input_surface_rect = input_surface.get_rect(center=input_rect.center)
        screen.blit(input_surface, input_surface_rect)

        pygame.draw.rect(screen, BLACK, confirm_button_rect)
        confirm_text = font.render("Confirm", True, WHITE)
        confirm_text_rect = confirm_text.get_rect(center=confirm_button_rect.center)
        screen.blit(confirm_text, confirm_text_rect)
    else:
        # Draw the balls if the game has started
        draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls)
        if swap_button_visible:
            pygame.draw.rect(screen, BLACK, swap_button_rect)
            swap_text = font.render("Swap", True, WHITE)
            swap_text_rect = swap_text.get_rect(center=swap_button_rect.center)
            screen.blit(swap_text, swap_text_rect)

        # AI Move
        if ai_player and len(selected_balls) < 2:
            ai_move()

    pygame.display.flip()

pygame.quit()
