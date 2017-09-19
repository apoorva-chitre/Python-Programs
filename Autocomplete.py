
# Program that reads text from a text file and then stores the words in a data structure and 
# then simulates the autocomplete feature such as in search engines and also provides related stats.

__author__ = 'Apoorva Chitre'

import unicodedata

wordlist = []

# function creates the required data structure for storing the words at the right place
def add(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(word)):

        try:
            alpha = wordlist[i]
            alpha[word[i]] += [word]
            wordlist[i] = alpha
        except:
            alpha = {}
            for letter in alphabet:
                alpha[letter] = []
            wordlist.append(None)
            alpha[word[i]] += [word]
            wordlist[i] = alpha


filename = input("Please enter a txt file name to search: ")

fileobj = open(filename, "r")
lines = fileobj.readlines()
fileobj.close()

worddict = {}

for line in lines :
    words = line.split()

    # Strip each word with any special characters and make it lowercase
    for word in words:
            w = word.strip(",.!'\"()")
            w = word.lower()

            # to strip vowel accents from the words
            w = ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn')
            w = ''.join(c for c in w if c.isalpha())

            # counting the occurences of each word and storing them in the dictionary,
            # where word is the key and count is the value

            if len(w) > 1:
                if worddict.get(w, None) :
                    worddict[w] += 1
                else:
                    worddict[w] = 1
            add(w)

choice = "yes"
while choice == "yes" :
    word = input('Enter start of a word: ')
    results = []

    # based on the start of the word input received,
    # extracting the possible words from the data structure using intersection of groups

    for i in range(len(word)):
        if len(results) == 0:
            results = set(wordlist[i][word[i]])
        else:
            results = set(results) & set(wordlist[i][word[i]])
    results = list(results)
    frequency = {}
    for each in results:
        frequency[each] = worddict.get(each,None) # extracting the occurrence count for each suggested word

    frequency_sorted = sorted(frequency, key=frequency.__getitem__, reverse = True)# sorting by dictionary values of occurrences
    total = 0

    # calculating the total occurrences of the sorted set
    for k in frequency_sorted :
        total += int(frequency[k])

    # Displaying the top 5 word suggestions with their %likelihood of occurrence
    print("Word" , "% likelihood",sep="\t")
    for k in frequency_sorted[0:5] :
        print(k,(worddict[k]/total)*100,sep="\t\t")

    choice = input("Do you want to continue? yes or no :")


#Sample outputs :

#C:\Users\lg\AppData\Local\Programs\Python\Python35-32\python.exe C:/Users/lg/PycharmProjects/CSCI6651/Autocomplete.py
#Please enter a txt file name to search: dracula.txt
#Enter start of a word: to
#Word	% likelihood
#to		85.6124031007752
#took		2.666666666666667
#too		2.511627906976744
#told		1.550387596899225
#together		1.0852713178294573
#Do you want to continue? yes or no :yes
#Enter start of a word: li
#Word	% likelihood
#little		33.25092707045735
#like		11.61928306551298
#light		9.023485784919654
#life		5.933250927070458
#likely		2.966625463535229
#Do you want to continue? yes or no :yes
#Enter start of a word: st
#Word	% likelihood
#st		7.105719237435008
#street		7.105719237435008
#still		6.932409012131716
#strange		3.9861351819757362
#stood		3.032928942807626
#Do you want to continue? yes or no :no

