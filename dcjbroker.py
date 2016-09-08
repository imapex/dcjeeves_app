__author__ = 'mtokarz'

from ucsd import ucsdworker
import dcjeevessentence



class dcjbroker():

    # Create a new broker
    def __init__(self,sentence,scrawlfile):
        self.sentence = dcjeevessentence.dcjeevessentence(sentence)
        self.scrawl = scrawlfile

    def execute(self):
        cloud = self.sentence.cloud
        type = self.scrawl.gettype(cloud)
        command = self.sentence.command
        params = self.sentence.getkeys()

        print(command)


        # We currently only support UCSD
        if (type=="UCSD"):
            worker = ucsdworker.ucsdworker(self.scrawl.getip(cloud),self.scrawl.getrestapikey(cloud))
            worker.execute(command,params)

        else:
            return "Cloud type ("+type+") is not supported"



