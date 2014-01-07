from heatclient import client as heat_client
from keystoneclient.v2_0 import client as ksclient

class heatclient(object):
    def __init__(self, **kwargs):
        self.dict = {}
      	self.dict['api_version'] = kwargs.get('version',"1")
      	self.dict['username'] = kwargs.get('username','admin')
      	self.dict['password'] = kwargs.get('password','buptnic')
      	self.dict['tenant_id'] = kwargs.get('tenant_id',None)
      	self.dict['tenant_name'] = kwargs.get('tenant_name','admin')
      	self.dict['token'] = kwargs.get('token',None)
      	self.dict['auth_url'] = kwargs.get('auth_url',r'http://210.25.137.232:5000/v2.0')
      	self._create_client()

    def _get_ksclient(self):
	      """Get an endpoint and auth token from Keystone.

        :param username: name of user
        :param password: user's password
        :param tenant_id: unique identifier of tenant
        :param tenant_name: name of tenant
        :param auth_url: endpoint to authenticate against
        :param token: token to use instead of username/password
        """
	      kc_args = {}
        kc_args['auth_url'] = self.dict.get('auth_url')
        if self.dict.get('tenant_id'):
            kc_args['tenant_id'] = self.dict.get('tenant_id')
        else:
            kc_args['tenant_name'] = self.dict.get('tenant_name')

        if self.dict.get('token'):
            kc_args['token'] = self.dict.get('token')
        else:
            kc_args['username'] = self.dict.get('username')
            kc_args['password'] = self.dict.get('password')

        return ksclient.Client(**kc_args)

    def _get_endpoint(self, client):
        """Get an endpoint using the provided keystone client."""
        return client.service_catalog.url_for(service_type='orchestration',
        									                    endpoint_type='publicURL')    

    def _create_client(self):
        ks_client = self._get_ksclient()
    	  token = self.dict['token'] if self.dict['token'] else ks_client.auth_token
        kwargs = {
            'token': token,
            'username': self.dict.get('username'),
            'password': self.dict.get('password')
        }
        endpoint = self._get_endpoint(ks_client)
        self.client = heat_client.Client(self.dict.get('api_version'), endpoint, **kwargs)

    def stacks_list(self):
    	  return [stack for stack in self.client.stacks.list()]


    def stack_delete(self, stack_id):
    	  return self.client.stacks.delete(stack_id)

    
    def stack_get(self, stack_id):
    	  return self.client.stacks.get(stack_id)


    def stack_create(self, **kwargs):
    	  return self.client.stacks.create(**kwargs)


    def events_list(self, stack_name):
        return self.client.events.list(stack_name)


    def resources_list(self, stack_name):
        return self.client.resources.list(stack_name)


    def resource_get(self, stack_id, resource_name):
        return self.client.resources.get(stack_id, resource_name)


    def resource_metadata_get(self, stack_id, resource_name):
        return self.client.resources.metadata(stack_id, resource_name)


    def template_validate(self, **kwargs):
        return self.client.stacks.validate(**kwargs)    
		
if __name__ == '__main__':
    stacks = None
    client=heatclient()
    stacks = client.stacks_list()
    if stacks:
	      print stacks
        print "Success lee!"
    else:
	      print "Work more!"
