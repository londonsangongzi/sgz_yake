import yake
import sgz_yake as yake2

from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions
import syntok.segmenter as segmenter
from syntok.tokenizer import Tokenizer

import sys
sys.path.append('D:\IN_NOTEBOOK\sgz_modules')
import sgzUtils


def pre_filter( text):
    prog = re.compile("^(\\s*([A-Z]))")
    parts = text.split('\n')
    buffer = ''
    for part in parts:
        sep = ' '
        if prog.match(part):
            sep = '\n\n'
        buffer += sep + part.replace('\t',' ')
    return buffer


language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9 
deduplication_algo = 'seqm'
windowSize = 1 
numOfKeywords = 10

#text="""Everything Is Working. But it's being led by just five stocks. This was the narrative as the market was bouncing in March and April and even into May. That narrative wasn't necessarily wrong at the time, and yes, I was a part of the chorus, but that narrative no longer reflects reality."""
#text="""The Mail is saying that the SD holiday will definitely not be extended. Maybe Sunak has realised that he has created an even worse situation by doing what he did. Maybe he also realises that he is open to accusations of corruption by being seen to stoke an asset class that he has a lot of money invested in. Wouldn't normally stop a Tory, but I think he is actually a reasonably decent man. We will see. Fatso might sit on him and make him extend it after all. Quote. A source added that Mr Sunak has also rejected calls to extend the stamp duty holiday. Https://www.dailymail.co.uk/news/article-9128309/Rishi-Sunak-delay-tax-rises-autumn-end-Stamp-Duty-holiday-March.html"""


#==============  检测token划分精准度  =============
#"""
text="2010-02-18, hello-world_1981, jeff_susan-charlie@hotmail.com, Let's meet U.S.A. at 14.10 in N.Y.! \
This happened in the U.S. last week. no-deal legislation... In March and April and even into May.! \
They Want Max vol. 'Min-vol will have its day in the sun again, but right now, investors want max vol?' \
Https://www.dailymail.co.uk/news/article-9128309/Rishi-Sunak-delay-tax-rises-autumn-end-Stamp-Duty-holiday-March.html"
print(text)
text=sgzUtils.filter_content(text)
print(text)

print('\norgin yake(segtok):\n')
sentences_str = [ [w for w in split_contractions(web_tokenizer(s)) if not (w.startswith("'") and len(w) > 1) and len(w) > 0] for s in list(split_multi(text)) if len(s.strip()) > 0]
print(sentences_str)

print('\nnew yake(syntok):\n')
sentences_str2 = []
for paragraph in segmenter.process(text):
    for sentence in paragraph:
        sen = []
        for token in sentence:
            # exactly reproduce the input
            # and do not remove "imperfections"
            #print(token.spacing, token.value, sep='', end='') 
            sen.append(token.value)   
        sentences_str2.append(sen)
print(sentences_str2) 

#By default, spaCy uses its dependency parser to do sentence segmentation, which requires loading a statistical model. 
#The sentencizer is a rule-based sentence segmenter that you can use to define your own sentence segmentation rules without loading a model.
#Note that English() is a pretty generic model -you can find some more useful pre-trained statistical models here: https://spacy.io/models/en
print("\nspacy:\n")
from spacy.lang.en import English
nlp_senlist = English()
sentencizer = nlp_senlist.create_pipe("sentencizer")
nlp_senlist.add_pipe(sentencizer)
doc = nlp_senlist(text)
#sen_list = [sent.string.strip() for sent in doc.sents]
#print(sen_list)
sentence_tokens = [[token.text for token in sent] for sent in doc.sents]
print(sentence_tokens)
"""
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
tokens=[]
for token in doc:
    tokens.append(token.text)  
print(tokens) 
"""

#nltk不同标记器的优势 MosesTokenizer ToktokTokenizer word_tokenize
#   word_tokenize()隐式调用sent_tokenize()
#   ToktokTokenizer()是最快的
#   The tok-tok tokenizer is a simple, general tokenizer, where the input has one sentence per line; thus only final period is tokenized.
#       from nltk.tokenize.toktok import ToktokTokenizer
#       toktok = ToktokTokenizer()
#       toktok.tokenize('The went to http://google.com.') #['The', 'went', 'to', 'http://google.com', '.']
#   MosesTokenizer()能够取消文本的索引 
#       MosesTokenizer has been moved out of NLTK due to licensing, but we can still use it.
#       from somewhere import MosesTokenizer
#       moses = MosesTokenizer()
#       moses.tokenize('The went to http://google.com.')
#   ReppTokenizer()能够提供标记偏移量
print("\nnltk(word_tokenize):\n")
import nltk
tokens = [nltk.word_tokenize(sentence) for sentence in nltk.sent_tokenize(text)]
print(tokens)
#print(nltk.word_tokenize(text))#word_tokenize将隐式调用sent_tokenize
print("\nnltk(ToktokTokenizer) 2021.3.2 目前看这个最好！限制：句子结尾只认1个标点:\n")
from nltk.tokenize.toktok import ToktokTokenizer
toktok = ToktokTokenizer()
tokens = [toktok.tokenize(sentence) for sentence in nltk.sent_tokenize(text)]
print(tokens)
print("\nnltk(TweetTokenizer):\n")
from nltk.tokenize import TweetTokenizer
tweettok = TweetTokenizer()
tokens = [tweettok.tokenize(sentence) for sentence in nltk.sent_tokenize(text)]
print(tokens)
#"""
#==============  检测token划分精准度  =============


######################################################################################

"""
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keys = custom_kw_extractor.extract_keywords(text)
keys = [key[0] for key in keys if float(key[1])>0.0]
print('\norgin yake:\n',keys)
#['working', 'march and april', 'narrative', 'bouncing in march', 'longer reflects reality', 'may. that narrative', 'reflects reality', 'march', 'april', 'may.']

custom_kw_extractor2 = yake2.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keys2 = custom_kw_extractor2.extract_keywords(text)
keys2 = [key[0] for key in keys2 if float(key[1])>0.0]
print('\nnew yake:\n',keys2)
#['working', 'march and april', 'narrative', 'bouncing in march', 'march', 'april', 'stocks', 'market was bouncing', 'reflects reality', 'led']
"""

