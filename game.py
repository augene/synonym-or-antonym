# Augene Pak
# Synonym or Antonym?

import json
import requests
import random

possible_words = list(open('words.txt').read().split())
word_list = ['']
data = ['']
score = 0
lost = False
play_again = "y"
syn_num = 0
ant_num = 0
random_number = 0
word_list = []

while play_again.startswith("y"):
    while not lost:
        # detect whether word exists in thesaurus
        while syn_num == 0 or ant_num == 0:
            i = 0
            syn_num = 0
            ant_num = 0

            # get random word that exists in API
            word = possible_words[random.randint(0, len(possible_words) - 1)]
            random_num = random.randint(0, 1)

            # request data using word
            rqst_st = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
            response = requests.get(rqst_st)
            data = json.loads(response.text)

            if str(type(data)) == "<class 'dict'>":
                continue

            for i in range(len(data[0]["meanings"])):
                syn_num += \
                    len(data[0]["meanings"][i]["definitions"][0]["synonyms"])
                ant_num += \
                    len(data[0]["meanings"][i]["definitions"][0]["antonyms"])

            # if (random_num == 0 and syn_num == 0) or \
            #         (random_num == 1 and ant_num == 0):
            #     syn_num = 0
            #     ant_num = 0
            #     continue

        # stores appropriate word list
        # if synonym list doesn't exist, switch to antonym list; vice versa
        if random_num == 0:
            for i in range(len(data[0]["meanings"])):
                word_list += \
                    data[0]["meanings"][i]["definitions"][0]["synonyms"]
        else:
            for i in range(len(data[0]["meanings"])):
                word_list += \
                    data[0]["meanings"][i]["definitions"][0]["antonyms"]

        # remove duplicates
        word_list = set(word_list)
        word_list = list(word_list)

        # select random word to pair with first word
        word2 = word_list[random.randint(0, len(word_list) - 1)]

        print(word + " & " + word2)
        response = input("Synonym or Antonym? (s/a) ")

        # only allow responses starting with s or a
        while not (response.startswith("s") or response.startswith("a")):
            print("Try again")
            response = input("Synonym or Antonym? (s/a) ")

        if (response.lower().startswith("s") and random_num == 0) or \
                (response.lower().startswith("a") and random_num == 1):
            print("Success!\n")
            score += 1
            data = ['']
        else:
            print("Failure :(\n")
            lost = True
        syn_num = 0
        ant_num = 0
        word_list = []

    # display if game ends
    print("Your score is " + str(score) + ".")

    play_again = input("Play again? (y/n) ")
    while not (play_again.startswith("y") or play_again.startswith("n")):
        print("Try again")
        play_again = input("Play again? (y/n) ")

    if play_again.startswith("y"):
        lost = False
        data = ['']
        score = 0
        print("-----------------------------------------------------")
    elif play_again.startswith("n"):
        print("\nThanks for playing!")
