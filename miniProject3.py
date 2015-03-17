# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
success = 0
attempts = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    C = t / 10 % 10
    B = t / 100 % 6
    A = t / 600
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global running
    running = True
    timer.start()
    
def stop_handler():
    global running, success, attempts
    if running:
        if time % 10 == 0:
            success += 1
        attempts += 1
        running = False
        timer.stop()
    
def reset_handler():
    timer.stop()
    global time, running, success, attempts
    time = 0
    running = False
    success = 0
    attempts = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), (40, 120), 40, 'White')
    canvas.draw_text(str(success) + "/" + str(attempts), (135, 30), 30, 'yellow')
    
# create frame
frame = simplegui.create_frame("stopwatch", 200, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_handler, 80)
frame.add_button("Stop", stop_handler, 80)
frame.add_button("Reset", reset_handler, 80)

# start frame
frame.start()


# Please remember to review the grading rubric
