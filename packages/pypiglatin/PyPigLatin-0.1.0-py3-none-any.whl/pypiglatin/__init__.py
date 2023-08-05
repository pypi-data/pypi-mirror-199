__version__ = '0.1.0'
__author__ = 'owenway imerplay '

vowels = "aeiou"

def translate_word(word):
    ret = ""
    
    if word[0].lower() in vowels:
        ret = (word + "way").lower()
        
    elif word[0].lower() not in vowels and word[1].lower() not in vowels:
        ret = (word[2:] + word[0] + word[1] + "ay").lower()
        
    elif word[0] not in vowels and word[1] in vowels:
        ret = (word[1:] + word[0] + "ay").lower()

    return ret

def translate_string(string):
    out_str = ""
    for word in string.split():
        print(word)
        out_str = out_str + translate_word(word) + " "
    print(out_str)
        
    
