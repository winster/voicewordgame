# A word game for children.

responses_dictionary = {'YOUR_TURN':['Now it\'s your turn!','Your turn!'], 
'TYPE_YOUR_WORD':['You have to say a word that starts with letter \'<first_letter>\'',
'Say a word that starts with \'<first_letter>\'','Your letter is \'<first_letter>\''],
'BOT_WORD_IS':['My word is...','And my word is...','And I say...'],
'OK_RESPONSE':['Nice! I like <user_word>','Hmm, <user_word>. Interesting',
  'Okay, <user_word>. Let me think of a nice one like that!', 
  'Interesting choice..<user_word>', 'Oh, I know <user_word>',
  'Ah..<user_word>! Wait for me.'],
'LAST_WORD':['So, my last word is...','And my last word is coming up!'],
'ERROR_WRONG_LETTER':['That doesn\'t seem to be the right word. Remember, the word has to start with letter \'<first_letter>\''],
'ERROR_ALREADY_SAID':['Oh, nice try, but <user_word> was already said!','No way. We already said that word','No, we already said <user_word>'],
'ERROR_BLANK_INPUT':['Sorry, I didn\'t get your word. Type a word that starts with letter \'<first_letter>\''],
'ERROR_NOT_ENGLISH_WORD':['Umm, <user_word> doesn\'t seem to be an English word',
  'Hmm, the English that I know doesn\'t list <user_word> as a word!',
  'No, <user_word> is not a valid word.']}

import random
import time
from nltk.corpus import words
from google.cloud import firestore
setofwords = set(words.words())

# This is the function that orchestrates the whole gameplay
def play_game(max_turns):
  
  turns = 0
  # Loading dictionary of bot words. Currently we have implemented only Level 1
  # words
  word_dictionary = load_dictionary('level1')
  said_words = []
  
  print ('Ok, let\'s start the game!')
  time.sleep(0.5)
  print ('I\'ll choose the first word')
  time.sleep(1)
  print('Hmmmmm.....it is.......')
  time.sleep(2)
  #First word is chosen from the dictionary at random
  bot_word = get_first_word()
  print(bot_word)
  #Add the word to the list of said words
  said_words.append(bot_word)
  print('Now, it\'s your turn!')
  time.sleep(0.5)
  print(randomised_response('',bot_word,'TYPE_YOUR_WORD'))
  user_word = get_user_word(bot_word, said_words)
  said_words.append(user_word)    
  turns+=1
  
  while turns<max_turns:
    print (randomised_response(str(user_word),bot_word,'OK_RESPONSE'))
    time.sleep(1)
    if turns == max_turns-1:
      print(randomised_response('','','LAST_WORD'))
    else:
      print(randomised_response('','','BOT_WORD_IS'))
    bot_word = get_next_word(word_dictionary,str(user_word),said_words)
    if bot_word != 'ERROR_BOT_LOSES':
      said_words.append(bot_word)
      time.sleep(2)
      print(bot_word)
      time.sleep(0.5)
      print(randomised_response('','','YOUR_TURN'))
      time.sleep(0.5)
      print(randomised_response('',bot_word,'TYPE_YOUR_WORD'))
      user_word = get_user_word(bot_word, said_words)   
      said_words.append(user_word)    
      turns+=1
    else:
      print('Oh no, I lose. Well played!')
      break
                                          
  print ('Thanks for playing. That was fun! Hope we can play again! :) :o)')
  return 

# Function to get user's word. Once input is received this function calls the
# validate_word function to identify if the entered word is valid as defined 
# in that function. If not, an error message is displayed to the user and a 
# recursive call to get_user_word function is made until a valid word is entered
def get_user_word(bot_word, said_words):
  
  user_word = input("Type your word: ")
  validation = validate_word(str(user_word), bot_word, said_words)
  if validation.startswith('ERROR'):
    print (randomised_response(str(user_word),bot_word,validation))
    user_word = get_user_word(bot_word, said_words)     
  return str(user_word)
 
