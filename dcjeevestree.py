# Tree data structure that represents the utterance file
#
# Used to easily add sentences, check if a sentence is in the data structure and
# export out the sentences in various formats.
#
#
# Each word in the sentence is stored in recursive dictionary
#
# Example
# Sentenece
#   dcjeeves start vm on PROD at <CLOUD>
# Stored as nested dictionary
#   {'dcjeeves': {'start vm': {'on': {'PROD': {'at': {'<CLOUD>': }}}}}}}
#
__author__ = 'mytokarz'
from dcjeevessentence import dcjeevessentence
import json
import sys


class dcjeevestree():
    mytree = {}

    def __init__(self):
        tree = {}

    # Add a new sentence to the tree
    def add(self,sentence):
        sentence = dcjeevessentence(sentence)
        sentence.parse()

        temptree = self.mytree
        temptree = temptree.setdefault('dcjeeves',{})
        temptree = temptree.setdefault(sentence.command,{})
        temptree = temptree.setdefault('on',{})
        temptree = temptree.setdefault(sentence.environment,{})
        temptree = temptree.setdefault('at',{})
        temptree = temptree.setdefault(sentence.cloud,{})
        count = 0
        for k, v in sentence.getkeys().items():
            if count == 0:
                temptree = temptree.setdefault('where',{})
            else:
                temptree = temptree.setdefault('and',{})
            temptree = temptree.setdefault(k,{})
            temptree = temptree.setdefault('equals',{})
            temptree = temptree.setdefault(v,{})
            count += 1
        return 1

    # Dump out the tree in JSON format
    def getjson(self):
        return json.dumps(self.mytree,indent=4)

    # Search the tree structure for a sentence to see if its known
    def includes(self,sent):
        print "Validating sentence: " + sent

        # First verify the sentence
        sentence = dcjeevessentence(sent)
        sentence.parse()
        try:
            cmd_utter = self.mytree['dcjeeves'][sentence.command]['on']['<ENVIRONMENT>']['at']['<CLOUD>']
            print "Everything before possible where clause matches"

            if sentence.containswhere():        # take action if where clause was used
                print "where clause found"
                cmd_utter = cmd_utter['where']  # Strip off the where
                print "Key and values expected: " + str(cmd_utter)
                print "Key and values passed in: " + str(sentence.getkeys())

                # Go through each key value pair and strip off while check the tree
                for k, v in sentence.getkeys().items():



        except:
            print "The sentence passed in does not match any utterances"
            print 'Passed in sentence: ' + sent
            return 0

        # Second verify the scrawl substitutions


        return 1


# Used for stand alone debugging
# tree = dcjeevestree()
# tree.add("dcjeeves start vm on PROD at <CLOUD> where vm name equals <VALUE1> and a equals b")
# tree.add("dcjeeves stop vm on QA at <CLOUD> where vm name equals <VALUE1>")
# tree.add("dcjeeves stop vm on DEV at <CLOUD>")
#
# print tree.getjson()

