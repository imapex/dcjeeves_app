#__author__ = 'mytokarz'

import yaml
import sys

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
        self.datamap = dict((k.lower(), v) for k, v in self.datamap.items())

        # Lowercase all the ENVIRONMENT keys, easier to search adn validate later
        for k in self.datamap.keys():
            t = []
            for list in self.datamap[k]['ENVIRONMENTS']:
                t.append(dict((k.lower(), v) for k, v in list.items()))
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
        :return: dict of all ENVIRONMENT and CLOUD mappings
        '''
        mapping = {}
        print ("List ENVIRONMENT and CLOUD mappings")
        for k in (self.listcloud()):
                # envs = ()
                # for j in self.datamap[k]['ENVIRONMENTS']:
                #     envs.append(list(j)[0])
                #     print ("CLOUD : "+k+" | ENVIRONMENT : "+list(j)[0])
            mapping[k] = self.listenvfromcloud(k)
        return mapping

    def listcloud(self):
        '''
        Get list of the CLOUD mappings
        :return: dict of all CLOUD mappings
        '''
        print ("List CLOUDS")
        clouds = {}
        for k in self.datamap:
            print ("CLOUD: "+k)
            clouds[k] = None
        return clouds

    def listenvfromcloud(self,cloud):
        '''
        Get list of ENVIRONMENT from passed in CLOUD
        :param cloud:
        :return: dict of all ENVIRONMENTs from passed in CLOUD.  None if CLOUD not found
        '''
        env = []
        try:
            print ("List ENVIRONMENTS from CLOUD: \""+cloud+"\"")
            for k in self.datamap[cloud.lower()]['ENVIRONMENTS']:
                for j in k.keys():
                    print ("ENVIRONMENT: "+j)
                env.append(j)
            return env
        except:
            print ("problem getting environments from cloud \""+cloud+"\"," +str(sys.exc_info()[0]))
        return None


# Used for stand alone debugging
myYaml = scrawl('scrawl.yaml')
#if myYaml.validateenvcloud("dEv","RoSemont"):
#    print ("Exists!")

#myYaml.listenvcloud()
#myYaml.listcloud()
#myYaml.listenvfromcloud("Rosemont")
#print (myYaml.validateenvcloud('qA','roseMont'))

# if myYaml.validateenvcloud('dev','Rosemont'):
#     print ("Valid environment and cloud passed in")
# else:
#     print ("Environment and Cloud not found")