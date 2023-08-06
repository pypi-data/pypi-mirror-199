from .targets import Targets
from .crud import KeycloakCRUD
import requests, json

# The Keycloak guys decided to use another resource DELETE /roles-by-id, instead of sticking to DELETE /roles.
def RolesURLBuilder(url):
    targets = Targets.makeWithURL(url)
    targets.targets['delete'].replaceResource('roles', 'roles-by-id')
    targets.targets['update'].replaceResource('roles', 'roles-by-id')
    targets.targets['root'].replaceResource('roles', 'roles-by-id')
    return targets


class Role:
    def __init__(self, crud, role_object):
        self.role = role_object
        self.crud = crud

    def add_composite(self, name):
        role_id = self.role['id']
        role_to_add = self.crud.find(name)

        if not role_to_add:
            raise Exception(f'Role {name} not found!')

        url = str(self.crud.root()) + f'/{role_id}/composites'
        ret = requests.post(url, data=json.dumps([role_to_add.role]), headers=self.crud.headers())

        return ret.status_code == 204 or ret.status_code == 304
    def composite(self):
        role_id = self.role['id']
        url = str(self.crud.root()) + f'/{role_id}/composites/realm'
        ret = requests.get(url, headers=self.crud.headers()).json()
        return ret

    def __str__(self):
        return str(self.role)

class Roles(KeycloakCRUD):
    def all(self):
        roles = super().all()
        roles = map(lambda r: Role(self, r), roles)
        return list(roles)

    def find(self, name):
        roles= self.all()
        for r in roles:
            if r.role['name'] == name:
                return r