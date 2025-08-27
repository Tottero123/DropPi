import requests
import pygame
import sys
import time

# Raspberry Pi IP + port
PI_URL = "http://192.168.1.142:5000/deploy"
PI_TEST_URL = "http://192.168.1.142:5000/"

# Colors (your palette)

UI_COLOR = (15,169,204)

BACKGROUND = (0,0,0)

# Screen setup
pygame.init()
res = (1000, 720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Raspberry Pi 5 Control")

width, height = res

# Fonts
title_font = pygame.font.SysFont("Corbel", 60, bold=True)
button_font = pygame.font.SysFont("Corbel", 40, bold=True)
status_font = pygame.font.SysFont("Corbel", 28)

# Button properties
button_width, button_height = 200, 80
button_x = 50
button_y = height // 2 - button_height // 2

# Init sound
pygame.mixer.init()
unsuccessful = pygame.mixer.Sound("sounds/Disconected.mp3")  # use .wav if possible
successful = pygame.mixer.Sound("sounds/Connected.mp3")

#image of raspberry pi
pi_image = pygame.image.load("rpi5.png")

# ---- Functions ----
def check_pi_connection():
    """Check if Raspberry Pi server is online at start"""
    try:
        r = requests.get(PI_TEST_URL, timeout=2)
        print("Connected to Raspberry Pi ✅")
        successful.play()
        return True
    except Exception as e:
        print("❌ Cannot reach Raspberry Pi:", e)
        unsuccessful.play()
        return False
    
def chek_for_unconnected():
    """Check if Raspberry Pi server is online during runtime"""
    try:
        r = requests.get(PI_TEST_URL, timeout=2)
        return True
    except Exception as e:
        print("❌ Lost connection to Raspberry Pi:", e)
        unsuccessful.play()
        return False

def deploy():
    """Send deploy command to Raspberry Pi"""
    try:
        r = requests.post(PI_URL, timeout=2)
        if r.status_code == 200:
            print("DEPLOY sent! ✅")
         
        else:
            print("❌ Deploy failed with status:", r.status_code)
      
    except Exception as e:
        print("❌ Deploy failed:", e)
       

# ---- Startup check ----
if not check_pi_connection():
    # Show error screen
    error_screen = pygame.display.set_mode((1000, 720))
    clock = pygame.time.Clock()
    show_question_mark = True  # For blinking
    blink_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill background
        error_screen.fill(BACKGROUND)

        # Render error messages
        err_text = status_font.render("Cannot connect to Raspberry Pi 5", True, UI_COLOR)
        err_text2 = status_font.render("Check network & restart.", True, UI_COLOR)
        error_screen.blit(err_text, (50, 60))
        error_screen.blit(err_text2, (50, 100))

        # Draw Raspberry Pi image
        error_screen.blit(pi_image, (width//2 - pi_image.get_width()//2, height//2 - pi_image.get_height()//2))

        # Handle blinking question mark
        blink_timer += clock.get_time()
        if blink_timer > 500:  # 500 ms = toggle every half second
            show_question_mark = not show_question_mark
            blink_timer = 0

        if show_question_mark:
            question_mark = pygame.font.SysFont("Corbel", 200, bold=True).render("?", True, UI_COLOR)
            error_screen.blit(question_mark, (width//2 - 50, height//2 + pi_image.get_height()//2))

        pygame.display.update()
        clock.tick(30)  # Limit to 30 FPS

# ---- Main loop ----
clock = pygame.time.Clock()  # Add clock for timing

clock = pygame.time.Clock()  # Make sure clock is defined

while True:
    mouse = pygame.mouse.get_pos()
    clicked = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:  # SPACEBAR as backup trigger
                deploy()

    # Background
    screen.fill(BACKGROUND)

    # Title
    title_text = title_font.render("Raspberry Pi 5 Control Center", True, UI_COLOR)
    screen.blit(title_text, (width//2 - title_text.get_width()//2, 100))
    screen.blit(pi_image, (width -200 - pi_image.get_width()//2, height//2 - pi_image.get_height()//2))
    # Button hover and click
    if (button_x <= mouse[0] <= button_x + button_width and
        button_y <= mouse[1] <= button_y + button_height):
    
        pygame.draw.rect(screen, UI_COLOR,
                         [button_x, button_y, button_width, button_height],
                         border_radius=20)
        if clicked:
            deploy()
    else:
        pygame.draw.rect(screen, UI_COLOR,
                         [button_x, button_y, button_width, button_height],
                         border_radius=20)

    # Button text (centered)
    text = button_font.render("START SERVO", True, BACKGROUND)
    screen.blit(text, (button_x + button_width//2 - text.get_width()//2,
                       button_y + button_height//2 - text.get_height()//2))

    # Status check
    connected = chek_for_unconnected()  # returns True/False
    status_text = status_font.render(
        f"Status: {'Connected' if connected else 'Disconnected'}",
        True,
        UI_COLOR if connected else (255, 50, 50)
    )
    #status panel
    rect = pygame.Rect(10, height - 110, width, 5)
    pygame.draw.rect(screen, UI_COLOR, rect, width=0)
    screen.blit(status_text, (20, height - 100))  # bottom-left corner

    # Update screen
    pygame.display.update()
    clock.tick(30)  # Limit FPS to 30
