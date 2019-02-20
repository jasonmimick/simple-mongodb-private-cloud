import abc
from typing import List
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

from openbrokerapi.catalog import (
    ServicePlan,
)

# interface for services
class OSBMDBService(object, metaclass=abc.ABCMeta):
  
  @abc.abstractmethod
  def plans(self) -> List[ServicePlan]:
    pass  

  @abc.abstractmethod
  def tags(self) -> List[str]:
    pass  

  @abc.abstractmethod
  def provision(self, instance_id: str, service_details: ProvisionDetails, async_allowed: bool) -> ProvisionedServiceSpec:
    pass

