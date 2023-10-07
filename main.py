import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import math

def change_label_image(label, image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    
def create_label(image_path, no_of_label):
    all_label = []
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    for _ in range(no_of_label):
        label = tk.Label(window, image=photo)
        label.image = photo  # To prevent garbage collection
        all_label.append(label)
    return all_label

def move_label_toward_target(label, target_x, target_y, move_x, move_y):
    current_x = label.winfo_x()
    current_y = label.winfo_y()
    
    # Calculate the direction towards the target
    dx = target_x - current_x
    dy = target_y - current_y
    
    # Calculate the distance to the target
    distance = math.sqrt(dx**2 + dy**2)
    
    # Normalize the direction vector
    if distance > 0:
        dx /= distance
        dy /= distance

    # Move label toward the target
    new_x = current_x + move_x * dx
    new_y = current_y + move_y * dy

    if 10 <= new_x <= 739 and 10 <= new_y <= 739:
        label.place(x=new_x, y=new_y)
        update_position(label)

def update_position(label):
    if label in label_positions:
        label_positions[label] = (label.winfo_x(), label.winfo_y())

def check_collision_rock():
    for label in label_rock:
        current_x, current_y = label_positions[label]
        for scissor_label in label_scissor:
            paper_x, paper_y = label_positions[scissor_label]
            distance = math.sqrt((current_x - paper_x)**2 + (current_y - paper_y)**2)
            if distance < 2:  # Adjust this distance threshold as needed
                label_rock.append(scissor_label)
                label_scissor.remove(scissor_label)
                change_label_image(scissor_label,rock_image)
                update_score()

def check_collision_paper():
    for label in label_paper:
        current_x, current_y = label_positions[label]
        for rock_label in label_rock:
            scissor_x, scissor_y = label_positions[rock_label]
            distance = math.sqrt((current_x - scissor_x)**2 + (current_y - scissor_y)**2)
            if distance < 2:  # Adjust this distance threshold as needed
                label_paper.append(rock_label)
                label_rock.remove(rock_label)
                change_label_image(rock_label,paper_image)
                update_score()

def check_collision_scissor():
    for label in label_scissor:
        current_x, current_y = label_positions[label]
        for paper_label in label_paper:
            rock_x, rock_y = label_positions[paper_label]
            distance = math.sqrt((current_x - rock_x)**2 + (current_y - rock_y)**2)
            if distance < 2:  # Adjust this distance threshold as needed
                label_scissor.append(paper_label)              
                label_paper.remove(paper_label)
                change_label_image(paper_label,scissor_image)
                update_score()

def update_score():
    global score_rock
    score_rock = len(label_rock)
    global score_paper
    score_paper = len(label_paper)
    global score_scissor
    score_scissor = len(label_scissor)
    score_label.config(text=f"Rock: {score_rock} Paper: {score_paper} Scissor: {score_scissor}")

def move_toward_target_rock():
    to_continue = True
    for label in label_rock:
        try:
            target_values_scissor = find_nearest_target(label, label_scissor)
            target_x, target_y = target_values_scissor
            move_label_toward_target(label, target_x, target_y, 3, 3)
        except:
            check_finish()
            to_continue = False
            break
    if to_continue:
        check_collision_rock()
        update_score()
        window.after(5, move_toward_target_rock)

def move_toward_target_paper():
    to_continue = True
    for label in label_paper:
        try:
            target_value_rock = find_nearest_target(label, label_rock)
            target_x, target_y = target_value_rock
            move_label_toward_target(label, target_x, target_y, 3, 3)
        except:
            check_finish()
            to_continue = False
            break
    if to_continue:
        check_collision_paper()
        update_score()
        window.after(5, move_toward_target_paper)

def move_toward_target_scissor():
    to_continue = True
    for label in label_scissor:
        try:
            target_value_paper = find_nearest_target(label, label_paper)
            target_x, target_y = target_value_paper
            move_label_toward_target(label, target_x, target_y, 3, 3)
        except:
            check_finish()
            to_continue = False
            break
    if to_continue:
        check_collision_scissor()
        update_score()
        window.after(5, move_toward_target_scissor)

def find_nearest_target(label, targets):
    current_x, current_y = label_positions[label]
    nearest_target = None
    min_distance = float('inf')

    for target in targets:
        target_x, target_y = label_positions[target]
        distance = math.sqrt((current_x - target_x)**2 + (current_y - target_y)**2)
        if distance < min_distance:
            min_distance = distance
            nearest_target = (target_x, target_y)

    return nearest_target

def check_finish():
    global score_rock
    global score_paper
    global score_scissor
    if score_rock >= 75:
        winner = "Rock"
    elif score_paper >= 75:
        winner = 'Paper'
    else:
        winner = 'Scissor'
    if score_rock >= 75 or score_paper >= 75 or score_scissor >= 75:
        finish_label = tk.Label(window, text=f"Finish!!! {winner} is winner", font=("Helvetica", 30))
        finish_label.place(x=50, y=375)

# Create a Tkinter window
window = tk.Tk()
window.title("Image Viewer")
window.geometry("750x750")

# Create label widgets for images
no_of_label = 25
paper_image = "./assests/paper.png"
rock_image = "./assests/rock.png"
scissor_image = "./assests/scissor.png"

label_paper = create_label(paper_image, no_of_label)
label_rock = create_label(rock_image, no_of_label)
label_scissor = create_label(scissor_image, no_of_label)

# Place labels randomly
for labels in [label_paper, label_rock, label_scissor]:
    for label in labels:
        label.place(x=random.randint(10, 739), y=random.randint(10, 739))

label_positions = {}
for labels in [label_paper, label_rock, label_scissor]:
    for label in labels:
        label_positions[label] = (label.winfo_x(), label.winfo_y())

# Create three threads to run the label movement functions
threads = []

def start_threads():
    for func in [move_toward_target_rock, move_toward_target_paper, move_toward_target_scissor]:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

# Button to trigger the label movement
start_button = tk.Button(window, text="Start!!!", command=start_threads)
start_button.place(x=705,y=0)

# Initialize scores
score_rock = len(label_rock)
score_paper = len(label_paper)
score_scissor = len(label_scissor)

# Create a label to display scores
score_label = tk.Label(window, text=f"Rock: {score_rock} Paper: {score_paper} Scissor: {score_scissor}")
score_label.place(x=10, y=10)

# Run the Tkinter main loop
window.mainloop()