# implementation of card game - Memory

import simplegui
import random

deck = []
exposed = []
count = 0

# helper function to initialize globals
def new_game():
    global deck, exposed
    deck = range(8)+range(8)
    random.shuffle(deck)
    exposed = []
    for i in range(16):
        exposed.append(False)
    
    global state, card, prev_card, count
    state = 0
    card = prev_card = 0
    count = 0
    label.set_text("Turns = 0")
     
# define event handlers
def mouseclick(pos):
    
    global card, prev_card, count
    index = pos[0] / 50
    if exposed[index] == False:
        exposed[index] = True
    
        global state
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
        else:
            if deck[card] == deck[prev_card]:
                exposed[card]  = True
                exposed[prev_card] = True
            else:
                exposed[card] = False
                exposed[prev_card] = False
            state = 1
    
        prev_card = card
        card = index
        count = count + 1
        label.set_text("Turns = " + str(count))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    i = 0
    for num in deck: #draw digits
        canvas.draw_text(str(num), (15 + 50 * i, 65), 50, 'White')
        i = i + 1
    
    i = 0
    for expose in exposed:
        if(not expose):
            canvas.draw_polygon([(50 * i + 1, 0), (50 * i + 1, 100),
                                 (50 * i + 49, 100), (50 * i + 49, 0)], 
                                1, 'green', 'green')
        i = i + 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric