# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members
from twisted.internet import defer

from buildbot.process.properties import Interpolate
from buildbot.steps.shell import ShellCommand
from buildbot.test.util.integration import RunMasterBase


# This integration test creates a master and worker environment,
# with one builders and a shellcommand step
# meant to be a template for integration steps
class SecretsConfig(RunMasterBase):

    @defer.inlineCallbacks
    def test_secret(self):
        yield self.setupConfig(masterConfig())

        change = dict(branch="master",
                      files=["foo.c"],
                      author="me@foo.com",
                  comments="good stuff",
                      revision="HEAD",
                      project="none"
                      )
        build = yield self.doForceBuild(wantSteps=True, useChange=change, wantLogs=True)
        self.assertEqual(build['buildid'], 1)


# master configuration
def masterConfig():
    c = {}
    from buildbot.config import BuilderConfig
    from buildbot.process.factory import BuildFactory
    from buildbot.plugins import steps, schedulers, util

    c['schedulers'] = [
        schedulers.AnyBranchScheduler(
            name="sched",
            builderNames=["testy"])]
    c['secretsManagers'] = [util.SecretInVault(
        vaultToken="8e77569d-0c39-2219-dfdf-7389a7bfe020",
        vaultServer="http://localhost:8200"
    )]

    f = BuildFactory()
    f.addStep(steps.PopulateSecrets(["password", "password2"]))
    f.addStep(ShellCommand(command=[Interpolate(
        'echo %(secrets:userpassword)s'), Interpolate('echo %(prop:password2)s')]))

    c['builders'] = [
        BuilderConfig(name="testy",
                      workernames=["local1"],
                      factory=f)]
    return c
