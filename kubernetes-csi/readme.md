1) создаю секрет с ключами для доступа к ObjectStorage
kubectl apply -f .\secret.yaml
2) создаю starageClass, описывающий класс хранилища:
kubectl apply -f .\storage-class.yaml
3) установка драйвера:
kubectl apply -f provisioner.yaml
kubectl apply -f driver.yaml
kubectl apply -f csi-s3.yaml
4) создание pvc:
kubectl apply -f pvc.yaml
5) создать под, который будет использовать objectstorage:
kubectl apply -f .\deployment.yaml