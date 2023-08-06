from .crud import KeycloakCRUD
from .helper import ValidateParams
import requests


class Users(KeycloakCRUD):
    def __lazy_load_groups(self):
        groups = KeycloakCRUD()
        groups.token = self.token
        groups.targets = self.targets.copy()
        groups.targets.change('groups')

        return groups

    def __findGroup(self, group):
        groups = self.__lazy_load_groups()
        return groups.findFirst(group)

    def __userGroupMappingAPI(self, userID):
        kc = KeycloakCRUD()
        kc.token = self.token
        kc.targets = self.targets.copy()

        kc.targets.addResources([userID, 'groups'])
        return kc

    def joinGroup(self, user, group):
        userID = self.findFirst(user)['id']
        groupID = self.__findGroup(group)['id']

        requestBody = {'groupId': groupID, 'userId': userID}

        return self.__userGroupMappingAPI(userID).update(groupID, requestBody)

    def groups(self, user):
        userID = super().findFirst(user)['id']
        return self.__userGroupMappingAPI(userID).all()

    def leaveGroup(self, user, group):
        userID = super().findFirst(user)['id']
        groupID = self.__findGroup(group)['id']

        return self.__userGroupMappingAPI(userID).remove(groupID)

    def groupMapping(self, user):
        userID = self.findFirst(user)['id']
        return self.__userGroupMappingAPI(userID)

    def find_user(self, username):
        url = self.targets.url('read')
        search_url = str(url) + '?search=' + username + '&max=1'
        ret = requests.get(search_url, headers=self.headers())
        users = ret.json()
        if not users:
            raise Exception("User "+ username +"not found")

        return users[0]

    # credentials: {type: "password", value: "passphrases", temporary: true}
    # type: password is the credential type supported by Keycloak.
    # value: Here we put the passphrase (required) 
    # temporary: **true** Means that this password would works the first time but it will force the user to setup a new one. 
    def update_credentials(self, username, secret, temporary=True):
        params = {"type": "password", "value": secret, "temporary": temporary}
        user = self.find_user(username)
        user_id = user['id']

        credentials = KeycloakCRUD()
        credentials.token = self.token
        credentials.targets = self.targets.addResourcesFor('update', [user_id, 'reset-password'])
        transaction = credentials.update('', params)
        return transaction