# Function to validate the word entered by the user. It checks if the user's word
# begins with the last letter of the bot's word and if the word was already said
# in the current game. Validation of whether the word exists in English 
# dictionary needs to be added
def validate_word(user_word, bot_word, said_words):

# validate for blank inputs
  if (len(user_word)<1):
    validation = 'ERROR_BLANK_INPUT'
  elif (user_word[0] != bot_word[-1]):
    validation = 'ERROR_WRONG_LETTER'
  elif user_word in said_words:
    validation = 'ERROR_ALREADY_SAID'
  elif user_word not in setofwords:
    validation = 'ERROR_NOT_ENGLISH_WORD'
  else:
    validation = 'VALID'
  return validation

# Function to validate bot word. Currently it checks for not null and also 
# whether the word was said earlier in the current game
def validate_bot_word(bot_word, said_words):

  if bot_word in said_words:
    return False
  elif not bot_word:
    return False
  else:
    return True
 
# This function is meant to randomise the bot responses for various scenarios,
# so that the conversation is not monotonous. The message is made dynamic using
# the relevant letter or word in the message, wherever it makes sense.
def randomised_response(user_word,bot_word,response_type):
  
  responses = list(responses_dictionary.get(response_type))
  if ((response_type in ['TYPE_YOUR_WORD','ERROR_WRONG_LETTER','ERROR_BLANK_INPUT'])):  
    response = random.choice(responses)
    response = response.replace('<first_letter>',bot_word[-1])
  elif response_type in ['OK_RESPONSE','ERROR_ALREADY_SAID','ERROR_NOT_ENGLISH_WORD']:
    response = random.choice(responses)
    response = response.replace('<user_word>',user_word.lower())
  else:
    response = random.choice(responses)
  return response

# Function to get the first word, chosen at random from the dictionary. Used only
# for the first time in the game.
def get_first_word():
  word_dictionary = load_dictionary('level1')
  
  letters = list(word_dictionary.keys())
  letter = random.choice(letters)
  words = list(word_dictionary.get(letter))
  word = random.choice(words)
  return word

# Function to get all the subsequent bot words. It also invokes the 
# validate_bot_word function to validate the bot word before responding to
# the user. If a suitable word cannot be found, the function returns an error
def get_next_word(word_dictionary, user_word, said_words):
  
  letter = user_word.lower()[-1]
  if(word_dictionary.get(letter)):
    words = list(word_dictionary.get(letter))
    word = random.choice(words)
    validation = validate_bot_word(word, said_words)
    if not validation:
      unsaid_words = list(set(words)-set(said_words))
      if len(unsaid_words)>0:
        word = random.choice(unsaid_words)
      else:
        word = 'ERROR_BOT_LOSES'
  else:
    word = 'ERROR_BOT_LOSES'
  return word

# Function to load dictionary. Currently only loading from text file has been 
# implemented. In the future, other methods like reading from a database or API
# can be implemented
def load_dictionary(level):
  
  return load_dictionary_from_file(level)

# Load dictionary from text file. In the current design, one file contains words
# related to one level only.
def load_dictionary_from_file(level):
  filename = 'dictionary_'+level+'.txt'
  word_dictionary = {}
  dictionary_values=[]
  f = open(filename, 'r')
  for line in f:
    # The file specifies the beginning of a list of words that start with a new 
    # letter by prefixing '~~' to the letter. (e.g. ~~b)
    if line.startswith('~~'):
      # Extract the letter after ~~
      key = str(line)[2]
      # Clear the array
      dictionary_values=[]
    else:
      word=str(line)
      # Remove \n character from the end
      word = word.replace('\n','')
      cleaned_word = word
      if(key in word_dictionary):
        # Append the existing array in the dictionary with the new word
        dictionary_values = word_dictionary.get(key)
        dictionary_values.append(cleaned_word)
        word_dictionary[key] = dictionary_values
      else:
        dictionary_values.append(cleaned_word)
        word_dictionary[key] = dictionary_values
  f.close()
  # print (word_dictionary)
  return word_dictionary


# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():
  max_turns = 5
  
  play_game(max_turns)

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
