import logging
from flask import Flask
from openbrokerapi import api
from openbrokerapi.catalog import (
    ServicePlan,
)
from openbrokerapi.log_util import basic_config
from openbrokerapi import api
from openbrokerapi.service_broker import (
    ServiceBroker,
    UnbindDetails,
    BindDetails,
    Binding,
    DeprovisionDetails,
    DeprovisionServiceSpec,
    UpdateDetails,
    UpdateServiceSpec,
    ProvisionDetails,
    ProvisionedServiceSpec,
    Service,
    LastOperation)
import os
from services import service, kubernetes, atlas

logger = logging.getLogger(__name__)


class MongoDBKubernetesBroker(ServiceBroker):

    def __init__(self):
 

      self.service_providers = {}
      self.service_providers['kubernetes']=kubernetes.KubernetesService()
      #service_providers['atlas']=atlas.AtlasService()
      self.service_plans = {}

    def catalog(self) -> Service:
      # We should add the ability to inject the service plans
      # this is where cluster admins can create the various t-shirt
      # sizes to support for MongoDB
      
      print("loaded service providers\n".join("{}\t{}".format(k, v) for k, v in self.service_providers.items()))
      plans = []
      tags = ['MongoDB', 'Database' ]
      for provider_name in self.service_providers.keys():
        print("loading plans for provider: %s" % provider_name)
        provider = self.service_providers[provider_name]
        provider_plans = provider.plans()
        for plan in provider_plans:
          self.service_plans[plan.id]=provider_name
        plans.extend( provider_plans )
        tags.extend( provider.tags() )

      catalog = Service(
            id='mongodb-open-service-broker',
            name='mongodb-open-service-broker-service',
            description='This service creates and provides your applications access to MongoDB services.',
            bindable=True,
            plans=plans,
            tags=tags,
            plan_updateable=False,
      )
      return catalog

    def provision(self, instance_id: str, service_details: ProvisionDetails,
                  async_allowed: bool) -> ProvisionedServiceSpec:
        logger.info("provision") 
        # TODO: Lookup provider and call provision() based upon plan selected
        # check that the plan_id exists!
        provider_name = self.service_plans[service_details.plan_id]
        provider = self.service_providers[provider_name]
        logger.info("request to provision plan_id=%s" % service_details.plan_id)
        spec = provider.provision(instance_id, service_details, async_allowed)
        return spec

    def bind(self, instance_id: str, binding_id: str, details: BindDetails) -> Binding:
        logger.info("bind") 

    def update(self, instance_id: str, details: UpdateDetails, async_allowed: bool) -> UpdateServiceSpec:
        logger.info("update") 

    def unbind(self, instance_id: str, binding_id: str, details: UnbindDetails):
        logger.info("deprounbind") 

    def deprovision(self, instance_id: str, details: DeprovisionDetails, async_allowed: bool) -> DeprovisionServiceSpec:
        logger.info("deprovision") 

    def last_operation(self, instance_id: str, operation_data: str) -> LastOperation:
        logger.info("last_opertation") 

def create_broker_blueprint(credentials: api.BrokerCredentials):
    logger.info("create_broker_blueprint: credentials: %s %s" % (credentials.username, credentials.password))
    return api.get_blueprint(MongoDBKubernetesBroker(), credentials, logger)

app = Flask(__name__)
logger = basic_config()  # Use root logger with a basic configuration provided by openbrokerapi.log_utils

# If we're running inside a kubernetes cluster, then we expect the credentials for
# the broker to be in a file mounted from a secret.
if os.environ.get('KUBERNETES_SERVICE_HOST'):
  k8s_host = os.environ.get('KUBERNETES_SERVICE_HOST')
  print("Detected running in a Kubernetes cluster. KUBERNETES_SERVICE_HOST=%s" % k8s_host)
  config_path = "/broker/broker-config"
  with open( ("%s/username" % config_path), 'r') as secret:
    username = secret.read()
  with open( ("%s/password" % config_path), 'r') as secret:
    password = secret.read()
else:
  print("Did not detect Kubernetes cluster. Running with default 'test/test' credentials")
  username = "test"
  password = "test"
openbroker_bp = api.get_blueprint(MongoDBKubernetesBroker(), api.BrokerCredentials(username,password), logger)
app.register_blueprint(openbroker_bp)
app.run("0.0.0.0")
