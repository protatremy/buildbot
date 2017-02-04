Secrets
-------

.. code-block:: python

  class SecretDetails(object):
      """
      ...
      """

      def __init__(self, provider, key, value, props=None):
          if props is None:
              props = dict()

A secretDetails is a python object initialized with a provider name, a key, a value and properties if needed.
Each parameter is an object property that should be returned the value.
Secrets founded are stored in a SecretDetails.

Secrets manager
---------------

The manager is a Buildbot service.

.. code-block:: python

    secretsService = self.master.namedServices['secrets']
    secretsDetailsList = secretsService.get(self.secrets)

The service execute a get method.
Depending on the kind of storage chosen and declared in the configuration, the manager get the selected provider and return a list of secretsDetails.

Secrets providers
-----------------

The secrets providers are implementing the specific getters, related to the storage chosen.

File provider
`````````````

.. code-block:: python

    c['secretsManagers'] = [util.SecretInFile(directory="/path/toSecretsFiles"]

In the master configuration the provider is instantiated through a Buildbot service secret manager with the file directory path.
File secrets provider reads the file named by the key wanted by Buildbot and returns the contained text value.
The provider SecretInFile allows Buildbot read secrets in the secret directory.

Vault provider
``````````````

.. code-block:: python

    c['secretsManagers'] = [util.SecretInVault(
    vaultToken=open('VAULT_TOKEN').read(),
    vaultServer="http://localhost:8200"
    )]

In the master configuration the provider is instantiated through a Buildbot service secret manager with the Vault token and the Vault server address.
Vault secrets provider access to Vault asking the key wanted by Buildbot and returns the contained text value.
The provider SecretInVAult allows Buildbot read secrets in Vault.

Secret Obfuscation
``````````````````

Secrets are never visible to the normal user via logs and thus are transmitted directly to the workers, using the :class:`Obfuscated`.
The class Obfuscated changes the password characters in ``####`` characters in the logs.
