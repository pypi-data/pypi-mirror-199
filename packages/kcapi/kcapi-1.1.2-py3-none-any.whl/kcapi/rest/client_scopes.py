from .targets import Targets
from .crud import KeycloakCRUD
import requests, json

class CS:
    def __init__(self, crud, val):
        self.value = val
        self.crud = crud
    def all(self):
        _id = self.value['id']
        url = str(self.crud.root()) + f'/{_id}'
        return requests.get(url, headers=self.crud.headers()).json()

    def find(self, name):
        models = self.all()
        for r in models['protocolMappers']:
            if r['name'] == name:
                return r

    def add_simple_mapper(self, name, id_token_claim=True, userinfo_token_claim=True):
        prototype = {
            "protocol": "openid-connect",
            "config": {
                "id.token.claim": id_token_claim,
                "userinfo.token.claim": userinfo_token_claim
            },
            "name": name,
            "protocolMapper": "oidc-claims-param-token-mapper"
        }

        return self.add_mapper(prototype)
    def add_mapper(self, model):
        _id = self.value['id']

        url = str(self.crud.root()) + f'/{_id}/protocol-mappers/models'
        ret = requests.post(url, data=json.dumps(model), headers=self.crud.headers())

        return ret.status_code == 201 or ret.status_code == 304

    def __str__(self):
        return str(self.value)

class ClientScopes(KeycloakCRUD):
    def all(self):
        res = super().all()
        resources = map(lambda r: CS(self, r), res)
        return list(resources)

    def find(self, name):
        roles = self.all()
        for r in roles:
            if r.value['name'] == name:
                return r