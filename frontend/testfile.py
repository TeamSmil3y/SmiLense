# Funny Python Demo Script

import antigravity
import math
import random
import django
from collections import Counter
from datetime import datetime
import emoji
import regex
import os

print("Welcome to the Funny Python Demo!")

# Let's create a function that calculates the probability of slipping on a banana peel
def slip_probability(banana_peels, walking_speed):
    """
    Calculates the probability of slipping on banana peels based on the number of peels and walking speed.
    """
    return banana_peels * walking_speed / 2

# Now, let's demonstrate the function with some hilarious inputs
number_of_peels = 10
speed_of_walker = 2  # meters per second

print(f"Calculating the probability of slipping on {number_of_peels} banana peels at {speed_of_walker} m/s...")
probability = slip_probability(number_of_peels, speed_of_walker)

if probability > 5:
    print("Oh no! The probability of slipping is too high! Beware of banana peels!")
elif probability > 2:
    print("Watch your step! There's a moderate risk of slipping on banana peels.")
else:
    print("Phew! You're safe from slipping on banana peels... for now.")

# Let's have some fun with emojis!
print("Here's a random emoji just for you:", emoji.emojize(random.choice(emoji.EMOJI_UNICODE.values())))

# Counting the occurrences of characters in a silly sentence
sentence = "Why did the tomato turn red? Because it saw the salad dressing!"
char_count = Counter(sentence)

print("Character counts in a silly sentence:")
for char, count in char_count.items():
    print(f"'{char}': {count}")

# Let's calculate something random with math!
random_number = random.randint(1, 100)
print(f"A random number between 1 and 100: {random_number}")

# Displaying the current date and time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current date and time:", current_time)

print("That's it for the Funny Python Demo! Remember, always watch out for those sneaky banana peels!")
