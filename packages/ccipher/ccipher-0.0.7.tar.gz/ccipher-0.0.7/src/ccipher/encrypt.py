from . import alphabet, numbers
from .commons import convertStringToLowerCase

def encryptLetter(letter: str, key: int) -> str:
    letterIndex = alphabet.find(letter)

    if (letterIndex < 0):
        return letter
    
    newIndex = (letterIndex + key) % len(alphabet)
    
    return alphabet[newIndex]


def encryptNumber(number: int, key: int):
    numberIndex = numbers.find(number)

    if (numberIndex < 0):
        return number
    
    newIndex = (numberIndex + key) % len(numbers)
    
    return numbers[newIndex]

def encrypt(string: str, key: int) -> str:
    lowerstring = convertStringToLowerCase(string)

    newString = ''

    for letter in lowerstring:
        if (letter.isnumeric()):
            newString += encryptNumber(number=letter, key=key)
        else:
            newString += encryptLetter(letter=letter, key=key)

    return newString
