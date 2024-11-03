"""Terminal-based game, where the user guesses whether two words are synonyms or antonyms."""

# Augene Pak
# Synonym or Antonym?

import random
import pandas as pd

LINE_LENGTH = 145

def generate_synonyms_antonyms_dict():
    """Return an in-memory dictionary of synonyms & antonyms from external file."""
    synonyms_antonyms_df = pd.read_csv('data/english_synonyms_and_antonyms.csv', sep='\t',
                                     names=['word', 'synonyms', 'antonyms']).fillna('')

    synonyms_antonyms_dict = {}
    for row in range(len(synonyms_antonyms_df)):
        word = synonyms_antonyms_df.iloc[row]['word']
        synonyms = synonyms_antonyms_df.iloc[row]['synonyms'].split(', ')
        antonyms = synonyms_antonyms_df.iloc[row]['antonyms'].split(', ')

        if synonyms == ['']:
            synonyms = []

        if antonyms == ['']:
            antonyms = []

        synonyms_antonyms_dict[word] = {'synonyms': synonyms, 'antonyms': antonyms}
    return synonyms_antonyms_dict

def print_synonym_or_antonym_ascii():
    """Prints the introductory ASCII art."""
    # Generated using https://patorjk.com/software/taag/#p=display&h=0&f=Standard&t=Synonym%20or%20Antonym%3F
    print(" ____                                                                              _              _                                         ___ ")      
    print("/ ___|   _   _   _ __     ___    _ __    _   _   _ __ ___       ___    _ __       / \\     _ __   | |_    ___    _ __    _   _   _ __ ___   |__ \\")
    print("\\___ \\  | | | | | '_ \\   / _ \\  | '_ \\  | | | | | '_ ` _ \\     / _ \\  | '__|     / _ \\   | '_ \\  | __|  / _ \\  | '_ \\  | | | | | '_ ` _ \\    / /")
    print(" ___) | | |_| | | | | | | (_) | | | | | | |_| | | | | | | |   | (_) | | |       / ___ \\  | | | | | |_  | (_) | | | | | | |_| | | | | | | |  |_| ")
    print("|____/   \\__, | |_| |_|  \\___/  |_| |_|  \\__, | |_| |_| |_|    \\___/  |_|      /_/   \\_\\ |_| |_|  \\__|  \\___/  |_| |_|  \\__, | |_| |_| |_|  (_) ")
    print("         |___/                           |___/                                                                          |___/                   ")
    print(" " * LINE_LENGTH)
    print("=" * LINE_LENGTH)


def select_word_pair(synonyms_antonyms, possible_words):
    """Randomly select and return tuple of words that are synonyms or antonyms to each other."""
    word_1 = possible_words[random.randint(0, len(possible_words) - 1)]

    synonyms = synonyms_antonyms[word_1]['synonyms']
    antonyms = synonyms_antonyms[word_1]['antonyms']

    # if there are no synonyms, choose from antonyms; vice versa
    # syn_or_ant -> synonym = 0, antonym = 1
    if not synonyms:
        syn_or_ant = 1
        word_2 = antonyms[random.randint(0, len(antonyms) - 1)]
    elif not antonyms:
        syn_or_ant = 0
        word_2 = synonyms[random.randint(0, len(synonyms) - 1)]

    else:
        # 0 = synonym, 1 = antonym
        syn_or_ant = random.randint(0, 2)
        if syn_or_ant == 0:
            synonyms = synonyms_antonyms[word_1]['synonyms']
            word_2 = synonyms[random.randint(0, len(synonyms) - 1)]
        else:
            antonyms = synonyms_antonyms[word_1]['antonyms']
            word_2 = antonyms[random.randint(0, len(antonyms) - 1)]

    return (word_1, word_2, syn_or_ant)

def play_game():
    """Runs the main game logic."""
    print_synonym_or_antonym_ascii()

    synonyms_antonyms = generate_synonyms_antonyms_dict()
    possible_words = list(synonyms_antonyms.keys())

    play_again = 'y'
    lost = False
    while play_again.startswith('y'):
        score = 0
        while not lost:
            print('Score: ' + str(score))
            word_1, word_2, syn_or_ant = select_word_pair(synonyms_antonyms, possible_words)

            print(word_1 + ' & ' + word_2)
            response = input('Synonym or Antonym? (s/a) ').lower()

            # only allow responses starting with s or a
            while not (response.lower().startswith('s') or response.lower().startswith('a')):
                response = input('Please enter either s or a! (s/a) ').lower()

            if (response.startswith('s') and syn_or_ant == 0) or \
                    (response.startswith('a') and syn_or_ant == 1):
                print('Correct :)')
                print('-' * LINE_LENGTH)
                score += 1
            else:
                print('Incorrect :(')
                print('-' * LINE_LENGTH)
                lost = True

        # display if game ends
        print('Your final score is ' + str(score) + '.')
        print('-' * LINE_LENGTH)

        play_again = input('Play again? (y/n) ').lower()
        while not (play_again.startswith('y') or play_again.startswith('n')):
            play_again = input('Please enter either y or n! (y/n) ').lower()

        print('=' * LINE_LENGTH)
        if play_again.startswith('y'):
            lost = False
            score = 0
        elif play_again.startswith('n'):
            print('Thanks for playing! :)')


play_game()
