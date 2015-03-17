# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
    # create Hand object
        self.cards = []
        self.value = 0
        self.contain_ace = False

    def __str__(self):
    # return a string representation of a hand
        ans = ""
        for card in self.cards:
            ans += " " + card.__str__()
        return "Hand contains" + ans

    def add_card(self, card):
    # add a card object to a hand
        self.cards.append(card)
        self.value += VALUES[card.get_rank()]
        if card.get_rank() == 'A':
            self.contain_ace = True

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        if not self.contain_ace:
            return self.value
        if self.value + 10 <= 21:
            return self.value + 10
        else:
            return self.value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards:
            card.draw(canvas,[pos[0] + i * 1.2 * CARD_SIZE[0], pos[1]])
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for card in self.cards:
            ans += " " + card.__str__()
        return "Deck contains" + ans



#define event handlers for buttons
def deal():
    global in_play, prompt, player_hand, dealer_hand, deck, outcome, score

    #initialize hand and deck
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    
    #deal two cards to player and dealer respectively
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    if in_play == True:
        score -= 1
    in_play = True
    prompt = "Hit or stand?"
    outcome = ""

def hit():
    global score, outcome, in_play, prompt, player_hand
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You went bust and lose."
            prompt = "New deal?"
       
def stand():
    global score, outcome, in_play, prompt
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21 or dealer_hand.get_value() < player_hand.get_value():
           outcome = "You win"
           in_play = False
           score += 1
        else:
           outcome = "You Lose"
           in_play = False
           score -= 1
        prompt = "New deal?"

# draw handler    
def draw(canvas):
    
    canvas.draw_text('Blackjack', (60, 80), 40, 'Blue')
    canvas.draw_text('Score: ' + str(score), (330, 80), 30, 'Black')
    canvas.draw_text('dealer     ' + outcome, (60, 140), 30, 'Black')
    canvas.draw_text('player     ' + prompt, (60, 370), 30, 'Black')
    dealer_hand.draw(canvas, (60, 180))
    player_hand.draw(canvas, (60, 410))
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [60 + CARD_CENTER[0], 180 + CARD_CENTER[1]], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric