from FastWords import FastWords
import time
import re
from spellchecker import SpellChecker

current_text = ''
Fast_bot = FastWords()
spell = SpellChecker()

while True:
    print("Starting new game!")
    time.sleep(2)
    Fast_bot.EndGame(click=True)
    time.sleep(1)
    # Plays one Episode
    while not Fast_bot.EndGame():


        print("\n")
        # Try to find word for 10000 times
        for i in range(25):
            text = Fast_bot.ReadScreen()
            if len(text) > 0 and text != current_text:
                current_text = text
                print(f"Raw Input: {current_text}")

        # Strip everything but spaces and capitals
        current_text = re.sub(r'[^A-Z] ', '', current_text).rstrip()

        # If we have two words just take the first one
        if len(current_text.split()) > 1:
            current_text = current_text.split()[0]

        # Now kill the spaces.
        current_text = re.sub(r'[^A-Z]', '', current_text)
        print(f"Refined Input: {current_text}")

        # Try spell check? optional
        # current_text = spell.correction(current_text).upper()
        # print(current_text)

        for letter in current_text:
            print(f"Looking for {letter}")
            Fast_bot.find_letter(letter)
            time.sleep(.2)
        time.sleep(2)
