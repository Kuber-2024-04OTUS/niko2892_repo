1) Для выполнения данного задания вам потребуется создать минимум 4 виртуальных машины в YC следующей конфигурации: Для master - 1 узел, 2vCPU, 8GB RAM, для worker – 3 узла, 2vCPU, 8GB RAM
создал ВМ в Яндекс.Облаке: master, worker-1, worker-2, worker-3

2) Выполните подготовительные работы на узлах:
- отключение swap:  sudo swapoff -a && sudo sed -i "s%/swap.img%#/swap.img%g" /etc/fstab
- установка overlay и br_netfilter: 
    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
    EOF

    sudo modprobe overlay
    sudo modprobe br_netfilter
- установка параметров kubernetes:
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward = 1
    EOF

    sudo sysctl --system

- Добавление GPG ключа docker:
    sudo apt-get update
    sudo apt-get install apt-transport-https ca-certificates curl gpg -y
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

- подключение докер репозитория
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update

3) Установите containerd, kubeadm, kubelet, kubectl на все ВМ
    sudo apt-get install -y apt-transport-https ca-certificates curl gpg containerd.io
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install kubelet kubeadm kubectl -y
    sudo apt-mark hold kubelet kubeadm kubectl
    sudo systemctl enable --now kubelet

- настройка containerd:
    sudo sh -c "containerd config default > /etc/containerd/config.toml"
    sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
    sudo systemctl restart containerd.service
    sudo systemctl enable containerd.service

4) Выполните kubeadm init на мастер-ноде
    sudo kubeadm init --pod-network-cidr=10.244.0.0/16
    Your Kubernetes control-plane has initialized successfully!

    To start using your cluster, you need to run the following as a regular user:

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    Alternatively, if you are the root user, you can run:

    export KUBECONFIG=/etc/kubernetes/admin.conf

    You should now deploy a pod network to the cluster.
    Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
    https://kubernetes.io/docs/concepts/cluster-administration/addons/

    Then you can join any number of worker nodes by running the following on each as root:

    kubeadm join 172.16.0.6:6443 --token us7rgz.rffqtf56adxgxyz7 --discovery-token-ca-cert-hash sha256:57108e1088c580d19a12c8f0c4b7ed92c9b1bee6b681b3d52722a3f7b3710654

5) установка сетевого плагина flannel: kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
Результат:
niko2892@master:~$ kubectl get po -A
NAMESPACE      NAME                             READY   STATUS    RESTARTS   AGE
kube-flannel   kube-flannel-ds-s7wr7            1/1     Running   0          38s
kube-system    coredns-76f75df574-p7chs         1/1     Running   0          6m56s
kube-system    coredns-76f75df574-sj8hv         1/1     Running   0          6m56s
kube-system    etcd-master                      1/1     Running   0          7m8s
kube-system    kube-apiserver-master            1/1     Running   0          7m8s
kube-system    kube-controller-manager-master   1/1     Running   0          7m12s
kube-system    kube-proxy-6dlfp                 1/1     Running   0          6m56s
kube-system    kube-scheduler-master            1/1     Running   0          7m8s

6) Выполните kubeadm join на воркер нодах:

niko2892@master:~$ kubectl get nodes -o wide
NAME       STATUS   ROLES           AGE    VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
master     Ready    control-plane   34m    v1.29.9   172.16.0.6    <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-1   Ready    <none>          3m6s   v1.29.9   172.16.0.24   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-2   Ready    <none>          60s    v1.29.9   172.16.0.15   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-3   Ready    <none>          51s    v1.29.9   172.16.0.37   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22

7) Обновление kubernetes на мастере:
- добавляю репозиторий с новой версией:
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update

- снимаю с холда пакеты kubeadm kubelet kubectl
    sudo apt-mark unhold kubeadm kubelet kubectl

- обновление kubeadm, kubelet, kubectl:
    sudo apt-get install -y kubeadm=1.30.3-1.1
    sudo apt-get install -y kubelet=1.30.3-1.1  kubectl=1.30.3-1.1
    
- ставлю обратно на холд пакеты:
    sudo apt-mark hold kubelet kubeadm kubectl

- результат:
kubectl get nodes -o wide
NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
master     Ready    control-plane   44m   v1.30.3   172.16.0.6    <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-1   Ready    <none>          13m   v1.29.9   172.16.0.24   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-2   Ready    <none>          11m   v1.29.9   172.16.0.15   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-3   Ready    <none>          11m   v1.29.9   172.16.0.37   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22

8) обновление kubernetes на воркерах:
то же самое, что и с мастером, но перед работой на ноде надо выполнить kubectl drain, а после завершения обновления kubectl uncordon
результат обновления:
niko2892@master:~$ kubectl get nodes -o wide
NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
master     Ready    control-plane   56m   v1.30.3   172.16.0.6    <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-1   Ready    <none>          24m   v1.30.3   172.16.0.24   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-2   Ready    <none>          22m   v1.30.3   172.16.0.15   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22
worker-3   Ready    <none>          22m   v1.30.3   172.16.0.37   <none>        Ubuntu 24.04.1 LTS   6.8.0-41-generic   containerd://1.7.22

9) Задание со *
создал ВМ в Яндекс.Облаке: master-1, master-2, master-3, worker-1, worker-2
на своем лкальном компе выполняю:
git clone https://github.com/kubernetes-sigs/kubespray.git
cd kubespray
cp -rfp inventory/sample inventory/k8s
declare -a IPS=(89.169.150.75 89.169.154.241 89.169.152.185 89.169.150.109 89.169.158.57)
генерирую инвентарник: CONFIG_FILE=inventory/k8s/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

в inventory/k8s/group_vars/k8s_cluster/addons.yml меняю 
ingress_nginx_enabled: true
ingress_nginx_host_network: true
helm_enabled: true

в ansible.cfg добавляю remote_user=root

устанавливаю кластер: ansible-playbook -i inventory/k8s/hosts.yaml cluster.yml

* делал все по инсрукции https://habr.com/ru/companies/domclick/articles/682364/
при выполнении ansible скрипта вызникает ошибка No module named 'ansible.module_utils.six.moves' , с ней разобраться так и не смог,
на самом деле модуль на серверах есть. Почему при выплонении скрипта он не находится не нашел причину.