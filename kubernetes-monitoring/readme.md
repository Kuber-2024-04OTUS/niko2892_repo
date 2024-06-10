1) запустить миникуб minikube start --registry-mirror=https://c.163.com
2) запустить деплоймент с кастомным образом nginx и экспортером:   kubectl apply -f .\nginx\deployment.yaml
3) включить сервис для него:    kubectl apply -f .\nginx\service.yaml
4) создать неймспейс для prometheus-operator:   kubectl create ns prometheus 
5) установить prometheus-operator. Для этого выполнить команды: 
- helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
- helm repo update
- helm -n prometheus install prometheus-stack prometheus-community/kube-prometheus-stack

6) добавить настройку для скейпинга метрик nginx:
    вариант №1: 
    получить values из чарта: helm show values prometheus-community/kube-prometheus-stack > .\prometheus-stack\values.yaml
    
    в values добавить 
    additionalServiceMonitors:
      - name: "nginx-exporter"
        namespaceSelector:
          any: true
        selector:
          matchLabels:
              app: nginx
        endpoints:
        - port: "nginx-exporter-port"
        - targetPort: "nginx-exporter-port"
          scheme: http 
    и выполнить helm -n prometheus upgrade -f .\prometheus-stack\values.yaml prometheus-stack prometheus-community/kube-prometheus-stack

    вариант №2: применить настройку из файла serviceMonitor.yaml
    выполнить kubectl apply -f .\prometheus-stack\serviceMonitor.yaml

7) пробросить порт для графаны: kubectl -n prometheus port-forward svc/prometheus-stack-grafana 8080:80
   ипортировать дашборд 12708 , уюбедиться, что на нем есть информация о работе nginx