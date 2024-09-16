1) Установка Consul
клонировать репозиторий с чартом консула ```git clone https://github.com/hashicorp/consul-k8s.git```
```
установить консул helm upgrade consul --install --create-namespace --namespace=consul --values=consul/values.yaml consul-k8s/charts/consul/
ингрес для ui консула:
kubectl apply -f consul/ingress.yaml
```

2) установка Vault
клонировать репозиторий с чартом волта ```git clone https://github.com/hashicorp/vault-helm.git```
```
helm install -n vault --create-namespace -f vault/values.yaml vault bitnami/vault
установить волт helm upgrade --install vault --create-namespace --namespace=vault --values=vault/values.yaml vault-helm/
```

3) распаковка волта:
```
kubectl exec vault-0 -n vault -- vault operator init
kubectl exec -it vault-0 -n vault -- vault operator unseal
kubectl exec -it vault-1 -n vault -- vault operator unseal
kubectl exec -it vault-2 -n vault -- vault operator unseal
```
4) создание хранилище секретов и секрет:
```
kubectl exec -it vault-0 -n vault -- vault login
kubectl exec -it vault-0 -n vault -- vault secrets enable -path otus -version=2 kv
kubectl exec -it vault-0 -n vault -- vault kv put otus/cred username=otus password=asajkjkahs
```
5) создание serviceAccount:
```
kubectl apply -f sa.yaml
```
6) включение авторизации auth/kubernetes:
```
kubectl exec -it vault-0 -n vault -- vault auth enable kubernetes

TOKEN_REVIEW_JWT=$(kubectl get secret -n vault vault-auth -o go-template='{{ .data.token }}' | base64 --decode)
KUBE_CA_CERT=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode)
KUBE_HOST=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.server}')

kubectl exec -it vault-0 -n vault -- vault write auth/kubernetes/config token_reviewer_jwt="$TOKEN_REVIEW_JWT" kubernetes_host="$KUBE_HOST" kubernetes_ca_cert="$KUBE_CA_CERT"
```
получаю в результате "Success! Data written to: auth/kubernetes/config"

7) создание otus-policy:
```
kubectl exec -it vault-0 -n vault -- vault policy write otus-policy - <<EOF
path "otus/*" {
  capabilities = ["read", "list"]
}

path "/v1/otus/*" {
  capabilities = ["read", "list"]
}
EOF
```

получаю "Success! Uploaded policy: otus-policy"

8) Создать роль auth/kubernetes/role/otus в vault с использованием ServiceAccount vault-auth из namespace Vault и политикой otus-policy:
```kubectl exec -it vault-0 -n vault -- vault write auth/kubernetes/role/otus bound_service_account_names="vault-auth" bound_service_account_namespaces="vault" policies="otus-policy" ttl="300h"```
получаю "Success! Data written to: auth/kubernetes/role/otus"

9) Установить External Secrets Operator:
```helm repo add external-secrets https://charts.external-secrets.io```
```helm install external-secrets --namespace=vault external-secrets/external-secrets```

11) Сохраниение в секреты client токена:
получаю токен ```curl --request POST --data '{"jwt": "'$TOKEN_REVIEW_JWT'", "role": "otus"}' http://127.0.0.1:55159/v1/auth/kubernetes/login | jq '.auth.client_token' | base64```
сохраняю его в client-token.yaml и создаю секрет ```kubectl apply -f client-token.yaml```

12) создание secretStore:
```
kubectl apply -f secret-store.yaml
```
13) создание externalSecret:
```
kubectl apply -f external-secret.yaml
```
14) проверка:
```
kubectl describe externalsecrets.external-secrets.io  -A
```
```
Name:         otus-external-secret
Namespace:    vault
Labels:       <none>
Annotations:  <none>
API Version:  external-secrets.io/v1beta1
Kind:         ExternalSecret
Metadata:
  Creation Timestamp:  2024-09-15T19:01:10Z
  Generation:          2
  Resource Version:    87630
  UID:                 b77e3ccf-6047-4a73-9d11-ac21e4c9edee
Spec:
  Data:
    Remote Ref:
      Conversion Strategy:  Default
      Decoding Strategy:    None
      Key:                  otus/cred
      Metadata Policy:      None
      Property:             username
    Secret Key:             username
    Remote Ref:
      Conversion Strategy:  Default
      Decoding Strategy:    None
      Key:                  otus/cred
      Metadata Policy:      None
      Property:             password
    Secret Key:             password
  Refresh Interval:         1h
  Secret Store Ref:
    Kind:  SecretStore
    Name:  vault-secret-store
  Target:
    Creation Policy:  Owner
    Deletion Policy:  Retain
    Name:             otus-cred
Status:
  Binding:
    Name:  otus-cred
  Conditions:
    Last Transition Time:   2024-09-16T05:50:12Z
    Message:                Secret was synced
    Reason:                 SecretSynced
    Status:                 True
    Type:                   Ready
  Refresh Time:             2024-09-16T05:50:12Z
  Synced Resource Version:  2-4145dbb39b277ce94d80d0d08075e0b1
Events:
  Type     Reason        Age                 From              Message
  ----     ------        ----                ----              -------
  Normal   Created       15s                 external-secrets  Created Secret
```