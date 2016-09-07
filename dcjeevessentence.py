__author__ = 'mytokarz'
import re

class dcjeevessentence():

    # Create a new sentence
    def __init__(self,sentence):
        self.key_values = {}
        self.where = 0
        self.sentence = sentence

    # Dissect a sentence and verify it matches the syntax supported.
    #
    # Supported structures
    # dcjeeves <COMMAND> on <ENVIRONMENT> at <CLOUD>
    # dcjeeves <COMMAND> on <ENVIRONMENT> at <CLOUD> where <KEY1> equals <VALUE1>
    # dcjeeves <COMMAND> on <ENVIRONMENT> at <CLOUD> where <KEY1> equals <VALUE1> and <KEY2> equals <VALUE2> ...
    #
    # Return true if it matches syntax
    # Return false if we can't parse
    def parse(self):
        passed_input = self.sentence.rstrip()

        # split at the 'where' clause
        split_me = re.split('\s+where\s+',passed_input,1, re.IGNORECASE)

        # Verify the begining clause up to <CLOUD> is correct
        match_me = re.match('^\s*dcjeeves\s+(.+)\s+(?:on)\s+(.+)\s+(?:at)\s+(.+)$',split_me[0], re.IGNORECASE)

        if match_me:
            self.command = match_me.group(1)
            self.environment = match_me.group(2)
            self.cloud = match_me.group(3)
        else:
            return 0

        # Get key values pairs if 'where' clause is used
        if len(split_me)>1:
            self.where = 1  # set the flag that there are keys
            values = split_me[1]
            while (values):
                # split at the next 'and' if applicable
                split_next = re.split('\s+and\s+',values,1, re.IGNORECASE)
                # parse the key value pair
                match_next = re.match('^\s*(.+)\s+(?:equals)\s+(.+)\s*$',split_next[0], re.IGNORECASE)
                if match_next:
                    self.key_values[match_next.group(1)]=match_next.group(2)
                    if len(split_next) > 1:
                        values = split_next[1]
                    else:
                        # no more key value pairs, done
                        break
                else:
                    # Key value pair regex didn't match, syntax error in sentence passed in
                    return 0
        # great looks like everything parsed the way we wanted it to
        return 1

    # Return the key value pairs
    def getkeys(self):
        return self.key_values

    def containswhere(self):
        return self.where

#Used for stand alone debugging
# sentence = dcjeevessentence("dcjeeves show vm status on <ENVIRONMENT> at <CLOUD> where MIKE equals AWESOME and c equals d")
#
# if sentence.parse():
#     print ("Good input")
#     print (sentence.__dict__)
#     for k, v in sentence.getkeys().items():
#          print(k, v)
# else:
#     print ("Bad input")