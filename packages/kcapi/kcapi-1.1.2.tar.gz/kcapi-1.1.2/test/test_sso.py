import unittest, time
from kcapi import OpenID, Keycloak
from .testbed import TestBed 

ADMIN_USER = "admin"
ADMIN_PSW  = "admin1234"
REALM = "test_heroes_test"
ENDPOINT = 'https://sso-cvaldezr-stage.apps.sandbox-m2.ll9k.p1.openshiftapps.com'


TEST_REALM = "TESTING"

class Testing_SSO_API(unittest.TestCase):
    def testing_CRUD_api(self):
        realm = self.master_realm

        resp = realm.create({"enabled": "true", "id": TEST_REALM, "realm": TEST_REALM})
        self.assertEqual(resp.isOk(), True)

        findings = realm.get(TEST_REALM).verify().resp().json()
        self.assertEqual(findings['id'], TEST_REALM)

        obj = {'displayName':"MyRealm" }
        state_update = realm.update(TEST_REALM, obj).isOk()
        self.assertEqual(state_update, True)

        updated_object = realm.get(TEST_REALM).verify().resp().json()
        self.assertEqual(updated_object['displayName'], "MyRealm")

        exists = realm.exist(TEST_REALM) 
        self.assertTrue(exists)

        do_not_exists = realm.exist("DoesntExist") 
        self.assertFalse(do_not_exists)

        remove_state = realm.remove(TEST_REALM).isOk()
        self.assertEqual(remove_state, True)

    def testing_findFirstByKV(self): 
        users = self.kc.build("users", self.realm) 
        batman = users.findFirstByKV('firstName', 'Bruce')
        self.assertEqual(batman['username'], 'batman')

    def testing_updateUsingKV(self): 
        users = self.kc.build("users", self.realm) 
        status = users.updateUsingKV('firstName', 'Bruce', {'firstName': 'Bruno', 'lastName': 'Diaz'})
        self.assertTrue(status)
        batman = users.findFirstByKV('firstName', 'Bruno')
        self.assertEqual(batman['username'], 'batman')
        self.assertEqual(batman['firstName'], 'Bruno')
        self.assertEqual(batman['lastName'], 'Diaz')

    def testing_existByKV(self): 
        users = self.kc.build("users", self.realm) 
        batman = users.existByKV('firstName', 'Bruce')
        self.assertEqual(batman, True )

    def testing_removeFirstByKV(self):
        users = self.kc.build("users", self.realm) 
        all_users = users.findAll().verify().resp().json()

        self.assertEqual(len(all_users), 3)
        aqua = users.removeFirstByKV('username', 'aquaman')
        self.assertTrue(aqua)

        all_users = users.findAll().verify().resp().json()
        self.assertEqual(len(all_users), 2)
        for usr in all_users: 
            self.assertTrue( usr['username'] in ['batman', 'superman'] )

        

    def testing_client_API(self): 
        client_payload = {"enabled":True,"attributes":{},"redirectUris":[],"clientId":"deleteme","protocol":"openid-connect"}

        clients = self.kc.build("clients", self.realm)
        state = clients.create(client_payload).isOk()
        self.assertEqual(state, True)

    def testing_client_API(self): 
        clientAPI = self.kc.build("clients", self.realm)
        state = clientAPI.findAll().verify().resp()
        self.assertEqual(state.status_code, 200)
     
    
    def testing_with_no_token(self): 
        try:
            self.kc = Keycloak(None, ENDPOINT)
            self.assertTrue(False)
        except Exception as E: 
            self.assertEqual("No authentication token provided" in str(E), True)

        try:
            self.kc = Keycloak('placeholder', None)
            self.assertTrue(False)
        except Exception as E: 
            self.assertEqual("No Keycloak endpoint URL" in str(E), True)

    def testing_roles_creation_and_removal(self):
        role_name = 'magical_2'
        role = {"name": role_name}
        roles = self.kc.build("roles", self.realm)
        state = roles.create(role).isOk() 
        self.assertTrue(state)

        magic_role = roles.findFirstByKV('name', role_name)
        self.assertIsNotNone(magic_role, "The role named magic should be in the server.")


        self.assertTrue(roles.removeFirstByKV("name", role_name))
        magic_role = roles.findFirstByKV('name', role_name)
        self.assertEqual(magic_role, [], "The role named magic should be deleted from the server.")

    def testing_case_sensitive_resource(self):
        myCaseTrickyUser = {"enabled":'true',"attributes":{},"username":"The Punisher","firstName":"Bruce", "lastName":"Wayne", "emailVerified":""}

        users = self.kc.build('users', self.realm) 
        state = users.create(myCaseTrickyUser).isOk()
        self.assertTrue(state)

        removed = users.removeFirstByKV('username', 'The Punisher')
        self.assertTrue(removed)

        is_empty = not users.findFirstByKV('username', 'The Punisher')
        self.assertTrue(is_empty)

    @classmethod
    def setUpClass(self):
        self.testbed = TestBed(REALM, ADMIN_USER, ADMIN_PSW, ENDPOINT)
        self.testbed.createRealms()
        self.testbed.createUsers()
        self.testbed.createClients()
        self.kc = self.testbed.getKeycloak()
        self.realm = self.testbed.REALM 
        self.master_realm = self.testbed.getAdminRealm()
        
    @classmethod
    def tearDownClass(self):
        self.testbed.goodBye()
        if self.master_realm.exist(TEST_REALM): 
            self.master_realm.remove(TEST_REALM)
            return True
        return True

if __name__ == '__main__':
    unittest.main()
