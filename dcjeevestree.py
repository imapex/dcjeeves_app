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
#   {'dcjeeves': {'start vm': {'on': {'PROD': {}}}}}
#


from dcjeevessentence import dcjeevessentence
import json

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

    def getjson(self):
        return json.dumps(self.mytree,indent=4)

    # Search the tree structure for a sentence to see if its part of tree
    def includes(self,sentence):
        return 0


# Used for testing
tree = dcjeevestree()
tree.add("dcjeeves start vm on PROD at <CLOUD> where vm name equals <VALUE1> and a equals b")
tree.add("dcjeeves stop vm on QA at <CLOUD> where vm name equals <VALUE1>")
tree.add("dcjeeves stop vm on DEV at <CLOUD>")

print tree.getjson()

