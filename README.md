# code
A code to block/mute those evil low income seniors and their "junior/senior caregivers" who refuse to retire.
this is such a nice platform...
who just said stfu ... cum on em...

so this is year # xxxxxxxxxxxxxxxxxxxxxxx    and i mastered HTML/CSS/PHP/asp but not this...



import random

def yoda_speak(sentence):
    words = sentence.split()
    if len(words) < 4:
        return "Hmm. Too short, it is."
    
    # Randomly split the sentence into two parts
    split_point = random.randint(1, len(words) - 2)
    first = words[:split_point]
    second = words[split_point:]
    
    yoda_sentence = ' '.join(second + first)
    return f"{yoda_sentence}, hmm."

# Example usage
input_sentence = "You must learn the ways of the Force"
print(yoda_speak(input_sentence))



-------------------------------------------------------------





