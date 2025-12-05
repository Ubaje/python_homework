#Task 1
def hello():
    return "Hello!"

#Task 2
def greet(name):
    return f"Hello, {name}!"

#Task 3
def calc(x,y, op="multiply"):
    match op:
        case "add":
            return x + y
        case "subtract":
            return x - y
        case "multiply":
            try:
                ans = x * y
            except TypeError:
                return "You can't multiply those values!"
            else:
                return ans
        case "divide":
            try:
                ans = x / y
            except TypeError:
                return "You can't divide those values!"
            except ZeroDivisionError:
                return "You can't divide by 0!"
            else:
                return ans
        case "modulo":
            return x % y
        
#Task 4
def data_type_conversion(value, to_type):
    try:
        match to_type:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
    except ValueError:
        return f"You can't convert {value} into a {to_type}."

#Task 5
def grade(*args):
    try:
        avg = sum(args) / len(args)
    except TypeError:
        return "Invalid data was provided."
    else:
        match avg:
            case _ if avg >= 90:
                return "A"
            case _ if avg >= 80:
                return "B"
            case _ if avg >= 70:
                return "C"
            case _ if avg >= 60:
                return "D"
            case _ :
                return "F"
            
#Task 6
def repeat(string, count):
    result = ""

    for i in range(count):
        result += string

    return result

#Task 7
def student_scores(op, **kwargs):
    match op:
        case "best":
            top_score = 0
            top_student = ""

            for student, score in kwargs.items():
                if score > top_score:
                    top_score = score
                    top_student = student
            
            return top_student
        case "mean":
            return sum(kwargs.values()) / len(kwargs.values())
        
#Task 8
def titleize(title):
    words = title.split()
    little_words = {"a", "on", "an", "the", "of", "and", "is","in"}

    for i, word in enumerate(words):
        if word not in little_words:
            words[i] = words[i].capitalize()
    
    words[0] = words[0].capitalize()
    words[-1] = words[-1].capitalize()
    
    return " ".join(words)

#Task 9
def hangman(secret, guess):
    result = ""
    for char in secret:
        if char in guess:
            result += char
        else:
            result += "_"
    
    return result

#Task 10
def pig_latin(text):
    vowels = {"a","e","i","o","u"}
    words = text.split(" ")

    for i, word in enumerate(words):
        match word[0]:
            case _ if word[0] in vowels:
                words[i] = word + "ay"
            case _:
                j = 1;
                while word[j] not in vowels:
                    j += 1
                
                if word[j-1] == 'q':
                    words[i] = word[j+1:] + word[:j+1] + "ay"
                else:
                    words[i] = word[j:] + word[:j] + "ay"
    return " ".join(words)