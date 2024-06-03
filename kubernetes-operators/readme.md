1) запустить миникуб minikube start --registry-mirror=https://c.163.com
2) запустить pip install kubernetes и pip install kopf
3) запустить оператор kopf run mysql-operator.py
4) создать crd kubectl apply -f crd.yaml
5) запустить kubernetes оператор командой kopf run mysql-operator.py
6) запустить приложение  kubectl apply -f mysql.yaml
7) посмотреть, что создались все необходимые ресурсы
8) удалить приложение  kubectl delete -f mysql.yaml
9) посмотреть, что удалились все ранее созданные ресурсы