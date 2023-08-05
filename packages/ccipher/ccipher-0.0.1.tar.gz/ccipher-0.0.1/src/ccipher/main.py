import encrypt
import decrypt
import file

def main():
    cipherkey = 4
    filename = 'file.txt'

    filecontent = file.readFile(filename=filename)
    
    encrypted = encrypt(filecontent, key=cipherkey)
    
    outputEncryptedFilename = 'encrypted.txt'

    file.writeFile(outputEncryptedFilename, encrypted)

    filecontentencrypted = file.readFile(filename=outputEncryptedFilename)

    decrypted = decrypt(string=filecontentencrypted, key=cipherkey)

    outputDecryptedFilename = 'decrypted.txt'

    file.writeFile(outputDecryptedFilename, decrypted)
        
if __name__ == '__main__':
    main()