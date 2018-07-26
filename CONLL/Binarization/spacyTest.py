import spacy
from spacy.pipeline import DependencyParser

nlp = spacy.load("fr")

#parser = DependencyParser(nlp.vocab)

doc2 = nlp(u"Une femme donne un cadeux à son mari")
doc1 = nlp(u"La complexité des législations entraîne nécessairement une spécialisation.")

doc3 = nlp(u"Six d' entre eux , seulement blessés , ont pu se réfugier sur l' autre rive de la Nipoué , en Côte - d' Ivoire , avant d' être transférés à man , dans un hôpital. ")
doc4 = nlp(u"La tâche des secouristes est immense , faute de moyens matériels et humains.")
doc5 = nlp(u"À Danané , le chef du secteur de santé rurale travaille en étroite collaboration avec une équipe très réduite de médecins sans frontières en attendant le renfort imminent de la Croix - rouge nationale et internationale.")
#processed = parser(doc)

from spacy import displacy

#displacy.serve(doc1,style="dep")
#displacy.serve(doc2,style="dep")
#displacy.serve(doc3,style="dep")
#displacy.serve(doc4,style="dep")
#displacy.serve(doc5,style="dep")

#displacy.serve(doc1,style="ent")
#displacy.serve(doc2,style="ent")
#displacy.serve(doc3,style="ent")
#displacy.serve(doc4,style="ent")
docs = [doc1,doc2,doc3,doc4,doc5]
displacy.serve(docs,style="ent",port=5001)