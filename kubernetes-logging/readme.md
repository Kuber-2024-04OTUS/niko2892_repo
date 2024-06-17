Настройка облака:

прометка нод:

kubectl label node cl10frpg08u0dopu25k8-umiq node-role.kubernetes.io/infra=infra
node/cl10frpg08u0dopu25k8-umiq labeled
kubectl label node cl16h3gr8lkeibjoqr56-elaq node-role.kubernetes.io/worker=worker
node/cl16h3gr8lkeibjoqr56-elaq labeled

тейнт инфра ноды:
kubectl taint nodes cl1ntcu8cm3ajf2prmct-ymuh infra=true:NoSchedule


конфигурация нод:

kubectl get node -o wide --show-labels:
NAME                        STATUS   ROLES    AGE   VERSION   INTERNAL-IP   EXTERNAL-IP       OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME     LABELS
cl10frpg08u0dopu25k8-umiq   Ready    infra    11m   v1.29.1   10.131.0.27   158.160.161.254   Ubuntu 20.04.6 LTS   5.4.0-174-generic   containerd://1.6.28   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=standard-v3,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/zone=ru-central1-d,kubernetes.io/arch=amd64,kubernetes.io/hostname=cl10frpg08u0dopu25k8-umiq,kubernetes.io/os=linux,node-role.kubernetes.io/infra=infra,node.kubernetes.io/instance-type=standard-v3,node.kubernetes.io/kube-proxy-ds-ready=true,node.kubernetes.io/masq-agent-ds-ready=true,node.kubernetes.io/node-problem-detector-ds-ready=true,topology.kubernetes.io/zone=ru-central1-d,yandex.cloud/node-group-id=cat430ecjs9hkmvu5jg7,yandex.cloud/pci-topology=k8s,yandex.cloud/preemptible=false

cl16h3gr8lkeibjoqr56-elaq   Ready    worker   10m   v1.29.1   10.131.0.16   158.160.171.204   Ubuntu 20.04.6 LTS   5.4.0-174-generic   containerd://1.6.28   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=standard-v3,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/zone=ru-central1-d,k8slens-edit-resource-version=v1,kubernetes.io/arch=amd64,kubernetes.io/hostname=cl16h3gr8lkeibjoqr56-elaq,kubernetes.io/os=linux,node-role.kubernetes.io/worker=worker,node.kubernetes.io/instance-type=standard-v3,node.kubernetes.io/kube-proxy-ds-ready=true,node.kubernetes.io/masq-agent-ds-ready=true,node.kubernetes.io/node-problem-detector-ds-ready=true,topology.kubernetes.io/zone=ru-central1-d,yandex.cloud/node-group-id=catp5eficdulcrs2qrpv,yandex.cloud/pci-topology=k8s,yandex.cloud/preemptible=false

kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints

NAME                        TAINTS
cl10frpg08u0dopu25k8-umiq   [map[effect:NoSchedule key:infra value:true]]
cl16h3gr8lkeibjoqr56-elaq   <none>


подготовка к установке loki:

1) создан сервисный аккаунт storage-loader
2) создан статический ключ доступа для СА: yc iam access-key create --service-account-name=storage-loader
3) создан бакет niko2892-loki-logs
4) проставлены nodeSelector и tolerations в values чарта
5) в секреты добавлены креды для подключения к s3: kubectl create secret generic loki-s3-credentials --from-literal=accessKeyId=<key> --from-literal=secretAccessKey=<secret> -n loki
 
_____________________________________________________________________________________________________________________________________________________________________________________

1) установка loki:

helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm upgrade --install --values .\loki\values.yaml loki --namespace=loki grafana/loki

2) установка promtail:

helm upgrade --install -n loki --values .\promtail\values.yaml promtail grafana/promtail

3) установка grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install --values .\grafana\values.yaml --namespace prometheus --create-namespace prometheus prometheus-community/kube-prometheus-stack