Для проверки нужно:
- включить миникуб minikube start
- включить ингресс-контроллер minikube addons enable ingress
- включить туннель в миникуб minikube tunnel
- добавить в hosts запись 127.0.0.1 homework.otus
- выполнить kubectl label nodes minikube homework=true (для того точбы запустились поды, см. доп. задания из ДЗ №2)
- перейти в папку с ДЗ №4 cd kubernetes-volumes
- выполнить команды:
kubectl apply -f kube-metrics-exporter/namespace.yaml - добавить неймспейс для экспортера метрик кубера
kubectl apply -f kube-metrics-exporter - установить экспортер метрик кубера
kubectl apply -f namespace.yaml   - создание неймспейса homework
kubectl apply -f configmap-nginx.yaml   - создание конфигурации  nginx
kubectl apply -f cm.yaml   - создание конфигмапа из задания 4 (с произвольным набором ключей)
kubectl apply -f storageClass.yaml   - создание storageClass (доп. задание из ДЗ №5)
kubectl apply -f pvc.yaml   - создание pvc c кастомным storageClass
kubectl apply -f deployment.yaml   - развертывание приложения
kubectl apply -f service.yaml  - настройка сервиса
kubectl apply -f ingress.yaml   - настройка ингресса 

для создания kubeconfig файла выполнить действия из файла cd-cert/readme.md

kubectl create token cd --namespace homework --duration 24h > token  - генерация суточного токена для SA "cd"