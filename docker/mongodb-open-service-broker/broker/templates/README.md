MongoDB Open Service Broker
===

Templates
===

The `templates` directory is where the service providers for the broker manage
the various templates used in deploying instances of that service's service.

The format of the directory is fixed, this convention maps each template
directly to a particular service provider id's plan id's. That is,

```
./templates/kubernetes/standalone-small-persistent
```

From this path alone we know, 

service_provider.id = 'kubernetes'
service_provider.plans[].id = 'standalone-small-persistent'

If you want to build a service provider, claim your provider id by creating a
folder in the `templates` directory.

### Template Format

For templating we're using [Jinja](http://jinja.pocoo.org/). So,
---
apiVersion: v1
kind: Service
metadata:
  name: {{ instance_name }}
spec:
  type: NodePort
  selector:
    app: {
