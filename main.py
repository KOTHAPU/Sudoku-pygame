import pygame
import sys
import os
import time
import random

# Initialize pygame
pygame.init()

# Default screen settings
main_screen_width, main_screen_height = 800, 600
black_screen_width, black_screen_height = 540, 590
screen = pygame.display.set_mode((main_screen_width, main_screen_height))
pygame.display.set_caption("Sudoku Game")

# Colors and Fonts
header_color = (22, 138, 233)  # Header blue color
background_color = (200, 200, 200)  # Light gray background
font_large = pygame.font.Font(None, 60)  # Large font
font_small = pygame.font.Font(None, 40)  # Smaller font

# Image paths
image_folder = r"D:\UNI\Sem 3\CSM216\project.py\images"
image_paths = [os.path.join(image_folder, "10min.jpg"),
               os.path.join(image_folder, "5min.jpg"),
               os.path.join(image_folder, "2min.jpg")]

# Popup settings
popup_width, popup_height = 600, 300
button_width, button_height = 150, 40


def generate_sudoku(difficulty):
    """Generates a Sudoku grid based on difficulty."""
    # Pre-defined solved grid for simplicity
    base_grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    # Shuffle rows and columns within blocks
    def shuffle_grid(grid):
        rows = [0, 1, 2]
        cols = [0, 1, 2]
        random.shuffle(rows)
        random.shuffle(cols)
        new_grid = [[0] * 9 for _ in range(9)]
        for i in range(3):
            for j in range(3):
                for r in range(3):
                    for c in range(3):
                        new_grid[i * 3 + r][j * 3 + c] = grid[rows[i] * 3 + r][cols[j] * 3 + c]
        return new_grid

    shuffled_grid = shuffle_grid(base_grid)

    # Remove numbers based on difficulty
    difficulty_map = {"Easy": 36, "Medium": 45, "Hard": 54}  # Numbers to remove
    to_remove = difficulty_map[difficulty]
    for _ in range(to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while shuffled_grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        shuffled_grid[row][col] = 0

    return shuffled_grid


def welcome_page():
    """Displays the welcome page."""
    screen.fill(header_color)
    welcome_text = font_large.render("Sudoku", True, (255, 255, 255))  # White text
    screen.blit(welcome_text, (
        main_screen_width // 2 - welcome_text.get_width() // 2, main_screen_height // 2 - welcome_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display this page for 3 seconds


def draw_popup(label):
    """Draws a popup with the given label."""
    popup_x, popup_y = (main_screen_width - popup_width) // 2, (main_screen_height - popup_height) // 2

    # Draw popup border and background
    pygame.draw.rect(screen, (230, 230, 230), (popup_x, popup_y, popup_width, popup_height), 2)
    pygame.draw.rect(screen, (50, 50, 50), (popup_x, popup_y - 50, popup_width, 50))  # Title background
    pygame.draw.rect(screen, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height))  # Main popup background

    # Title
    title_text = font_small.render(label, True, (255, 255, 255))
    title_x = popup_x + (popup_width - title_text.get_width()) // 2
    title_y = popup_y - 50 + (50 - title_text.get_height()) // 2
    screen.blit(title_text, (title_x, title_y))

    # Buttons
    button_texts = ["Easy", "Medium", "Hard"]
    button_x = popup_x + (popup_width - button_width) // 2
    button_y_start = popup_y + 60

    for i, text in enumerate(button_texts):
        button_rect = pygame.Rect(button_x, button_y_start + i * (button_height + 20), button_width, button_height)
        pygame.draw.rect(screen, (24, 144, 255), button_rect, border_radius=5)
        button_text = font_small.render(text, True, (255, 255, 255))
        text_x = button_rect.centerx - button_text.get_width() // 2
        text_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (text_x, text_y))

    pygame.display.flip()
    return [pygame.Rect(button_x, button_y_start + i * (button_height + 20), button_width, button_height) for i in range(3)]


def main_game_page():
    """Displays the main game page."""
    global screen
    screen.fill(background_color)

    # Draw header
    pygame.draw.rect(screen, header_color, (0, 0, main_screen_width, 70))
    sudoku_text = font_large.render("SUDOKU", True, (255, 255, 255))  # White color
    screen.blit(sudoku_text, (main_screen_width // 2 - sudoku_text.get_width() // 2, 20))

    # Load and position images with error handling
    images = []
    for img_path in image_paths:
        try:
            img = pygame.transform.scale(pygame.image.load(img_path), (180, 180))
            images.append(img)
        except FileNotFoundError:
            print(f"Error: File not found - {img_path}")
            images.append(pygame.Surface((180, 180)))  # Placeholder if image is missing

    # Position each grid image with a gap of 100 pixels between them
    grid_x_positions = [100, 310, 520]
    labels = ["10 mins", "5 mins", "2 mins"]

    for i, (img, label) in enumerate(zip(images, labels)):
        # Display each grid image
        screen.blit(img, (grid_x_positions[i], 200))

        # Display the label below each grid
        label_text = font_small.render(label, True, (0, 0, 0))  # Black text
        screen.blit(label_text, (grid_x_positions[i] + 50, 390))

    pygame.display.flip()
    return grid_x_positions, labels


def is_sudoku_completed(sudoku_puzzle, cell_values):
    """Check if the Sudoku puzzle is completed and correct."""
    # Merge the puzzle with the user's inputs (this is the final grid state)
    completed_grid = [[sudoku_puzzle[row][col] if sudoku_puzzle[row][col] != 0 else cell_values.get((row, col), 0)
                       for col in range(9)] for row in range(9)]

    # Check rows, columns, and 3x3 subgrids
    for i in range(9):
        if len(set(completed_grid[i])) != 9 or 0 in completed_grid[i]:
            return False  # Invalid row
        column = [completed_grid[j][i] for j in range(9)]
        if len(set(column)) != 9 or 0 in column:
            return False  # Invalid column

    # Check 3x3 subgrids
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            subgrid = [completed_grid[r + i][c + j] for i in range(3) for j in range(3)]
            if len(set(subgrid)) != 9 or 0 in subgrid:
                return False  # Invalid 3x3 subgrid

    return True  # The puzzle is solved


def restart_game(difficulty, timer_seconds):
    """Reset the game state and start a new game."""
    global screen

    # Reset the game state
    global sudoku_puzzle, cell_values, selected_cell, previous_selected_cell, completed_flag, time_expired
    sudoku_puzzle = generate_sudoku(difficulty)  # Generate a new Sudoku puzzle
    cell_values = {}
    selected_cell = None
    previous_selected_cell = None
    completed_flag = False
    time_expired = False

    # Reset the timer
    start_time = time.time()

    # Start a new game by calling black_screen_page
    black_screen_page(difficulty, timer_seconds)


def black_screen_page(difficulty, timer_seconds):
    """Displays the Sudoku game based on the selected difficulty and timer."""
    global screen
    screen = pygame.display.set_mode((black_screen_width, black_screen_height))
    screen.fill((200, 200, 200))  # Light gray background

    # Generate Sudoku puzzle
    sudoku_puzzle = generate_sudoku(difficulty)

    # Define grid properties
    grid_size = 9
    cell_size = black_screen_width // grid_size
    bold_color = (0, 0, 0)
    light_color = (50, 50, 50)

    # Timer setup
    start_time = time.time()

    # Event loop
    running = True
    selected_cell = None
    previous_selected_cell = None  # Track the previously selected cell
    cell_values = {}  # Dictionary to store the values entered by the user

    completed_flag = False
    time_expired = False
    time_expired_time = 0  # Track the time when the timer hits 0
    last_cell_filled = False  # Flag to track if the last cell has been filled
    puzzle_completed_time = 0  # Store the time when the puzzle is completed
    popup_delay_time = 0  # Track delay time for popup to avoid immediate popup

    while running:
        # Calculate remaining time
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, timer_seconds - elapsed_time)

        # Check if Sudoku is completed and show "Congratulations!" popup only when the last cell is filled
        if not completed_flag:
            if is_sudoku_completed(sudoku_puzzle, cell_values) and not last_cell_filled:
                last_cell_filled = True  # Mark that the last cell is filled
                puzzle_completed_time = time.time()  # Record time when the puzzle is completed
                completed_flag = True
                message_text = "Congratulations!"
                message_color = (0, 255, 0)

        # Check if the timer has expired
        if remaining_time == 0 and not time_expired:
            time_expired = True
            time_expired_time = time.time()

        # Handle "Time's Up!" popup
        if time_expired and time.time() - time_expired_time >= 1:
            message_text = "Time's up! Better luck next time"
            message_color = (255, 0, 0)
            restart_button, exit_button = display_popup(screen, message_text, message_color)
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if restart_button.collidepoint(mouse_x, mouse_y):
                            # Restart game logic
                            restart_game(difficulty, timer_seconds)  # Call restart_game
                            waiting_for_input = False  # Exit popup loop
                        elif exit_button.collidepoint(mouse_x, mouse_y):
                            pygame.quit()
                            sys.exit()

        # Show "Congratulations!" popup after 1 second delay
        if completed_flag and time.time() - puzzle_completed_time >= 1:
            restart_button, exit_button = display_popup(screen, message_text, message_color)
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if restart_button.collidepoint(mouse_x, mouse_y):
                            # Restart game logic
                            restart_game(difficulty, timer_seconds)  # Call restart_game
                            waiting_for_input = False  # Exit popup loop
                        elif exit_button.collidepoint(mouse_x, mouse_y):
                            pygame.quit()
                            sys.exit()

        # Draw the grid
        # Draw the grid background and clear cells
        for row in range(grid_size):
            for col in range(grid_size):
                cell_x = col * cell_size
                cell_y = row * cell_size + 50

                # Clear the cell background with a light gray color
                pygame.draw.rect(screen, (200, 200, 200), (cell_x + 1, cell_y + 1, cell_size - 2, cell_size - 2))

        # Draw the grid lines
        for i in range(10):
            width = 4 if i % 3 == 0 else 1  # Thicker lines for bold grid lines
            pygame.draw.line(screen, (0, 0, 0), (0, i * cell_size + 50), (black_screen_width, i * cell_size + 50),
                             width)
            pygame.draw.line(screen, (0, 0, 0), (i * cell_size, 50), (i * cell_size, black_screen_width + 50), width)

        # Draw header (difficulty and timer)
        pygame.draw.rect(screen, header_color, (0, 0, black_screen_width, 50))
        difficulty_text = font_small.render(difficulty, True, (255, 255, 255))
        timer_text = font_small.render(f"Timer: {remaining_time // 60}:{remaining_time % 60:02}", True, (255, 255, 255))
        screen.blit(difficulty_text, ((black_screen_width - difficulty_text.get_width()) // 2, 10))
        screen.blit(timer_text, (black_screen_width - timer_text.get_width() - 10, 10))

        # Draw numbers and highlight the selected cell
        font_grid = pygame.font.Font(None, 40)
        for row in range(grid_size):
            for col in range(grid_size):
                cell_x = col * cell_size
                cell_y = row * cell_size + 50

                # Highlight the currently selected cell with light blue
                if selected_cell == (row, col):
                    highlight_rect = pygame.Rect(cell_x + 1, cell_y + 1, cell_size - 2, cell_size - 2)
                    if col % 3 == 0:
                        highlight_rect.x += 2
                        highlight_rect.width -= 2
                    if row % 3 == 0:
                        highlight_rect.y += 2
                        highlight_rect.height -= 2
                    pygame.draw.rect(screen, (200, 200, 255), highlight_rect)  # Light blue for selected cell

                # Draw pre-filled number from sudoku_puzzle if present
                if sudoku_puzzle[row][col] != 0:
                    num_text = font_grid.render(str(sudoku_puzzle[row][col]), True, (0, 0, 0))
                    screen.blit(num_text, (cell_x + cell_size // 3, cell_y + cell_size // 3))

                # Draw the user-entered number from cell_values if present
                elif (row, col) in cell_values:
                    num_text = font_grid.render(str(cell_values[(row, col)]), True, (0, 0, 0))
                    x = col * cell_size + cell_size // 2 - num_text.get_width() // 2
                    y = row * cell_size + 50 + cell_size // 2 - num_text.get_height() // 2
                    screen.blit(num_text, (x, y))

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_y > 50:
                    col = mouse_x // cell_size
                    row = (mouse_y - 50) // cell_size
                    # If the selected cell changes, remove highlight from the previous one
                    if selected_cell != (row, col):
                        previous_selected_cell = selected_cell  # Save the current selected cell as previous
                        selected_cell = (row, col)  # Set the new selected cell
            elif event.type == pygame.KEYDOWN and selected_cell:
                if event.unicode.isdigit() and event.unicode != '0':
                    row, col = selected_cell
                    # Only update the cell if it's empty (not a pre-filled number)
                    if sudoku_puzzle[row][col] == 0:
                        cell_values[(row, col)] = int(event.unicode)

        # Clear previous selected cell highlight if the selected cell changed
        if previous_selected_cell != selected_cell:
            if previous_selected_cell:
                prev_row, prev_col = previous_selected_cell
                prev_cell_x = prev_col * cell_size
                prev_cell_y = prev_row * cell_size + 50
                # Redraw the previous cell without highlight
                pygame.draw.rect(screen, (200, 200, 200), (prev_cell_x + 1, prev_cell_y + 1, cell_size - 2, cell_size - 2))

def display_popup(screen, message_text, message_color):
    """Display a popup message with Restart and Exit buttons."""
    # Popup dimensions
    popup_width = 450
    popup_height = 160
    popup_x = (black_screen_width - popup_width) // 2
    popup_y = (black_screen_height - popup_height) // 2

    pygame.draw.rect(screen, header_color, (popup_x, popup_y, popup_width, popup_height))

    # Render the message text
    text = font_small.render(message_text, True, (255, 255, 255))
    text_x = popup_x + (popup_width - text.get_width()) // 2
    text_y = popup_y + 20  # Place the message at the top
    screen.blit(text, (text_x, text_y))

    # Define button dimensions
    button_width = 120
    button_height = 40

    # Calculate spacing for buttons to be centered horizontally
    total_button_width = button_width * 2  # Two buttons
    spacing = (popup_width - total_button_width) // 3  # Space between buttons

    # Draw the "Restart" button
    restart_button_rect = pygame.Rect(popup_x + spacing, popup_y + 80, button_width, button_height)
    pygame.draw.rect(screen, (0, 255, 0), restart_button_rect)
    restart_text = font_small.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2,
                               restart_button_rect.centery - restart_text.get_height() // 2))

    # Draw the "Exit" button
    exit_button_rect = pygame.Rect(popup_x + spacing * 2 + button_width, popup_y + 80, button_width, button_height)
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    exit_text = font_small.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (
        exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))

    pygame.display.flip()

    return restart_button_rect, exit_button_rect


def main():
    """Main program."""
    welcome_page()

    while True:
        grid_x_positions, labels = main_game_page()

        # Wait for user to click on a grid
        running = True
        selected_difficulty = None
        selected_timer = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i, grid_x in enumerate(grid_x_positions):
                        if grid_x <= mouse_x <= grid_x + 180 and 200 <= mouse_y <= 380:
                            # Show difficulty popup
                            popup_rects = draw_popup("Select Difficulty")
                            selecting_difficulty = True
                            while selecting_difficulty:
                                for popup_event in pygame.event.get():
                                    if popup_event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif popup_event.type == pygame.MOUSEBUTTONDOWN:
                                        for j, rect in enumerate(popup_rects):
                                            if rect.collidepoint(popup_event.pos):
                                                selected_difficulty = ["Easy", "Medium", "Hard"][j]
                                                selected_timer = [600, 300, 120][i]  # 10 mins, 5 mins, 2 mins
                                                selecting_difficulty = False
                                                running = False

        if selected_difficulty and selected_timer:
            black_screen_page(selected_difficulty, selected_timer)


if __name__ == "__main__":
    main()
