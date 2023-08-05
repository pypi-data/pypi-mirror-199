def readFile(filename: str) -> str:    
    with open(filename, 'r', encoding='utf-8') as f:
        fileContent = f.read()
    
    return fileContent

def writeFile(filename: str, string: str) -> bool:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(string)
        
        return True
    except:
        Exception('error to write in file')

        return False