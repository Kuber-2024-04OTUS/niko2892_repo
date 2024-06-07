Для проверки нужно:
- включить миникуб minikube start
- включить ингресс-контроллер minikube addons ingress
- включить туннель в миникуб minikubu tunnel
- добавить в hosts запись 127.0.0.1 homework.otus
- выполнить kubectl label nodes minikube homework=true (для того точбы запустились поды, см. доп. задания из ДЗ №2)
- перейти в папку с ДЗ №3 cd kubernetes-networks
- выполнить команды:
kubectl apply -f namespace.yaml
kubectl apply -f configmap-nginx.yaml *я добавил страницу-заглушку, чтобы /homepage не возвращал 404
kubectl apply -f deployment.yaml
kubectl apply -f ingress.yaml