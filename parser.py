import os
import codecs
from html.parser import HTMLParser

path = './colecao_teste/'

class SGMLParser(HTMLParser):
  def __init__(self, raise_exception = True) :
    HTMLParser.__init__(self)
    self.doc = "" # Resultado final do parsing. Formato esperado: um JSON com os dados de cada documento por linha
    self.process_data = True # Define se os dados dentro da tag devem ser lidos

  # IRRELEVANTE, IGNORAR ###############################################################################################
  @property
  def json(self):
    return self.doc
         
  @staticmethod
  def to_json(content, raise_exception = True):
      parser = SGMLParser()
      parser.feed(content)
      return parser.json
  ######################################################################################################################
  
  def handle_starttag(self, tag, attrs):
    if (tag == 'doc'):
      self.doc += "{"
    elif (tag == 'docid' or tag == 'category'):
      self.process_data = False
    else:
      self.doc += f'"{tag}": '

  def handle_endtag(self, tag):
    if (tag == 'doc'):
      self.doc += '}\n'
    elif (tag == 'docid' or tag == 'category'):
      self.process_data = True
    elif (tag != 'text'):
      self.doc += ', '

  def handle_data(self, data):
    if len(data) > 1 and self.process_data:
      escaped_data = data.replace('"', '\\"').replace('\n', ' ').replace('\r', '')
      # STEMMING E REMOÇÃO DE STOPWORDS OCORRERIA AQUI
      self.doc += f'"{escaped_data}"'

parser = SGMLParser()

json_output = open(f'colecao.json', 'w+')
for filename in os.listdir(path):
  with codecs.open(f'{path}{filename}', 'r', encoding='latin-1') as sgml_input:
    json_output.write(parser.to_json(sgml_input.read()))
json_output.close()