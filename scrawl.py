#__author__ = 'mytokarz'

import yaml

class scrawl():

    def __init__(self, filename):
        '''
        Read in the scrawl yaml configuration file and store it as an object
        :param filename: path to the yaml file
        :return:
        '''
        datamap = {}

        try:
            f = open(filename)
            # use safe_load instead load
            self.datamap = yaml.safe_load(f)
            f.close()
        except yaml.YAMLError as exc:
            print(exc)

        # Lowercase all the CLOUD keys, easier to search and validat later
        self.datamap = dict((k.lower(), v) for k, v in self.datamap.iteritems())

        # Lowercase all the ENVIRONMENT keys, easier to search adn validate later
        for k in self.datamap.keys():
            t = []
            for list in self.datamap[k]['ENVIRONMENTS']:
                t.append(dict((k.lower(), v) for k, v in list.iteritems()))
            self.datamap[k]['ENVIRONMENTS'] = t


    def validateenvcloud(self,env,cloud):
        '''
        :param env: find the environment under the cloud passed in
        :param cloud: find the cloud with the name passed in
        :return: true if cloud and enviroment exists
        '''
        if cloud.lower() in self.datamap:
            for k in (self.datamap[cloud.lower()]["ENVIRONMENTS"]):
                if env.lower() in k:
                    return 1
        return 0

    def listenvcloud(self):
        '''
        Get list of the ENVIRONMENT and CLOUD mappings
        :return: JSON of all ENVIRONMENT and CLOUD mappings
        '''


    def listenvfromcloud(self,cloud):
        '''
        Get list of ENVIRONMENT from passed in CLOUD
        :param cloud:
        :return: JSON of all ENVIRONMENTs from passed in CLOUD.  None if CLOUD not found
        '''



# Used for stand alone debugging
#myYaml = scrawl('scrawl.yaml')
#if myYaml.validateenvcloud("dEv","RoSemont"):
#    print "Exists!"
