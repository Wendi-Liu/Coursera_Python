# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, times_left
    secret_number = random.randrange(0, upper_bound)
    times_left = int(math.ceil(math.log(upper_bound + 1, 2)) + 0.5)
    print "New game. Range is from 0 to", upper_bound
    print "Number of remaining guesses is", times_left
    print ""

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global upper_bound
    upper_bound = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global upper_bound
    upper_bound = 1000
    new_game()    
    
def input_guess(guess):
    # main game logic goes here	
    guess = int(guess)
    print "Guess was", guess
    global times_left
    times_left -= 1
    print "Number of remaining guesses is", times_left
    if secret_number > guess:
        print "Higher!"
    elif secret_number < guess:
        print "Lower!"
    else:
        print "Correct!"
    print ""
    if secret_number == guess:
        new_game()
    elif times_left <= 0:
        print "You lose!"
        print "The correct number is", secret_number
        print ""
        new_game()
    
# create frame
frame = simplegui.create_frame("guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()

# call new_game
upper_bound = 100
new_game()

# always remember to check your completed program against the grading rubric
