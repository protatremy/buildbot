from __future__ import absolute_import
from __future__ import print_function

from twisted.internet import defer
from twisted.trial import unittest

from buildbot.process.properties import Secret
from buildbot.secrets.manager import SecretManager
from buildbot.test.fake import fakemaster
from buildbot.test.fake.fakebuild import FakeBuild
from buildbot.test.fake.secrets import FakeSecretStorage
from buildbot.util.service import BuildbotService


class FakeBuildWithMaster(FakeBuild):

    def __init__(self, master):
        super(FakeBuildWithMaster, self).__init__()
        self.master = master

class FakeServiceUsingSecrets(BuildbotService):

    name = "FakeServiceUsingSecrets"
    renderables = [Secret("foo")]

    def reconfigService(self, *args, **kwargs):
        self.kwargs = kwargs

    def returnRenderedSecrets(self, secretKey):
        try:
            return getattr(self, secretKey)
        except Exception as e:
            print("[EXCEPTION] e!", str(e))
            raise Exception


class FakeServiceUsingSecretsNotFound(FakeServiceUsingSecrets):

    name = "FakeServiceUsingSecrets2"
    renderables = [Secret("more")]


class TestRenderSecrets(unittest.TestCase):

    def setUp(self):
        self.master = fakemaster.make_master()
        fakeStorageService = FakeSecretStorage(secretdict={"foo": "bar",
                                                       "other": "value"})
        self.secretsrv = SecretManager()
        self.secretsrv.services = [fakeStorageService]
        self.secretsrv.setServiceParent(self.master)
        self.srvtest = FakeServiceUsingSecrets()
        self.srvtest.setServiceParent(self.master)
        self.successResultOf(self.master.startService())

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.master.stopService()

    def test_secret_rendered(self):
        self.assertEqual("bar", self.srvtest.returnRenderedSecrets("foo"))

    @defer.inlineCallbacks
    def test_secret_rendered_not_found(self):
        new = FakeServiceUsingSecretsNotFound()
        yield self.srvtest.reconfigServiceWithSibling(new)
        print("[DEBUG] ", self.srvtest.returnRenderedSecrets("more"))

    def test_secret_render_no_secretkey(self):
        self.assertRaises(Exception, self.srvtest.returnRenderedSecrets, "more")
