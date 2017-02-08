from __future__ import absolute_import
from __future__ import print_function

from buildbot.process import buildstep
from buildbot.process import logobserver
from buildbot.process.results import SUCCESS


class PopulateSecrets(buildstep.LoggingBuildStep):

    def __init__(self, secretskeys=None, provider=None):
        super(PopulateSecrets, self).__init__()
        self.secrets = secretskeys
        self.name = "PopulateSecrets"
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)

    def extract_stages(self, stdout):
        stages = []
        for line in stdout.split('\n'):
            stage = str(line.strip())
            if stage:
                stages.append(stage)
        return stages

    def run(self):
        # get all the secrets
        secretsDetailsList = []
        allservices = self.master.services
        print(allservices)
        credsservice = self.master.namedServices['secrets']
        for secret in self.secrets:
            secretsDetail = credsservice.get(secret)
            secretsDetailsList.append(secretsDetail)
        return SUCCESS
