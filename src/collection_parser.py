import os
import re
import codecs
import unicodedata
import functools
import nltk
from html.parser import HTMLParser

path = './collection/'

stemmer = nltk.stem.RSLPStemmer()
stopwords = nltk.corpus.stopwords.words('portuguese')

def strip_accents(text):
  try:
      text = unicode(text, 'utf-8')
  except NameError: # unicode is a default on python 3 
      pass

  text = unicodedata.normalize('NFD', text)\
          .encode('ascii', 'ignore')\
          .decode("utf-8")

  return str(text)

def process_tokens(obj, token):
  if token.lower() not in stopwords:
    unaccented_string = strip_accents(token)
    try:
      obj.append(stemmer.stem(unaccented_string))
    except:
      if token not in ['º', 'ª', '²']:
        print(f'{token} não foi processado.')
  return obj

class SGMLParser(HTMLParser):
  def __init__(self, raise_exception = True) :
    HTMLParser.__init__(self)
    self.doc = "" # Resultado final do parsing. Formato esperado: um JSON com os dados de cada documento por linha
    self.cur_tag = "" # Guarda tag para handle_data
    self.process_data = True # Define se os dados dentro da tag devem ser lidos
    self.tracked_tags = ["doc", "docno", "text"]

  @property
  def json(self):
    return self.doc
         
  @staticmethod
  def to_json(content, raise_exception = True):
      parser = SGMLParser()
      parser.feed(content)
      return parser.json
  
  def handle_starttag(self, tag, attrs):
    if (tag == 'doc'):
      self.doc += "{"
    elif (tag not in self.tracked_tags):
      self.process_data = False
    else:
      self.doc += f'"{tag}": '
      self.cur_tag = tag

  def handle_endtag(self, tag):
    if (tag == 'doc'):
      self.doc += '}\n'
    elif (tag not in self.tracked_tags):
      self.process_data = True
    elif (tag != 'text'):
      self.doc += ', '

  def handle_data(self, data):
    if len(data) > 1 and self.process_data:
      if self.cur_tag == "text":
        tokens = re.findall(r"[\w'-]+", data)
        tokens = list(functools.reduce(process_tokens, tokens, []))
        data = " ".join(tokens)
      self.doc += f'"{data}"'

parser = SGMLParser()

json_output = open(f'collection.json', 'w+')
for filename in os.listdir(path):
  with codecs.open(f'{path}{filename}', 'r', encoding='latin-1') as sgml_input:
    json_output.write(parser.to_json(sgml_input.read()))
json_output.close()