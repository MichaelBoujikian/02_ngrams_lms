import argparse
import os, re
import collections


def preprocess(line):
    # DO NOT CHANGE THIS METHOD unless you want to explore other options and discuss your finding in the report

    # get rid of the stuff at the end of the line (spaces, tabs, new line, etc.)
    line = line.rstrip()
    # lower case
    line = line.lower()
    # remove everything except characters and white space
    line = re.sub("[^a-z ]", '', line)
    # tokenized, not done "properly" but sufficient for now
    tokens = line.split()

    # adding $ before and after each token because we are working with bigrams
    tokens = ['$' + token + '$' for token in tokens]

    return tokens


def create_model(path):
    # This is just some Python magic ...
    # unigrams[key] will return 0 if the key doesn't exist
    unigrams = collections.defaultdict(int)
    # and then you have to figure out what bigrams will return
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))

    f = open(path, 'r')
    ## You shouldn't visit a token more than once
    count=0
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
            # FIXME Update the counts for unigrams and bigrams
            for n in token:
                unigrams[n] = unigrams.get(n, 0) + 1
                
                if count == 0:
                    pass
                else:
                    bigrams[prev, n] = bigrams.get((prev,n), 0) +1

                count+=1
                prev = n
                
            pass

    # FIXME After calculating the counts, calculate the smoothed log probabilities
    #newDict = collections.defaultdict(int)
    #newDict = dict()
    newDict = {}
    
    alphArray = 'abcdefghijklmnopqrstuvwxyz'
    for n in alphArray:
        for i in alphArray:
            value = (bigrams.get((n,i), 0)+1)/(unigrams.get(n, 0)+26)
            newDict[n, i] = value


    # return the actual model: bigram (smoothed log) probabilities and unigram counts (the latter to smooth
    # unseen bigrams in predict(...)

    return newDict


def predict(file, model_en, model_es):
    prediction = None

    # FIXME Use the model to make predictions.
    # FIXME: Predict whichever language gives you the highest (smoothed log) probability
    # - remember to do exactly the same preprocessing you did when creating the model (that's why it is a method)
    # - you may want to use an additional method to calculate the probablity of a text given a model (and call it twice)

    # prediction should be either 'English' or 'Spanish'

    model = create_model(file)

    # res = {key: model[key] - model_en.get(key, 0)
    #                    for key in model.keys()}

    # res2 = {key: model[key] - model_es.get(key, 0)
    #                    for key in model.keys()}

    res = {key:abs(model_en.get(key, 0) - model.get(key,0))
                       for key in model.keys()}
    res2 = {key:abs(model_es.get(key, 0) - model.get(key,0))
                       for key in model.keys()}
    

    value = 0
    value2 = 0
    for n in res.values():
        value += n
    for n in res2.values():
        value2 += n
    #print("value: ", value, " values2: ", value2)
    if value < value2:
        prediction = 'English'
    else:
        prediction = 'Spanish'

    return prediction


def main(en_tr, es_tr, folder_te):
    # DO NOT CHANGE THIS METHOD

    # STEP 1: create a model for English with en_tr
    model_en = create_model(en_tr)

    # STEP 2: create a model for Spanish with es_tr
    model_es = create_model(es_tr)

    # STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print("Prediction for English documents in test:")
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print(f"{f}\t{predict(f_path, model_en, model_es)}")

    folder = os.path.join(folder_te, "es")
    print("\nPrediction for Spanish documents in test:")
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print(f"{f}\t{predict(f_path, model_en, model_es)}")


if __name__ == "__main__":
    # DO NOT CHANGE THIS CODE

    parser = argparse.ArgumentParser()
    parser.add_argument("PATH_TR_EN",
                        help="Path to file with English training files")
    parser.add_argument("PATH_TR_ES",
                        help="Path to file with Spanish training files")
    parser.add_argument("PATH_TEST",
                        help="Path to folder with test files")
    args = parser.parse_args()

    main(args.PATH_TR_EN, args.PATH_TR_ES, args.PATH_TEST)
