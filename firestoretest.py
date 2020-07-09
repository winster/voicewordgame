# Playground to learn handling data in Cloud Firestore

import random
import firebase_admin
import csv
from firebase_admin import credentials
from firebase_admin import firestore
from wordgame import load_dictionary_from_file


# initializations 
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def load_dictionary_to_db(filename):
  
  f = open(filename, 'r')
  reader = csv.reader(f, delimiter=',')
  for row in reader:
    clues = []
    # pick values from csv row
    level, letter, word, last_letter, clue1, clue2 = row
    # make clue array
    if clue1 != '':
      clues.append(clue1)
      if clue2 != '':
        clues.append(clue2)
    word_data = {
      'last_letter':last_letter,
      'clues':clues
    }
    
    collection_path = 'words/'+level.strip()+'/'+letter.strip()
    print(collection_path, word, 'data: ',word_data)
    word_ref = db.collection(collection_path).document(word)
    word_ref.set(word_data,merge=True)
    print ('added', word)
    
  f.close()
  return    

# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():
  
  #project-404326690342
  # [START quickstart_get_collection]
  word_dictionary_ref = db.collection('word_dictionary/1/a')
  docs = word_dictionary_ref.stream()
  
  for doc in docs:
      print(f'{doc.id} => {doc.to_dict()}')
  

 # 
 # word_data = {
 #   'last_letter':'t',
 #   'clues':['Clue 1','Clue 2']
 # }
  
 # word_dictionary_ref.document('act').set(word_data)
   
  # [END quickstart_get_collection]

  load_dictionary_to_db('word_dictionary.csv')

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
