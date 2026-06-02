import turtle
import time
import random
import math

# ---------------- GAME VARIABLES ---------------- #

delay = 0.1
score = 0
high_score = 0

# ---------------- WINDOW SETUP ---------------- #

wn = turtle.Screen()
wn.title("AI Snake Game")
wn.bgcolor("black")
wn.setup(width=700, height=700)
wn.tracer(0)

# ---------------- SNAKE HEAD ---------------- #

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# ---------------- FOOD ---------------- #

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 0)

segments = []

# ---------------- SCORE DISPLAY ---------------- #

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 310)

pen.write(
    "Score : 0  High Score : 0",
    align="center",
    font=("Arial", 20, "bold")
)

# ---------------- MOVEMENT ---------------- #

def move():

    if head.direction == "up":
        head.sety(head.ycor() + 20)

    elif head.direction == "down":
        head.sety(head.ycor() - 20)

    elif head.direction == "left":
        head.setx(head.xcor() - 20)

    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# ---------------- AI FUNCTIONS ---------------- #

def is_safe(x, y):
    """
    Check if position is safe.
    """

    if x > 330 or x < -330 or y > 330 or y < -330:
        return False

    for segment in segments:
        if segment.distance(x, y) < 20:
            return False

    return True


def ai_move():
    """
    Move toward food while avoiding
    walls and body.
    """

    head_x = head.xcor()
    head_y = head.ycor()

    food_x = food.xcor()
    food_y = food.ycor()

    possible_moves = {
        "up": (head_x, head_y + 20),
        "down": (head_x, head_y - 20),
        "left": (head_x - 20, head_y),
        "right": (head_x + 20, head_y)
    }

    safe_moves = {}

    for direction, (x, y) in possible_moves.items():

        if is_safe(x, y):

            distance = math.sqrt(
                (food_x - x) ** 2 +
                (food_y - y) ** 2
            )

            safe_moves[direction] = distance

    if safe_moves:
        best_move = min(safe_moves, key=safe_moves.get)
        head.direction = best_move


# ---------------- RESET GAME ---------------- #

def reset_game():
    global score
    global delay

    time.sleep(1)

    head.goto(0, 0)
    head.direction = "Stop"

    for segment in segments:
        segment.goto(1000, 1000)

    segments.clear()

    score = 0
    delay = 0.1

    pen.clear()
    pen.write(
        f"Score : {score}  High Score : {high_score}",
        align="center",
        font=("Arial", 20, "bold")
    )


# ---------------- MAIN GAME LOOP ---------------- #

while True:

    wn.update()

    # AI decision
    ai_move()

    # Move body

    for index in range(len(segments) - 1, 0, -1):

        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()

        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Move snake
    move()

    # Border collision

    if (
        head.xcor() > 330 or
        head.xcor() < -330 or
        head.ycor() > 330 or
        head.ycor() < -330
    ):
        reset_game()

    # Food collision

    if head.distance(food) < 20:

        x = random.randrange(-300, 301, 20)
        y = random.randrange(-300, 301, 20)

        food.goto(x, y)

        # New segment

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("gray")
        new_segment.penup()

        segments.append(new_segment)

        score += 10

        if score > high_score:
            high_score = score

        delay = max(0.03, delay - 0.001)

        pen.clear()
        pen.write(
            f"Score : {score}  High Score : {high_score}",
            align="center",
            font=("Arial", 20, "bold")
        )

    # Body collision

    for segment in segments:

        if segment.distance(head) < 20:

            reset_game()
            break

    time.sleep(delay)

wn.mainloop()