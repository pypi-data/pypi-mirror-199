def encrypt(str):
    words = ["a","e","i","o","u"]
    code = ["2","1","3","5","4"]
    upper_words = ["A","E","I","O","U"]
    upper_code = ["7","6","8","0","9"]
    for i in range(5):
        str = str.replace(words[i],code[i])
        str = str.replace(upper_words[i],upper_code[i])
    return str

def decrypt(str):
    words = ["a","e","i","o","u"]
    code = ["2","1","3","5","4"]
    upper_words = ["A","E","I","O","U"]
    upper_code = ["7","6","8","0","9"]
    for i in range(5):
        str = str.replace(code[i],words[i])
        str = str.replace(upper_code[i],upper_words[i])
    return str
