# smart_house
***
Чтобы запустить сервис нужно выполнить следующее:
sudo docker compose up -d

cd my-react-app
npm run dev

***
Для вывода списка всех запущенных контейнеров пишем команду
docker ps

Находим контейнер с кафкой и пишем команду для входа в bash терминал контейнера
docker exec -it {container_id} bash

Далее переходим в директорию где находятся скрипты кафки
cd /
cd bin

После перехода в директорию можем посмотреть список всех команд кафки
ls | grep kafka

Пример использования команд:

kafka-topics --bootstrap-server localhost:9092 --list - Выведет список всех созданных топиков
kafka-console-consumer --bootstrap-server localhost:9092 --topic {topic_name} - Запустить процесс процесс прослушивания топика(
    можно добавить флаг --from-beginning для отображения сообщений с момента создания топика
)
kafka-console-producer --bootstrap-server localhost:9092 --topic {topic_name} - Запустить процесс записи сообщений в выбранный топик
***
***
Чтобы зайти и мосмотреть логи сервисов нужно сделать
sudo docker exec -it {service-name} /bin/sh
ls |grep "log"
tail -f {log-file}
***
