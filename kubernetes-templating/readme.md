Подготовка:
- minikube start
- minikube addons enable ingress
- minikube tunnel
- добавить в файл hosts запись запись 127.0.0.1 homework.otus

Задание 1:
- Создаю чарт helm create nginx-otus
- Добавляю зависимость от другого чарта (redis):
    - helm repo add bitnami https://charts.bitnami.com/bitnami  - добавляю репозиторий с чартами
    - helm repo update  - обновляю информацию о репозитории
    - helm search repo --versions --devel redis  - смотрю доступные версии редиса
    - добавляю зависимость от redis в Chart.yaml:  
        dependencies:
        - name: redis
            version: "19.0.0"
            repository: "https://charts.bitnami.com/bitnami"
            condition: redis.enabled
    - helm dependency update  - обновляю зависимости своего чарта
    - в values.yaml включаю redis redis.enabled: true и меняю ему неймспейс redis.namespaceOverride: homework
    - helm install nginx-otus .\nginx-otus\  - устанавливаю чарт
Для развертывания приложения использовать команду helm install nginx-otus .\nginx-otus\

Задание 2:
- создаю helmfile.yaml и заполняю. Параметры для кафки беру из https://github.com/bitnami/charts/blob/main/bitnami/kafka/README.md
- запускаю helmfile командой helmfile apply