# FRENCH CCGBANK CORPUS

These codes are implemented to generate a combinatory categorial grammar french corpus based on the French Treebank corpus.

## Corpus
We used the French Tree Bank corpus under CONLL format with their Postag and dependency tree information. - [Links](http://ftb.linguist.univ-paris-diderot.fr/)
## Requirements

Python 3.5 or later

## Running
Using command in linux environnment:
```python
python ./generate.py
```
## Output

ID  | Form  | Lemma | Xpostag  | Upostag  |  | Dep  | Head  | CCG tag
--- | --- | --- | --- | --- | --- | --- | --- | --- 
1   |	La |	le |	D |	DET |	2 |	det |	2 |	NP/NP 
2 |	tâche |	tâche |	N |	NC |	5 |	suj |	5 |	NP
3 |	des  |	de |	P+D |	P+D |	2 |	dep |	2 |	(NP\NP)/NP
4 |	secouristes |	secouriste |	N	 |NC |	3	 |obj.p	 |3	 |NP
5 |	est |	être |	V	 |V	 |0 |	root |	0 |	(S\NP)/NP
6 |	immense	 |immense |	A	 |ADJ	 |5 |	ats  |	5  |	NP/NP
7 |	,	 |, |	PONCT	 |PONCT	 |5 |	ponct	 |5 |	ponct
8 |	faute |	faute	 |N	 |NC |	5 |	mod |	5	 |NP
9 |	de |	de |	P	 |P |	8 |dep_cpd |	8	 |NP/NP
10 |	moyens	 |moyen	 |N |	NC |	8 |	obj.p |	8 |	NP
11 |	matériels  |	matériel |	A  |	ADJ	 | 10  |	mod  |	10  |	(NP\NP)/NP
12	 | et  |	et  |	C  |	CC  |	11  |	coord  |	11  |	ponct
13	 | humains  |	humain  |	A  |	ADJ |	12 |	dep.coord |	12  |	NP\NP
14	 | .	 |. |	PONCT |	PONCT |	5 |	ponct |	5 |	ponct


