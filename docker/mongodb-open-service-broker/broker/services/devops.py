import os
import re
import abc
from typing import List
from pprint import pprint
import glob 
import urllib
from .service import OSBMDBService
from .kubehelper import KubeHelper
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
    ServiceBroker,
    DeprovisionServiceSpec,
    DeprovisionDetails)
from kubernetes import client, config, utils
import yaml


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

  def __init__(self, logger, broker):
    super().__init__(logger,broker)
    self.my_services = {}
    self.provider_id = "devops"

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
    self.my_services[instance_id] = []
    for output in outputs.keys():
      self.logger.info("Provisioning: %s" % output) 
      KubeHelper.create_from_yaml( outputs[output]['rendered_template'], True) 
      self.my_services[instance_id].append( outputs[output]['rendered_template'] )
    # == 'hello-mongodb-kubernetes-operator':
    #  self.logger.info("provision hello-mongodb-kubernetes-operator start")
    spec = ProvisionedServiceSpec(
           dashboard_url='http://ops-manager/sdfsf',
           operation='some info here'
    )
    return spec


  def deprovision(self, instance_id: str, service_details: DeprovisionDetails, async_allowed: bool) -> DeprovisionServiceSpec:
    print("---> deprovision")
    specs = self.my_services[instance_id]
    try:
      for output in specs:
        self.logger.info("DEprovisioning: %s" % output) 
        KubeHelper.delete_from_yaml( outputs[output]['rendered_template'], True) 
    finally:
      # clean up
      del self.my_services[instance_id]
      return DeprovisionServiceSpec(is_async=True)

