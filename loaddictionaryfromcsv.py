# Load dictionary data from CSV file

import random
import firebase_admin
import csv
from firebase_admin import credentials
from firebase_admin import firestore


# DB initialization
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to load dictionary from a csv file to the cloud firestore database
def load_dictionary_to_db(filename):
  # Open file with the encoding used for Excel-generated csv files
  f = open(filename, 'r', encoding='utf-8-sig')
  reader = csv.reader(f, delimiter=',')

  for row in reader:
    clues = []
    # Read values from csv row into variables
    level, letter, word, last_letter, clue1, clue2 = row
    # Make clue array                                  
    if clue1 != '':
      clues.append(clue1)
      if clue2 != '':
        clues.append(clue2)
    word_data = {
      'last_letter':last_letter,
      'clues':clues
    }
    # Collection path where the document for the word has to be created
    # e.g. words/1/a
    collection_path = 'words/'+level.strip()+'/'+letter.strip()
    letter_ref = db.collection(collection_path)
     
#   docs = letter_ref.stream()
#   for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

    # Add word into the collection
    letter_ref.document(word).set(word_data,merge=True)
    print ('added', word)

  f.close()
  return    


def main():

  load_dictionary_to_db('word_dictionary.csv')

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
