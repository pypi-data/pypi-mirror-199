from . import alphabet, numbers
from .commons import convertStringToLowerCase

def decryptLetter(letter: str, key: int) -> str:
    letterIndex = alphabet.find(letter)

    if (letterIndex < 0):
        return letter
    
    newIndex = (letterIndex - key) % len(alphabet)
    
    return alphabet[newIndex]

def decryptNumber(number: int, key: int) -> str:
    numberIndex = numbers.find(number)

    if (numberIndex < 0):
        return number
    
    newIndex = (numberIndex - key) % len(numbers)
    
    return numbers[newIndex]

def decrypt(string: str, key: int) -> str:
    lowerstring = convertStringToLowerCase(string)

    newString = ''

    for letter in lowerstring:
        if (letter.isnumeric()):
            newString += decryptNumber(number=letter, key=key)
        else:
            newString += decryptLetter(letter=letter, key=key)

    return newString