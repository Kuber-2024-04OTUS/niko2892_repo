Настройка облака:

прометка нод:

kubectl label node cl1ntcu8cm3ajf2prmct-ymuh node-role.kubernetes.io/infra=infra
kubectl label node cl192aosbo9td097qlb5-unur node-role.kubernetes.io/worker=worker
kubectl label nodes cl192aosbo9td097qlb5-unur homework=true (чтобы запустился nginx из ДЗ kubernetes-networks)

тейнт инфра ноды:
kubectl taint nodes cl1ntcu8cm3ajf2prmct-ymuh infra=true:NoSchedule


конфигурация нод:

kubectl get node -o wide --show-labels:
NAME                        STATUS   ROLES    AGE   VERSION   INTERNAL-IP   EXTERNAL-IP       OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME     LABELS
cl192aosbo9td097qlb5-unur   Ready    worker   13d   v1.29.1   10.131.0.24   158.160.176.204   Ubuntu 20.04.6 LTS   5.4.0-174-generic   containerd://1.6.28   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=standard-v3,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/zone=ru-central1-d,homework=true,kubernetes.io/arch=amd64,kubernetes.io/hostname=cl192aosbo9td097qlb5-unur,kubernetes.io/os=linux,node-role.kubernetes.io/worker=worker,node.kubernetes.io/instance-type=standard-v3,node.kubernetes.io/kube-proxy-ds-ready=true,node.kubernetes.io/masq-agent-ds-ready=true,node.kubernetes.io/node-problem-detector-ds-ready=true,topology.kubernetes.io/zone=ru-central1-d,yandex.cloud/node-group-id=catq0nictuoj9421sthn,yandex.cloud/pci-topology=k8s,yandex.cloud/preemptible=false

cl1ntcu8cm3ajf2prmct-ymuh   Ready    infra    13d   v1.29.1   10.131.0.20   158.160.175.174   Ubuntu 20.04.6 LTS   5.4.0-174-generic   containerd://1.6.28   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=standard-v3,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/zone=ru-central1-d,kubernetes.io/arch=amd64,kubernetes.io/hostname=cl1ntcu8cm3ajf2prmct-ymuh,kubernetes.io/os=linux,node-role.kubernetes.io/infra=infra,node.kubernetes.io/instance-type=standard-v3,node.kubernetes.io/kube-proxy-ds-ready=true,node.kubernetes.io/masq-agent-ds-ready=true,node.kubernetes.io/node-problem-detector-ds-ready=true,topology.kubernetes.io/zone=ru-central1-d,yandex.cloud/node-group-id=cat7o52ct59qpauri835,yandex.cloud/pci-topology=k8s,yandex.cloud/preemptible=false

kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints

NAME                        TAINTS
cl192aosbo9td097qlb5-unur   <none>
cl1ntcu8cm3ajf2prmct-ymuh   [map[effect:NoSchedule key:infra value:true]]



Далее все команды выполняются из директории kubernetes-gitops

Установка ArgoCD:
- helm pull oci://cr.yandex/yc-marketplace/yandex-cloud/argo/chart/argo-cd --version 5.46.8-6
- распаковать чарт
- установить toleration и nodeselector для выбора infra нод в values.yaml (в словаре global)
- helm install --namespace argocd --create-namespace argo-cd ./argo-cd/


Создание проекта Otus:
kubectl apply -n argocd -f .\otus.yaml


Создание приложения из ДЗ kubernetes-networks:
kubectl apply -f .\kubernetes-networks.yaml

Создание приложения из ДЗ kubernetes-templating:
kubectl apply -f .\kubernetes-templating.yaml