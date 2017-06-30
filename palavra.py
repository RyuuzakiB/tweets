#coding=UTF-8
import unicodedata
from string import punctuation
def eh_palavra(s):
    s= "".join([x for x in s if x.isalpha()])  #tira pontuação e números das palavras
    if(len(s)>=2):
    	return s.lower()
    else:
    	return None
