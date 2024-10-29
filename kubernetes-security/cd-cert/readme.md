на основе кубконфига kubectl config view > ../cd-kubeconfig создаю конфиг для SA "cd":

openssl genpkey -out cd.key -algorithm ed25519 - создание приватного ключа для ServiceAccount "cd"
openssl req -new -key cd.key -out cd.csr -subj '/CN=cd/O=edit' - создание запроса на получение сертификата
cat cd.csr | base64 > cd-64.csr форматироване запроса в base64
заполняю запрос на сертификат по инструкции https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/
kubectl apply -f certificateRequest.yaml   - выполняю запрос на сертификат 
kubectl get csr    - смотрю, какие есть запросы на сертификаты
kubectl certificate approve cd   - подтверждаю сертификат "cd"
kubectl get csr/cd -o jsonpath='{.status.certificate}' | base64 -d > certificate   - получаю сертификат
kubectl config --kubeconfig ../cd-kubeconfig set-credentials cd --client-key=cd.key --client-certificate=certificate --embed-certs=true  - добавляю креды в конфиг
kubectl config --kubeconfig ../cd-kubeconfig set-context cd --user=cd --cluster=minikube   - переключаю контекст и пользователя на "cd"
kubectl --kubeconfig=../cd-kubeconfig config get-contexts смотрю какие есть контексты в конфиге и какой выбран

CURRENT   NAME   CLUSTER    AUTHINFO   NAMESPACE
*         cd     minikube   cd         homework