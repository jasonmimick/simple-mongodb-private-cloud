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

logger = logging.getLogger(__name__)


class MongoDBKubernetesBroker(ServiceBroker):

    def __init__(self):
        pass

    def catalog(self) -> Service:
      # We should add the ability to inject the service plans
      # this is where cluster admins can create the various t-shirt
      # sizes to support for MongoDB
      return Service(
            id='mongodb-kubernetes-broker',
            name='mongodb-kubernetes-broker-service',
            description='This service provides your applications access to MongoDB services.',
            bindable=True,
            plans=[
                ServicePlan(
                    id='standalone-small',
                    name='standalone-small',
                    description='example service plan',
                ),
                ServicePlan(
                    id='replicaset-small',
                    name='replicaset-small',
                    description='example service plan',
                ),
                ServicePlan(
                    id='atlas-replicaset-small',
                    name='atlas-replicaset-small',
                    description='example service plan',
                )
                    
            ],
            tags=['MongoDB', 'Database', 'JSON'],
            plan_updateable=False,
        )

    def provision(self, instance_id: str, service_details: ProvisionDetails,
                  async_allowed: bool) -> ProvisionedServiceSpec:
        logger.info("provision") 
        spec = ProvisionedServiceSpec(
           dashboard_url='http://ops-manager/sdfsf',
           operation='some info here'
        )
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
openbroker_bp = api.get_blueprint(MongoDBKubernetesBroker(), api.BrokerCredentials("test", "test"), logger)
app.register_blueprint(openbroker_bp)
app.run("0.0.0.0")
