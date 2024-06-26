import sys
import fileinput
import json
import collections
import re
import time
import os
start_time = time.time()

total_results_list = []
total_medications_list = []
total_supplements_list = []

supplement_file = fileinput.input("txts/supplements.txt", encoding="utf-8")
supplement_list = []
for line in supplement_file:
    items = line.strip().split(", ")
    line = [items[0]] + [item.lower() for item in items]
    supplement_list.append(line)

medication_file = fileinput.input("txts/medications.txt", encoding="utf-8")
medication_list = []
for line in medication_file:
    items = line.strip().split(", ")
    line = [items[0]] + [item.lower() for item in items]
    medication_list.append(line)

sys.stdout.reconfigure(encoding='utf-8')

reading_filename = "mydatav1.jsonl"
writing_filename = "mydatav2.jsonl"

file = fileinput.input(reading_filename, encoding="utf-8")
data = [json.loads(line) for line in file]

try:
    os.remove('mydatav2.jsonl')
except Exception:
    pass

i = 0
for dictionary in data:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    body = url_pattern.sub('', dictionary["body"])

    filtered_words_list = [word.lower() for word in body
                      .replace(' im ',' ')
                      .replace('.',' ')
                      .replace('!',' ')
                      .replace(',', ' ')
                      .replace('?',' ')
                      .replace('(',' ')
                      .replace(')', ' ')
                      .replace('’', '\'')
                      .replace('&amp;#x200b;', ' ')
                      .replace('\"', ' ')
                      .replace('/', ' ')
                      .replace('=', ' ')
                      .replace('*', ' ')
                      .replace('<', ' ')
                      .replace('>', ' ')
                      .replace(':', ' ')
                      .replace('\n\n-', ' ')
                      .replace('\n-', ' ')
                      .replace(' -', ' ')
                      .replace('- ', ' ')
                      .replace('•', ' ')
                      .replace('\n', ' ')
                      .replace('background-color:', ' ')
                      .replace('--condition_highlight', ' ')
                      .split()]
    
    filtered_words = " ".join(filtered_words_list)
    
    # Identify medications
    for item in medication_list:
        keyterm = item[0]
        find_terms = sorted([med for med in item[1:] if '!' not in med], key=len, reverse=True)
        avoid_terms = [med for med in item if '!' in med]

        for word in find_terms:
            if (" " + word + " " in filtered_words) and (not any(w in filtered_words for w in avoid_terms)):
                pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                dictionary["body"] = pattern.sub('<span class="' + keyterm[::-1].replace(" ", "-").replace("(", "-").replace(")", "-").replace("/", "-").replace("'", "-") + " medication" + '" style="background-color: var(--medication_highlight); border-radius: 3px;">' + word + '</span>', dictionary["body"])

                if keyterm not in dictionary["medications"]:
                    dictionary["medications"].append(keyterm)
                    total_results_list.append(keyterm)
                    total_medications_list.append(keyterm)

    # Identify supplements
    for item in supplement_list:
        keyterm = item[0]
        find_terms = sorted([sup for sup in item[1:] if '!' not in sup], key=len, reverse=True)
        avoid_terms = [sup for sup in item if '!' in sup]

        for word in find_terms:
            if (" " + word + " " in filtered_words.lower()) and (not any(w in filtered_words for w in avoid_terms)):
                pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                dictionary["body"] = pattern.sub('<span class="' + keyterm[::-1].replace(" ", "-").replace("(", "-").replace(")", "-").replace("/", "-").replace("'", "-") + " supplement" + '" style="background-color: var(--supplement_highlight); border-radius: 3px;">' + word + '</span>', dictionary["body"])

                if keyterm not in dictionary["supplements"]:
                    dictionary["supplements"].append(keyterm)
                    total_results_list.append(keyterm)
    
    # if there's at least some medication or supplement, store it
    if (len(dictionary["medications"]) or len(dictionary["supplements"])):
        with open(writing_filename, "a") as json_file:
            json_file.write(json.dumps(dictionary))
            json_file.write("\n")
        json_file.close()

    # get an update on how far into the process we are
    i += 1
    if (i % 100 == 0):
        print(i)

for item in collections.Counter(total_results_list).most_common():
    print(item[1], item[0])

elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Elapsed time: {minutes} minutes {seconds} seconds")