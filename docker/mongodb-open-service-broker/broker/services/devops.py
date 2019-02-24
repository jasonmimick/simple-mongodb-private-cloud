import os
import re
import abc
from typing import List
from pprint import pprint
import glob 
import urllib
from .service import OSBMDBService
from openbrokerapi.catalog import (
    ServicePlan,
)
from openbrokerapi.service_broker import (
    BindDetails,
    BindState,
    ProvisionedServiceSpec,
    UpdateServiceSpec,
    Binding,
    DeprovisionDetails,
    ProvisionDetails,
    ProvisionState,
    UnbindDetails,
    UpdateDetails,
    ServiceBroker)
from jinja2 import Template
from kubernetes import client, config, utils
import yaml

class KubeHelper():

  @staticmethod
  def get_ns_kind_name(yaml_filepath_or_contents,verbose=False):
    y = yaml.load(yaml_filepath_or_contents)
    # TODO: add error handling to make sure keys exist
    x = { 'kind' : y['kind'], 'name' : y['name'] }
    if "namespace" in yml_object["metadata"]:
      x['namespace'] = y["metadata"]["namespace"]
    else:
      x['namespace'] = "default"
    return x

  @staticmethod
  def get_documents(yaml_filepath_or_contents, verbose=False):
    if verbose:
      print("get_documents yaml_filepath_or_contents=%s" % yaml_filepath_or_contents)
    docs = []
    if os.path.isfile(yaml_filepath_or_contents):
      if verbose:
        print("os.path.isfile was True")
      with open(yaml_filepath_or_contents, 'r') as stream:
        for doc in yaml.load_all(stream):
          if doc is None:
            print("get_documents: doc was None!")
            continue
          if verbose:
            print("get_documents loaded: %s" % doc)
          docs.append(doc)
    else:
      for doc in yaml.load_all(yaml_filepath_or_contents):
        if doc is None:
          print("get_documents: doc was None!")
          continue
        if verbose:
          print("get_documents loaded: %s" % doc)
        docs.append(doc)
    return docs 

  @staticmethod
  def read_many_ns_object(k8s_client, yaml_filepath_or_contents, verbose=False):
    responses = []
    yamls = KubeHelper.get_documents(yaml_filepath_or_contents, verbose)
    for y in yamls:
      responses.append( KubeHelper.read_ns_object(y,verbose) ) 
    return responses

  @staticmethod
  def read_ns_object(k8s_client, yaml_filepath_or_contents, verbose=False):
    print("read_ns_object>>>> %s" % yaml_filepath_or_contents)
    yml_object = yaml.load(yaml_filepath_or_contents)
    # TODO: case of yaml file containing multiple objects
    group, _, version = yml_object["apiVersion"].partition("/")
    if version == "":
      version = group
      group = "core"
    # Take care for the case e.g. api_type is "apiextensions.k8s.io"
    # Only replace the last instance
    group = "".join(group.rsplit(".k8s.io", 1))
    fcn_to_call = "{0}{1}Api".format(group.capitalize(), version.capitalize())
    k8s_api = getattr(client, fcn_to_call)(k8s_client)
    # Replace CamelCased action_type into snake_case
    kind = yml_object["kind"]
    kind = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', kind)
    kind = re.sub('([a-z0-9])([A-Z])', r'\1_\2', kind).lower()
    # Decide which namespace we are going to put the object in,
    # if any
    if hasattr(k8s_api, "read_namespaced_{0}".format(oi['kind'])):
      resp = getattr(k8s_api, "read_namespaced_{0}".format(io['kind']))(body=yml_object, namespace=namespace, **kwargs)
    else:
      resp = getattr(k8s_api, "read_{0}".format(kind))(body=yml_object, **kwargs)
    if verbose:
      print("{0} read. status='{1}'".format(kind, str(resp.status)))
      print("resp: %s" % resp)
    return resp

  @staticmethod
  def utils_create_from_yaml(k8s_client, yaml_file, verbose=False, **kwargs):
    yml_object = yaml.load(yaml.dump(yaml_file))
    # TODO: case of yaml file containing multiple objects
    group, _, version = yml_object["apiVersion"].partition("/")
    if version == "":
      version = group
      group = "core"
    # Take care for the case e.g. api_type is "apiextensions.k8s.io"
    # Only replace the last instance
    print("-1 --> group: %s" % group)
    group = "".join(group.rsplit(".k8s.io", 1))
    print("0 --> group: %s" % group)
    if len(group.split('.'))>1:
      if verbose:
        print("Found API group with multiple dots")
      g2 = ""
      g3 = group.split('.')
      print("g3=%s" % g3)
      for xx in g3:
        print("-----> xx=%s" % xx)
        g2+=xx.capitalize()
      print("g2=%s" % g2)
      fcn_to_call = "{0}{1}Api".format(g2, version.capitalize())
    else:
      fcn_to_call = "{0}{1}Api".format(group.capitalize(),version.capitalize())
    if verbose:
      print("fcn_to_call=%s" % fcn_to_call)
    k8s_api = getattr(client, fcn_to_call)(k8s_client)
    # Replace CamelCased action_type into snake_case
    kind = yml_object["kind"]
    print("1 --> kind: %s" % kind)
    kind = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', kind)
    print("2 --> kind: %s" % kind)
    kind = re.sub('([a-z0-9])([A-Z])', r'\1_\2', kind).lower()
    print("3 --> kind: %s" % kind)
    # Decide which namespace we are going to put the object in,
    # if any
    if "namespace" in yml_object["metadata"]:
      namespace = yml_object["metadata"]["namespace"]
    else:
      namespace = "default"
    # Expect the user to create namespaced objects more often
    if hasattr(k8s_api, "create_namespaced_{0}".format(kind)):
      resp = getattr(k8s_api, "create_namespaced_{0}".format(kind))(body=yml_object, namespace=namespace, **kwargs)
    else:
      resp = getattr(k8s_api, "create_{0}".format(kind))(body=yml_object, **kwargs)
    if verbose:
      print("{0} created. resp={1}".format(kind, resp))
    return k8s_api

  @staticmethod
  def create_from_many_yaml(k8s_client, yaml_file, verbose=False):
    responses = []
    yamls = KubeHelper.get_documents(yaml_file, verbose)
    for y in yamls:
      if verbose:
        print("create_from_many_yaml y=%s" % y)
      responses.append( KubeHelper.utils_create_from_yaml(k8s_client, y,verbose) ) 
    return responses

  @staticmethod
  def create_from_yaml(yaml_file, verbose=False):
    if not os.getenv('KUBERNETES_SERVICE_HOST'): 
      if verbose:
        print("create_from_yaml: - KUBERNETES_SERVICE_HOST not set!")
      return
    config.load_incluster_config()
    #with open('/var/run/secrets/kubernetes.io/serviceaccount/token','r') as t:
    #  api_token = t.read()
    #3configuration = client.Configuration()
    #url = "https://{0}:{1}".format(os.getenv('KUBERNETES_SERVICE_HOST'), os.getenv('KUBERNETES_SERVICE_PORT'))
    #configuration.host = url
    #configuration.verify_ssl = False
    #with open('/var/run/secrets/kubernetes.io/serviceaccount/ca.crt','r') as cert:
    #  configuration.ssl_ca_cert = cert.read()
    #configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    #configuration.debug = True
    #configuration.api_key = {"authorization": "Bearer " + api_token}
    #configuration.assert_hostname = True
    #configuration.verify_ssl = False
    #client.Configuration.set_default(configuration)
    #info = KubeHelper.get_ns_kind_name(yaml_file)
    k8s_client = client.ApiClient()
    reponses = KubeHelper.create_from_many_yaml(k8s_client, yaml_file, verbose)
    print("responses: {0}".format(responses))
    deps = KubeHelper.read_ns_object(k8s_client,yaml_file)
    if verbose:
      print("{0} created".format(deps.metadata.name)) 

