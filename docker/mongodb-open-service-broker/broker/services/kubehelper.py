from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import yaml
import os
import re
import abc
from typing import List
from pprint import pprint
import glob 
import urllib
from .service import OSBMDBService

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
    if verbose:
      print("read_many_ns_object yaml_filepath_or_contents=%s" % yaml_filepath_or_contents)
    responses = []
    yamls = KubeHelper.get_documents(yaml_filepath_or_contents, verbose)
    for y in yamls:
      if verbose:
        print("#####  ------>>>>>>> y:%s" % y)
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
    return KubeHelper.make_it_so("create", k8s_client, yaml_file, verbose, **kwargs)

  @staticmethod
  def make_it_so(op,k8s_client, yaml_file, verbose=False, **kwargs):
    ops = [ "create", "delete", "patch" ]
    if not op in ops:
      raise HTTPException("Invalid operation='%s'" % op, status_code=400)      
       
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
    try:
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
      if hasattr(k8s_api, "{0}_namespaced_{1}".format(op,kind)):
        resp = getattr(k8s_api, "{0}_namespaced_{1}".format(op,kind))(body=yml_object, namespace=namespace, **kwargs)
      else:
        resp = getattr(k8s_api, "{0}_{1}".format(op,kind))(body=yml_object, **kwargs)
      if verbose:
        print("{0} {1}. resp={2}".format(kind, op, resp))

    except Exception as error:
      
      print("error: %s" % error)
      # Decide which namespace we are going to put the object in,
      # if any
      if "namespace" in yml_object["metadata"]:
        namespace = yml_object["metadata"]["namespace"]
      else:
        namespace = "mongodb"
      api_instance = client.CustomObjectsApi(client.ApiClient())
      group = 'mongodb.com' # str | The custom resource's group name
      version = 'v1' # str | The custom resource's version
      plural = 'mongodbreplicasets' 
      body = yaml_file # object | The JSON schema of the Resource to create.
      pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)

      try: 
        ns = yml_object['metadata']['namespace']
        #resp = api_instance.create_cluster_custom_object(group, version, plural, body, pretty=pretty)
        resp = api_instance.create_namespaced_custom_object(group, version, ns, plural, body, pretty=pretty)
        if verbose:
          print("resp={0}".format(resp))
      except ApiException as e:
        print("Exception when calling CustomObjectsApi->create_cluster_custom_object: %s\n" % e)
        resp = e
    return resp 

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
    k8s_client = client.ApiClient()
    responses = KubeHelper.create_from_many_yaml(k8s_client, yaml_file, verbose)
    print("responses: %s" % responses)
    if verbose:
      #info = [ { "kind" : r['kind'], "name" : r['metadata']['name'] } for r in responses ]
      #info = [ { "kind" : r.kind, "name" : r.metadata.name } for r in responses ]
      print("create_from_yaml: Created: %s" % responses) 
    return responses


  def delete_from_yaml(yaml_file, verbose=False):
    config.load_incluster_config()
    k8s_client = client.ApiClient()
    responses = KubeHelper.make_it_so("delete",k8s_client, yaml_file, verbose)
    print("responses: %s" % responses)
    if verbose:
      #info = [ { "kind" : r['kind'], "name" : r['metadata']['name'] } for r in responses ]
      info = [ { "kind" : r.kind, "name" : r.metadata.name } for r in responses ]
      print("create_from_yaml: Created: %s" % info) 
    return responses
    

