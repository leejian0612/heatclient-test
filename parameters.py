para_dict={
"stack_name": "test-v6",
"disable_rollback": True,
"parameters": {"private_net_cidr": "2001:da8:25d:8088::/64",
               "key_name": "heat_key",
               "image": "Fedora16-x86_64-openstack-sda",
               "private_net_gateway": "2001:da8:25d:8088::1",
               "public_net_id": "d6258cbe-2638-474b-afa7-78ede6d19e29",
               "private_net_name": "net_v6",
               "flavor": "m1.small"},
"template":""" 

heat_template_version: 2013-05-23

description: >
  HOT template to create a new neutron network plus a router to the public
  network, and for deploying two servers into the new network. The template also
  assigns floating IP addresses to each server so they are routable from the
  public network.

parameters:
  key_name:
    type: string
    description: Name of keypair to assign to servers
  image:
    type: string
    description: Name of image to use for servers
  flavor:
    type: string
    description: Flavor to use for servers
  public_net_id:
    type: string
    description: >
      ID of public network for which floating IP addresses will be allocated
  private_net_name:
    type: string
    description: Name of private network to be created
  private_net_cidr:
    type: string
    description: Private network address (CIDR notation)
  private_net_gateway:
    type: string
    description: Private network gateway address
 
resources:
  private_net:
    type: OS::Neutron::Net
    properties:
      name: { get_param: private_net_name }

  private_subnet:
    type: OS::Neutron::Subnet
    properties:
      ip_version: 6
      network_id: { get_resource: private_net }
      cidr: { get_param: private_net_cidr }
      gateway_ip: { get_param: private_net_gateway }
      
  router:
    type: OS::Neutron::Router

  router_gateway:
    type: OS::Neutron::RouterGateway
    properties:
      router_id: { get_resource: router }
      network_id: { get_param: public_net_id }

  router_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: router }
      subnet_id: { get_resource: private_subnet }

  server1:
    type: OS::Nova::Server
    properties:
      name: Server1
      image: { get_param: image }
      flavor: { get_param: flavor }
      key_name: { get_param: key_name }
      networks:
        - port: { get_resource: server1_port }

  server1_port:
    type: OS::Neutron::Port
    properties:
      network_id: { get_resource: private_net }

  server2:
    type: OS::Nova::Server
    properties:
      name: Server2
      image: { get_param: image }
      flavor: { get_param: flavor }
      key_name: { get_param: key_name }
      networks:
        - port: { get_resource: server2_port }

  server2_port:
    type: OS::Neutron::Port
    properties:
      network_id: { get_resource: private_net }

outputs:
  server1_private_ip:
    description: IP address of server1 in private network
    value: { get_attr: [ server1, accessIPv6 ] }
  
  server2_private_ip:
    description: IP address of server2 in private network
    value: { get_attr: [ server2, accessIPv6 ] }  
""",
"timeout_mins": 60
}
