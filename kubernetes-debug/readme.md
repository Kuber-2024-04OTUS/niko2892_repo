1) запустить миникуб minikube start
2) создать под  kyos0109/nginx-distroless:
kubectl create ns homework
kubectl apply -f nginx-config.yaml
kubectl apply -f nginx-distroless.yaml
3) создание эфимерного контейнера для отладки пода:
kubectl -n homework debug -it nginx-distroless --image=busybox --target=nginx --share-processes
4) результат ls -la /proc/1/root/etc/nginx/ иэ эфимерного контейнера:
```
total 48
drwxr-xr-x    3 root     root          4096 Oct  5  2020 .
drwxr-xr-x    1 root     root          4096 Sep 16 10:56 ..
drwxr-xr-x    2 root     root          4096 Oct  5  2020 conf.d
-rw-r--r--    1 root     root          1007 Apr 21  2020 fastcgi_params
-rw-r--r--    1 root     root          2837 Apr 21  2020 koi-utf
-rw-r--r--    1 root     root          2223 Apr 21  2020 koi-win
-rw-r--r--    1 root     root          5231 Apr 21  2020 mime.types
lrwxrwxrwx    1 root     root            22 Apr 21  2020 modules -> /usr/lib/nginx/modules
-rw-r--r--    1 root     101            636 Sep 16 10:56 nginx.conf
-rw-r--r--    1 root     root           636 Apr 21  2020 scgi_params
-rw-r--r--    1 root     root           664 Apr 21  2020 uwsgi_params
-rw-r--r--    1 root     root          3610 Apr 21  2020 win-utf
```

5) запустить tcpdump в отладочном контейнере (для запуска утилиты использовал другой образ nicolaka/netshoot):
tcpdump -nn -i any -e port 80

6) сделать запрос к nginx (сделал со своего ПК через port-forward)
результат работы tcpdump сохранил в tcpdump.txt

7) запустить отладочный контейнеро для ноды, на которой работает nginx-distroless
kubectl -it debug node/minikube --image=busybox

8) посмотреть логи nginx-distroless из отладочного контейнера:
cat /host/var/log/pods/homework_nginx-distroless_ca0f7d2b-1f83-4e11-b287-967a3aa026b9/nginx/0.log

```
{"log":"127.0.0.1 - - [16/Sep/2024:19:13:26 +0800] \"GET / HTTP/1.1\" 200 612 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C
hrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0\" \"-\"\n","stream":"stdout","time":"2024-09-16T11:13:26.302429583Z"}
{"log":"127.0.0.1 - - [16/Sep/2024:19:13:26 +0800] \"GET /favicon.ico HTTP/1.1\" 404 555 \"http://localhost:53630/\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe
bKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0\" \"-\"\n","stream":"stdout","time":"2024-09-16T11:13:26.63281131Z"}
{"log":"2024/09/16 19:13:26 [error] 7#7: *2 open() \"/usr/share/nginx/html/favicon.ico\" failed (2: No such file or directory), client: 127.0.0.1, server: localhost, re
quest: \"GET /favicon.ico HTTP/1.1\", host: \"localhost:53630\", referrer: \"http://localhost:53630/\"\n","stream":"stderr","time":"2024-09-16T11:13:26.633081926Z"}
{"log":"127.0.0.1 - - [16/Sep/2024:19:14:49 +0800] \"GET / HTTP/1.1\" 304 0 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chr
ome/128.0.0.0 Safari/537.36 Edg/128.0.0.0\" \"-\"\n","stream":"stdout","time":"2024-09-16T11:14:49.510199361Z"}
```

9) Выполнить strace:
kubectl debug -it nginx-distroless -n homework --image=nicolaka/netshoot --target=nginx --share-processes

попробовал в отладочном контейнере запустить strace -p 1
в результате получил:
strace: Process 1 attached
rt_sigsuspend([], 8

это и требовалось в задании. похоже, эфимерный контейнер по дефолту запускается с general профилем https://github.com/kubernetes/enhancements/tree/master/keps/sig-cli/1441-kubectl-debug#debugging-profiles