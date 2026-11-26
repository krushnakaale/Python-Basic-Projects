import random

BANK = {
 'Python': [('Which keyword defines a function?', ['def','func','define','fn'],0),('Which type is immutable?', ['list','dict','tuple','set'],2),('What is len("Python")?', ['5','6','7','8'],1),('Which operator gives a remainder?', ['//','**','%','/'],2),('Which value represents absence?', ['False','0','None','Empty'],2)],
 'Computer Fundamentals': [('What does CPU stand for?', ['Central Processing Unit','Computer Power Unit','Central Print Utility','Control Program User'],0),('Which memory is volatile?', ['SSD','RAM','ROM','DVD'],1),('Which is an input device?', ['Monitor','Printer','Keyboard','Speaker'],2),('How many bits make a byte?', ['4','8','16','32'],1),('Which protocol secures web traffic?', ['FTP','HTTP','HTTPS','SMTP'],2)],
 'General Knowledge': [('Which planet is largest?', ['Earth','Mars','Jupiter','Venus'],2),('What is the capital of India?', ['Mumbai','New Delhi','Pune','Chennai'],1),('Which gas do plants absorb for photosynthesis?', ['Oxygen','Helium','Carbon dioxide','Hydrogen'],2),('How many sides has a hexagon?', ['5','6','7','8'],1),('Which ocean is largest?', ['Atlantic','Indian','Arctic','Pacific'],3)]}

class Quiz:
    def __init__(self, category):
        self.questions = random.sample(BANK[category], len(BANK[category]))
        self.index = self.score = 0
        self.answered = False
    @property
    def current(self):
        return self.questions[self.index]
    def answer(self, choice):
        if self.answered: return None
        self.answered = True
        correct = choice == self.current[2]
        self.score += int(correct)
        return correct
    def advance(self):
        if not self.answered: raise ValueError('Answer first')
        if self.index + 1 == len(self.questions): return False
        self.index += 1
        self.answered = False
        return True
