import re

class dcjeevessentence():
    # define key value pairs since they are not always created (not mandatory)
    #key_values = {}

    # Create a new sentence
    def __init__(self,sentence):
        self.key_values = {}
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

    # pushes out the sentence into a dictionary
    def dumptree(self):
        dumpdict = {}
        if len(self.key_values.keys()) > 0:
            dumpdict{}
            print self.key_values.keys()
        print self.environment
        return dumpdict



# sentence = dcjeevessentence("dcjeeves show vm status on <ENVIRONMENT> at <CLOUD> where a equals b and c equals d")
#
# if sentence.parse():
#     print "YES"
#     print sentence.__dict__
#     for k, v in sentence.getkeys().items():
#          print(k, v)
# else:
#     print "NO"