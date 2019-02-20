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

class KubernetesService(OSBMDBService):

  def plans(self) -> List[ServicePlan]:
    plans=[
      ServicePlan(
          id='standalone-small-persistent',
          name='standalone-small',
          description='example service plan',
      ),
      ServicePlan(
          id='standalone-small-inmemory',
          name='standalone-small',
          description='example service plan',
      ),
      ServicePlan(
          id='replicaset-small',
          name='replicaset-small',
          description='example service plan',
      ),
      ServicePlan(
          id='shardedcluster-small',
          name='atlas-replicaset-small',
          description='example service plan',
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
