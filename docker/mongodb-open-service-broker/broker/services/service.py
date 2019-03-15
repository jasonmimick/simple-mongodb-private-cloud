import abc
from typing import List
import glob 
import urllib
from jinja2 import Template
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

#from broker import HTTPException

# interface for services
class OSBMDBService(object, metaclass=abc.ABCMeta):
  
  def __init__(self, logger,broker):
    self.logger = logger
    self.broker = broker

  def load_templates(self,plan_id):
    # Load all templates in repo
    template_dir = "/broker/templates/{0}/{1}/".format(self.provider_id,plan_id)
    self.logger.info("load_templates template_dir=%s" % template_dir)
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


  def has_plan(self,plan_id) -> bool:
    return [p for p in self.myplans if p.id == plan_id]


  @abc.abstractmethod
  def plans(self) -> List[ServicePlan]:
    pass  

  @abc.abstractmethod
  def tags(self) -> List[str]:
    pass  

  @abc.abstractmethod
  def provision(self, instance_id: str, service_details: ProvisionDetails, async_allowed: bool) -> ProvisionedServiceSpec:
    pass