class DevOpsService(OSBMDBService):

  def plans(self) -> List[ServicePlan]:
    plans=[
      ServicePlan(
          id='hello-mongodb-ops-manager',
          name='hello-mongodb-ops-manager',
          description='Installs a demonstration version of MongoDB Ops Manager.',
      ),
      ServicePlan(
          id='hello-mongodb-kubernetes-operator',
          name='hello-mongodb-kubernetes-operator',
          description='Installs a demonstration version of the MongoDB Kubernetes Operator',
      )
    ]
    self.myplans = plans[:]
    return plans
                    
            
  def tags(self) -> List[str]:
    return [ "MongoDB Kubernetes Operator", "k8s", "containers", "docker" ] 

  def has_plan(self,plan_id) -> bool:
    return [p for p in self.myplans if p.id == plan_id]

  def load_templates(self,plan_id):
    # Load all templates in repo
    template_dir = "/broker/templates/devops/**"
    template_filename_wildcard = "*.yaml"
    template_files = glob.glob("%s/%s" % (template_dir, template_filename_wildcard))
    templates = {}
    self.logger.info("load_templates: %s" % template_files)
    for template_file in template_files:
      self.logger.info("loading: %s" % template_file)
      with open(template_file, 'r') as t:
        template = t.read()
        self.logger.debug("loaded template: %s" % template)
        templates[template_file] = { 'template' : str(template), 'rendered_template' : None }

    template_filename_wildcard = "*.url"
    template_files = glob.glob("%s/%s" % (template_dir, template_filename_wildcard))
    self.logger.info("load_templates: %s" % template_files)
    for template_file in template_files:
      self.logger.info("loading: %s" % template_file)

      with open(template_file, 'r') as t:
        url = t.read()
        self.logger.info("loading template from url: %s" % url)
        with urllib.request.urlopen(url) as u:
          template = u.read()
          self.logger.debug("loaded template: %s" % template)
          templates[template_file] = { 'template' : str(template), 'rendered_template' : None }
    return templates

  def render_templates(self, templates, parameters):
    rendered_templates = {}
    self.logger.info("render_templates: %s" % templates.keys())
    for template_name in templates.keys():
      
      template = templates[template_name]
      #self.logger.info('template:%s' % template)
      rendered_templates[template_name] = {}
      rendered_templates[template_name]['template'] = template['template']
      #if "{{ " in template['template']:
      t = Template( template['template'] )
      rendered_template = t.render(parameters)
      #else:
      #  self.logger.info("No parameters detected in template.")
      #  rendered_template = template['template']
      rendered_templates[template_name]['rendered_template'] = rendered_template
      self.logger.debug('rendered_template:%s' % template)
    return rendered_templates

  def provision(self, instance_id: str, service_details: ProvisionDetails, async_allowed: bool) -> ProvisionedServiceSpec:
    self.logger.info("devops provider - provision called") 
    self.logger.info("devops provider - instance_id:%s" % instance_id) 
    self.logger.info("devops provider - async_allowed:%s" % async_allowed) 
    self.logger.info("devops provider  - service_details: %s" % vars(service_details))
    if not self.has_plan(service_details.plan_id):
      raise HTTPException('invalid plan_id', status_code=400)      
    
    templates = self.load_templates(service_details.plan_id)    
    # merge parameters from 'context' and 'parameters' to templates
    parameters = { **service_details.parameters, **service_details.context }
    self.logger.info("render parameters: %s" % parameters)
    outputs = self.render_templates(templates,parameters)
    self.logger.debug( outputs )
    for output in outputs.keys():
      self.logger.info("Provisioning: %s" % output) 
      KubeHelper.create_from_yaml( outputs[output]['rendered_template'], True) 
    # == 'hello-mongodb-kubernetes-operator':
    #  self.logger.info("provision hello-mongodb-kubernetes-operator start")
    spec = ProvisionedServiceSpec(
           dashboard_url='http://ops-manager/sdfsf',
           operation='some info here'
    )
    return spec
