import kopf
import logging
import os
import yaml
import kubernetes

def create_role(name, namespace):
    #create role https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/RbacAuthorizationV1Api.md#create_namespaced_role
    pvc = os.path.join(os.path.dirname(__file__),'kopf','role.yaml')
    tmpl = open(pvc, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)

    kopf.adopt(data)
    
    api = kubernetes.client.RbacAuthorizationV1Api()
    obj = api.create_namespaced_role(
        namespace=namespace,
        body=data,
    )

    logging.info(f"Role {name} is created!")

    return{'role-name': obj.metadata.name}


def create_cluster_role(name, namespace):
    #create cluster role https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/RbacAuthorizationV1Api.md#create_cluster_role
    cluster_role = os.path.join(os.path.dirname(__file__),'kopf','cluster-role.yaml')
    tmpl = open(cluster_role, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)
    
    try:
        api = kubernetes.client.RbacAuthorizationV1Api()
        obj = api.create_cluster_role(
            body=data,
        )

        logging.info(f"ClusterRole {name} is created!")
        return{'clusterrole-name': obj.metadata.name}
    except Exception as e:
        print(e)
        logging.error(e)

def delete_cluster_role(name, namespace):
    api = kubernetes.client.RbacAuthorizationV1Api()
    
    try:
        obj = api.delete_cluster_role(
            name=name
        )

        logging.info(f"ClusterRole {name} is deleted!")
        return{'cluster-role-deleted': obj.metadata.name}
    except Exception as e:
        print(e)
        logging.error(e)

def create_rb(name, namespace):
    #create rolebinding https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/RbacAuthorizationV1Api.md#create_namespaced_role_binding
    pvc = os.path.join(os.path.dirname(__file__),'kopf','role-binding.yaml')
    tmpl = open(pvc, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)

    kopf.adopt(data)
    
    api = kubernetes.client.RbacAuthorizationV1Api()
    obj = api.create_namespaced_role_binding(
        namespace=namespace,
        body=data,
    )

    logging.info(f"RoleBinding {name} is created!")

    return{'rolebinding-name': obj.metadata.name}


def create_cluster_rb(name, namespace):
    #create cluster rolebinding https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/RbacAuthorizationV1Api.md#create_cluster_role_binding
    pvc = os.path.join(os.path.dirname(__file__),'kopf','cluster-role-binding.yaml')
    tmpl = open(pvc, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)
    
    api = kubernetes.client.RbacAuthorizationV1Api()
    
    try:
        obj = api.create_cluster_role_binding(
            body=data,
        )

        logging.info(f"RoleBinding {name} is created!")
        return{'rolebinding-name': obj.metadata.name}
    except Exception as e:
        print(e)
        logging.error(e)


def delete_cluster_role_binding(name, namespace):
    api = kubernetes.client.RbacAuthorizationV1Api()
    try:
        obj = api.delete_cluster_role_binding(
            name=name
        )

        logging.info(f"ClusterRoleBinding {name} is deleted!")
        return{'cluster-role-binding-deleted': obj.metadata.name}
    except Exception as e:
        print(e)
        logging.error(e)


def create_sa(name, namespace):
    #create service-account https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_service_account
    pvc = os.path.join(os.path.dirname(__file__),'kopf','sa.yaml')
    tmpl = open(pvc, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)

    kopf.adopt(data)
    
    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_service_account(
        namespace=namespace,
        body=data,
    )

    logging.info(f"ServiceAccount {name} is created!")

    return{'servicaaccount-name': obj.metadata.name}


def create_pvc(name, namespace, storage_size):
    #create pvc https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_persistent_volume_claim
    if not storage_size:
        raise kopf.PermanentError(f"Size must be set. Got {storage_size!r}.")
    
    pvc = os.path.join(os.path.dirname(__file__),'kopf','pvc.yaml')
    tmpl = open(pvc, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace, size=storage_size)
    data = yaml.safe_load(text)

    kopf.adopt(data)
    
    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logging.info(f"PVC {name} is created!")

    return{'pvc-name': obj.metadata.name}


def create_svc(name, namespace):
    #create service https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_service
    service = os.path.join(os.path.dirname(__file__),'kopf','service.yaml')
    tmpl = open(service, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace)
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_service(
        namespace=namespace,
        body=data,
    )

    logging.info(f"Service {name} is created!")

    return{'service-name': obj.metadata.name}


def create_deployment(name, namespace, image, password, database, container_port):
    #create deployment
    deployment = os.path.join(os.path.dirname(__file__),'kopf','deployment.yaml')
    tmpl = open(deployment, 'rt').read()
    text = tmpl.format(name=name, namespace=namespace, image=image, password=password, database=database, container_port=int(container_port))
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.AppsV1Api()
    obj = api.create_namespaced_deployment(
        namespace=namespace,
        body=data,
    )

    logging.info(f"Deployment {name} is created")

    return{'deployment-name': obj.metadata.name}


@kopf.on.create('mysqls')
def create_fn(spec, name, namespace, logger, **kwargs):
    image = spec.get('image')
    database = spec.get('database')
    password = spec.get('password')
    storage_size = spec.get('storage_size')
    container_port = spec.get('container_port')

    create_cluster_role(name, namespace)
    create_sa(name, namespace)
    create_cluster_rb(name, namespace)
    create_pvc(name, namespace, storage_size)
    create_svc(name, namespace)
    create_deployment(name, namespace, image, password, database, container_port)


@kopf.on.delete('mysqls')
def delete_fn(name, namespace, **kwargs):
    delete_cluster_role_binding(name, namespace)
    delete_cluster_role(name, namespace)