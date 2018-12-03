#!/bin/bash
oc login -u system:admin
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-group anyuid system:authenticated
oc adm policy add-cluster-role-to-user cluster-admin developer
oc adm policy add-cluster-role-to-user cluster-admin admin

