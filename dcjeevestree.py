# Tree data structure that represents the utterance file
#
# We will just be converting each possible
from dcjeevessentence import dcjeevessentence
import json

class dcjeevestree():

    def __init__(self):
        tree = {}

    # Add a new sentence to the tree
    def add(self,sentence):
        sentence = dcjeevessentence(sentence)
        sentence.parse()

        sentence.dumptree()

        return 1

    # Search the tree structure for a sentence to see if its part of tree
    def includes(self,sentence):

        return 0

    #

tree = dcjeevestree()

tree.add("dcjeeves start vm on PROD at <CLOUD> where vm name equals <VALUE1>")
tree.add("dcjeeves stop vm on QA at <CLOUD> where vm name equals <VALUE1>")
tree.add("dcjeeves stop vm on DEV at <CLOUD>")