"""process.py"""
# pylint: disable=C0103
import os
import pickle
import re

#DIR = "data/republican_primary/"
#DIR = "data/democratic_primary/"
DIR = "data/general_election/"
REGEX_ALPHABET = "[^abcdefghijklmnopqrstuvwxyz]"

#compile stopwords to filter out of data
with open("data/stopwords-en.txt", "r", encoding="utf-8") as f:
    stopwords = [re.sub(REGEX_ALPHABET, "", i) for i in re.split("\n", f.read().lower())]

walk = [x for x in os.walk(DIR)]

# collect file paths of all files to read
txt_files = {}
for i,j in enumerate(walk[0][1]):
    db = {}
    txt_files[j] = []
    for k in os.listdir(DIR + j):
        if k[-4:] == ".txt":
            txt_files[j].append(DIR + j + '/' + k)

# read the files and save the word occurences to a db
for i,j in txt_files.items():
    db = {}
    for k in txt_files[i]:
        with open(k, "r", encoding="utf-8") as f:
            speaker = ""
            for line in f:
                line = line.lower()
                colon_index = -1
                try: # identify the speaker if it changed from previous lines
                    colon_index = line.index(":")
                    speaker = line[:colon_index]
                    line = line[colon_index:]
                    # ^ inclusive to not go out of bounds. regex will remove it.
                except (ValueError, RuntimeError) as e:
                    pass
                if speaker in db:
                    db[speaker].append(line)
                else:
                    db[speaker] = [line]

            # for l in re.split(" |\n", f.read().lower()):
            #     l = re.sub(REGEX_ALPHABET, "", l)
            #     if l in db:
            #         db[l] += 1
            #     else:
            #         db[l] = 1
    # get rid of stopwords in the db
    # for word in stopwords:
    #     db.pop(word, None) # remove all stopwords that exist, return None for those that don't
    # TODO: remove the following, this was done to filter speakers
    with open("data/speakers.txt", "a", encoding="utf-8") as spfile:
        for name in db:
            spfile.write(name + "\n")
    with open(DIR + i + "b", "wb") as dbfile: # dump the database
        pickle.dump(db, dbfile)

with open("data/republican_primary/2008b", "rb") as f:
    db = pickle.load(f)

x = [i for i in db]
print(x)
