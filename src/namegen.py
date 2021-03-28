from random import choice

vowels = list('aeoui')
consonants = list('bcdfghklmnpqrstvwxyz')

def gen_syllable() -> str:
    syll = ""
    length = choice([1, 2, 3])
    if length == 1:
        syll += choice(vowels)
    elif length == 2:
        if choice([0,1]):
            syll += choice(vowels)
            syll += choice(consonants)
        else:
            syll += choice(consonants)              
            syll += choice(vowels)
    else:
            syll += choice(consonants)        
            syll += choice(vowels)
            syll += choice(consonants)
    return syll

def gen_word() -> str:
    word = ""
    for i in range(choice([2, 3, 4])):
        word += gen_syllable()
    return word

