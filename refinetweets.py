import stanza
from stanza.server import CoreNLPClient

def refineTweets(tweet):
    tweet_data = []
    word_dep = []
    with CoreNLPClient(annotators=['pos', 'ner'], memory='4G', endpoint='http://localhost:9001', be_quiet=True) as client1:
        document = client1.annotate(tweet)
        for sent in document.sentence:
            for t in sent.token:
                tweet_data.append([t.word, t.pos, t.ner, t.tokenBeginIndex])

    with CoreNLPClient(annotators=['depparse'], memory='4G', endpoint='http://localhost:9001', be_quiet=True) as client2:
        dep_document = client2.annotate(tweet)
        for sent in dep_document.sentence:
            for d in sent.basicDependencies.edge:
                if d.dep=='amod' or d.dep=='nsubj' or d.dep=='dobj':
                    word_dep.append([d.dep, d.source, d.target])
    
    return tweet_data, word_dep
