import abc
from typing import List
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
    return plans
                    
            
  def tags(self) -> List[str]:
    return [ "MongoDB Kubernetes Operator", "k8s", "containers", "docker" ] 


  def provision(self, instance_id: str, service_details: ProvisionDetails, async_allowed: bool) -> ProvisionedServiceSpec:
    print("kubernetes provider - provision called") 
    spec = ProvisionedServiceSpec(
           dashboard_url='http://ops-manager/sdfsf',
           operation='some info here'
    )
    return spec
