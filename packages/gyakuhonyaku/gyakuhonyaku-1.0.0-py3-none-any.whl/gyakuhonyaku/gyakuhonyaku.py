from googletrans import Translator
translator = Translator()
def gyakuhonyaku(word:str):
  a=translator.translate(word, dest='en')
  b=translator.translate(a.text, dest='ko')
  c=translator.translate(b.text, dest='en')
  d=translator.translate(c.text, dest='de')
  e=translator.translate(d.text, dest='en')
  f=translator.translate(e.text, dest='ja')
  print(f.text)
