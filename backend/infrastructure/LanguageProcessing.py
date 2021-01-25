# Imports
import spacy
from enum import Enum
from spacy.symbols import PROPN, NOUN, CCONJ, ADP, VERB
import numpy as np


class RelationDirection(Enum):
    NONE = 1
    START = 2
    DEST = 3


class RelationStrength(Enum):
    NONE = 1
    WEAK = 2
    STRONG = 3


class LanguageProcessing:

    class WordSense:
        def __init__(self, word: str, direction: RelationDirection, strength: RelationStrength):
            self.word = word
            self.direction = direction
            self.strength = strength

        def __str__(self):
            return f"Word '{self.word}' has a direction of {self.direction.name} and a {self.strength.name} strength."

        def __repr__(self):
            return f"Word '{self.word}' has a direction of {self.direction.name} and a {self.strength.name} strength."

    class LinkedWordSense:
        def __init__(self, word: str, fixedWord: str, direction: RelationDirection, strength: RelationStrength):
            self.word = word
            self.fixedWord = fixedWord
            self.direction = direction
            self.strength = strength

        def __str__(self):
            return f"Words '{self.word}' fixed with '{self.fixedWord}' has a direction of {self.direction.name} and a {self.strength.name} strength."

        def __repr__(self):
            return f"Words '{self.word}' fixed with '{self.fixedWord}' has a direction of {self.direction.name} and a {self.strength.name} strength."

    # CCONJ links: 'cc'_child
    CCONJ_Relation = [
        # Start
        WordSense("depuis", RelationDirection.START, RelationStrength.STRONG),
        # Destination
        WordSense("puis", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("et", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("enfin", RelationDirection.DEST, RelationStrength.STRONG)
    ]

    # NOUN links: 'nmod'_parent
    NOUN_Relation = [
        # Start
        WordSense("provenance", RelationDirection.START,
                  RelationStrength.STRONG),
        # Destination
        WordSense("direction", RelationDirection.DEST, RelationStrength.WEAK),
        WordSense("destination", RelationDirection.DEST, RelationStrength.WEAK)
    ]

    # ADP_FIXED has the priority
    # ADP links: 'case'_child, 'dep'_parent
    ADP_FIXED_Relation = [
        # Start
        LinkedWordSense("à", "partir", RelationDirection.START,
                        RelationStrength.STRONG),
        LinkedWordSense("en", "partant", RelationDirection.START,
                        RelationStrength.STRONG),
        # Destination
        LinkedWordSense("à", "destination",
                        RelationDirection.DEST, RelationStrength.STRONG),
        LinkedWordSense("en", "direction",
                        RelationDirection.DEST, RelationStrength.WEAK)
    ]
    ADP_Relation = [
        # Start
        WordSense("de", RelationDirection.START, RelationStrength.STRONG),
        WordSense("du", RelationDirection.START, RelationStrength.STRONG),
        WordSense("des", RelationDirection.START, RelationStrength.STRONG),
        WordSense("depuis", RelationDirection.START, RelationStrength.STRONG),
        # Destination
        WordSense("à", RelationDirection.DEST, RelationStrength.WEAK),
        WordSense("au", RelationDirection.DEST, RelationStrength.WEAK),
        WordSense("aux", RelationDirection.DEST, RelationStrength.WEAK),
        WordSense("dans", RelationDirection.DEST, RelationStrength.WEAK),
        WordSense("en", RelationDirection.DEST, RelationStrength.WEAK),
        # par : "passer par Paris"
        WordSense("par", RelationDirection.DEST, RelationStrength.WEAK)
    ]

    # VERB links: 'obl:arg'_parent, 'obl:mod'_parent
    # "partir" is ambiguous: "partir de ..." "partir à ..."
    VERB_MARK_Relation = [
        WordSense("après", RelationDirection.START, RelationStrength.STRONG),
        WordSense("avant", RelationDirection.DEST, RelationStrength.STRONG)
    ]
    VERB_Relation = [
        # Start
        WordSense("décoller", RelationDirection.START,
                  RelationStrength.STRONG),
        WordSense("passer", RelationDirection.START, RelationStrength.WEAK),
        WordSense("être", RelationDirection.START, RelationStrength.STRONG),
        # Destination
        WordSense("arriver", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("aller", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("visiter", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("atterrir", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("découvrir", RelationDirection.DEST,
                  RelationStrength.STRONG),
        WordSense("voyager", RelationDirection.DEST, RelationStrength.STRONG),
        WordSense("rendre", RelationDirection.DEST, RelationStrength.STRONG)
    ]

    def analyseRequest(self, request):
        print(f"Request: {request}")
        nlp = spacy.load("fr_core_news_lg")
        doc = nlp(request)
        locations = []
        fullTrip = []

        # Extract locations
        for i in doc.ents:
            if i.label_ == 'LOC' or i.label_ == 'GPE':
                locations.append(i.text)
        print(f"Locations found: {locations}")

        if len(locations) <= 1:
            print("Cannot parse request or invalid request.")
        else:
            # Get token for each locations
            tokens = np.zeros(len(locations), dtype=object)
            for i in range(len(locations)):
                tokenFound = False
                # Priority: PROPN
                for token in doc:
                    if token.pos == PROPN:
                        isUsable = True
                        for tokenSelected in tokens:
                            if type(tokenSelected) != int and tokenSelected == token:
                                isUsable = False
                        if isUsable:
                            if token.text in locations[i]:
                                tokens[i] = token
                                tokenFound = True
                                break

                # Secondary: NOUN
                if tokenFound == False:
                    for token in doc:
                        if token.pos == NOUN:
                            isUsable = True
                            for tokenSelected in tokens:
                                if type(tokenSelected) != int and tokenSelected == token:
                                    isUsable = False
                            if isUsable:
                                if token.text in locations[i]:
                                    tokens[i] = token
                                    tokenFound = True
                                    break

                # Failsafe: any (e.g in "Je veux faire Paris Gare De l'Est Marseille": Marseille is parsed as a VERB)
                if tokenFound == False:
                    for token in doc:
                        isUsable = True
                        for tokenSelected in tokens:
                            if type(tokenSelected) != int and tokenSelected == token:
                                isUsable = False
                        if isUsable:
                            if token.text in locations[i]:
                                tokens[i] = token
                                tokenFound = True
                                break

                # None
                if tokenFound == False:
                    print(f"Localization {locations[i]} not found")
                    tokens[i] = None

            # Remove None tokens
            tmpTokens = tokens
            tokens = []
            for token in tmpTokens:
                if token != None:
                    tokens.append(token)

            # Weight tokens to prepare ordering
            weighedTokens = np.zeros(len(tokens), dtype=object)
            for i in range(len(tokens)):
                print(f"Token #{i + 1} : {tokens[i].lemma_}")
                foundWeight = []
                parent = tokens[i].head

                # CCONJ
                for child in tokens[i].children:
                    if child.pos == CCONJ:
                        for ref in self.CCONJ_Relation:
                            if ref.word == child.lemma_:
                                print(
                                    f"Found CCONJ: {ref.word} - {ref.strength.name}")
                                foundWeight.append(ref)
                                break

                # NOUN
                if len(foundWeight) <= 0:  # Not prioritary over CCONJ
                    if parent.pos == NOUN:
                        for ref in self.NOUN_Relation:
                            if ref.word == parent.lemma_:
                                print(
                                    f"Found NOUN: {ref.word} - {ref.strength.name}")
                                foundWeight.append(ref)
                                break

                # ADP_FIXED
                if len(foundWeight) <= 0:  # Not prioritary over CCONJ and NOUN
                    for child in tokens[i].children:
                        if child.pos == ADP:
                            for subChild in child.children:
                                if subChild.dep_ == 'fixed':
                                    for ref in self.ADP_FIXED_Relation:
                                        if ref.word == child.lemma_ and ref.fixedWord == subChild.lemma_:
                                            print(
                                                f"Found ADP_FIXED: {ref.word} {ref.fixedWord}")
                                            foundWeight.append(ref)
                                            break

                # ADP
                if len(foundWeight) <= 0:  # Not prioritary over CCONJ, NOUN and ADP_FIXED
                    for child in tokens[i].children:
                        for ref in self.ADP_Relation:
                            if ref.word == child.lemma_:
                                print(
                                    f"Found ADP: {ref.word} - {ref.strength.name}")
                                foundWeight.append(ref)
                                break

                # VERB_MARK
                if len(foundWeight) <= 1:  # Prioritary over CCONJ, NOUN and ADP_FIXED
                    if parent.pos == VERB:
                        for child in parent.children:
                            if child.dep_ == 'mark' and child.pos == ADP:
                                for ref in self.VERB_MARK_Relation:
                                    if ref.word == child.lemma_:
                                        print(
                                            f"Found VERB_MARK: {ref.word} - {ref.strength.name}")
                                        foundWeight.append(ref)
                                        break

                # VERB
                if len(foundWeight) <= 1:  # Prioritary over CCONJ, NOUN, ADP_FIXED and VERB_MARK
                    for ref in self.VERB_Relation:
                        if ref.word == parent.lemma_:
                            print(
                                f"Found VERB: {ref.word} - {ref.strength.name}")
                            foundWeight.append(ref)
                            break

                # Default - Keep position
                if len(foundWeight) == 0:  # Fallback
                    print(f"Using default weight")
                    foundWeight.append(self.WordSense(
                        "default", RelationDirection.DEST, RelationStrength.WEAK))

                # Extract first strong relation
                selectedWeight = None
                for j in range(len(foundWeight)):
                    if foundWeight[j].strength == RelationStrength.STRONG:
                        selectedWeight = foundWeight[j]
                        break
                if selectedWeight is None:
                    selectedWeight = foundWeight[0]

                print(f"Using: {selectedWeight.word}")
                print("---------------")
                weighedTokens[i] = (tokens[i], selectedWeight)

            # Order tokens
            orderedTokens = []
            # First pass for direction: START
            for i in range(len(weighedTokens)):
                token, weight = weighedTokens[i]
                numberOfStrongStrength = 0
                if weight.direction == RelationDirection.START:
                    if weight.strength == RelationStrength.STRONG:
                        orderedTokens.insert(numberOfStrongStrength, token)
                        numberOfStrongStrength = numberOfStrongStrength + 1
                    else:
                        orderedTokens.append(token)

            # Second pass for direction: DEST
            numberOfStrongStrength = 0
            for i in range(len(weighedTokens)):
                token, weight = weighedTokens[i]
                if weight.direction == RelationDirection.DEST:
                    if weight.strength == RelationStrength.STRONG:
                        orderedTokens.append(token)
                        numberOfStrongStrength = numberOfStrongStrength + 1
                    else:
                        if numberOfStrongStrength == 0:
                            orderedTokens.append(token)
                        else:
                            orderedTokens.insert(
                                len(orderedTokens) - numberOfStrongStrength, token)

            # Populate full trip cities list
            for token in orderedTokens:
                fullTrip.append(token.text)
            print(f"Result trip: {fullTrip}")

            # DEBUG
            # for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
            # displacy.serve(doc, style="dep")

            return fullTrip

    # TESTS
    requests = [
        ("J'aimerais aller d'Orléans à Paris puis dans les Vosges",
         ["Orléans", "Paris", "Vosges"]),
        ("Je veux aller à Marseille à partir de Lyon", ["Lyon", "Marseille"]),
        ("Je veux visiter Paris en partant de Bordeaux et en passant par Nantes", [
         "Bordeaux", "Nantes", "Paris"]),
        ("Je veux prendre le train à Mulhouse à destination de Strasbourg",
         ["Mulhouse", "Strasbourg"]),
        ("Strasbourg en provenance de Mulhouse", ["Mulhouse", "Strasbourg"]),
        ("Je veux aller de Mulhouse à Strasbourg", ["Mulhouse", "Strasbourg"]),
        ("Je veux faire Paris Gare De l'est Marseille",
         ["Paris", "Marseille"]),
        ("Je veux aller à Paris après être allé à Mulhouse depuis Lyon",
         ["Lyon", "Mulhouse", "Paris"]),
        ("Paris-Marseille", ["Paris", "Marseille"]),
        ("Je suis à Paris et je veux aller à Strasbourg avec mon amis Frank que je récupère à Mulhouse",
         ["Paris", "Mulhouse", "Strasbourg"]),
        ("Je souhaite une pizza napolitaine à Rome", []),
        ("Je veux aller à Lyon", [])
    ]

    def testNLP(self):
        for index in range(len(self.requests)):
            sentence, expectedResult = self.requests[index]
            result = self.analyseRequest(sentence)
            print(
                f"\n\n\n***************************    # {index}    ***************************")
            print(f"result:    {result}")
            print(f"exprected: {expectedResult}")
            print(
                "*****************************************************************\n\n\n")
