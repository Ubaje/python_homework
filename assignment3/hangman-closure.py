#Task 4
def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        reveled_word = ""
        
        for x in secret_word:
            if x.lower() in guesses:
                reveled_word += x
            else:
                reveled_word += "_"
            
        print(reveled_word)

        all_guessed = all(ch.lower() in guesses for ch in secret_word)
        return all_guessed
    return hangman_closure


if __name__ == "__main__":
    secret = input("Enter the secret word: ").strip()
    hangman = make_hangman(secret)

    print("\nStart guessing letters!\n")

    guessed = False
    while not guessed:
        letter = input("Guess a letter: ").strip()
        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a single letter.")
            continue

        guessed = hangman(letter)

    print(f"\nYou guessed the word '{secret}'!")