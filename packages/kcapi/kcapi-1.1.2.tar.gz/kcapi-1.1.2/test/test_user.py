import unittest, time
from kcapi import OpenID, RestURL
from .testbed import TestBed


class Testing_User_API(unittest.TestCase):
    def test_adding_credentials_to_user(self):

        username = 'batman'
        passphrase = '123456'
        users = self.testbed.getKeycloak().build('users', self.REALM)
        state = users.update_credentials(username, passphrase, False).isOk()
        self.assertTrue(state)

        oid_client = OpenID({
            "client_id": "dc",
            "username": username,
            "password": passphrase,
            "grant_type": "password",
            "realm": self.REALM
        }, self.testbed.ENDPOINT)

        token = oid_client.getToken()
        self.assertNotEqual(token, None)

    @classmethod
    def setUpClass(self):
        self.testbed = TestBed()
        self.testbed.createRealms()
        self.testbed.createUsers()
        self.testbed.createClients()
        self.REALM = self.testbed.REALM

    @classmethod
    def tearDownClass(self):
        self.testbed.goodBye()


if __name__ == '__main__':
    unittest.main()
