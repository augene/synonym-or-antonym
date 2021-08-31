english = list(open('vocab/english.txt', encoding="utf8").read().split())
words_alpha = list(open('vocab/words_alpha.txt').read().split())

list1_as_set = set(english)
intersection = list1_as_set.intersection(words_alpha)

intersection_as_list = list(intersection)
print(len(intersection_as_list))

with open('words.txt', 'w') as f:
    for line in intersection_as_list:
        f.write(line)
        f.write('\n')
