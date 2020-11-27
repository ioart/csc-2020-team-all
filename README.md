Этот репозиторий предназначен для рецензирования кода проектов, сделанных во время прохождения курса "Базы Данных" в Computer Science Center

## 2020-11-12
**Сеньор**: Артем Иоселевский
**Джуниор**: Анна Родионова
**Цель**: создать удаленную базу на https://www.elephantsql.com/ и подключиться к ней
**Результат**: цель достигнута


## Как залить код проекта в репозиторий

* Этот скрипт предполагает, что у вас Linux в котором есть git CLI и вы умеете авторизовываться в GitHub (что не очень тривиально). Если у вас иная OS, сделайте аналогичные действия её средствами
* Первым аргументом скрипта является номер вашего проекта, вторым -- путь к текстовому файлу с вашим кодом

```
#!/bin/sh
PRJ=project$1
git clone https://github.com/dbms-class/csc-2020-team-all
cd csc-2020-team-all
git checkout -b $PRJ
mkdir $PRJ
cd $PRJ
cp "$2" $PRJ.sql
git add $PRJ.sql
git commit 
git push origin $PRJ
```

Пример запуска: `./commit 42 /tmp/проект42`. Этот же скрипт, но без команды git clone и последующей cd, лежит в репозитории. 

## Требования к коду проекта

1. Код должен быть работоспособным, то есть, файл, будучи скормленным постгресу как есть, должен выполняться без ошибок и создавать в пустой бахе все требуемые таблицы. **цель B и выше**
1. К каждой таблице должен быть дан комментарий, объясняющий смысл фиксированной строки таблицы. Для простых таблиц, описывающих очевидные свойства одного очевидно простого объекта, достаточно комментария вида "-- Строка представляет из себя объект Звездолёт с его свойствами". Для справочников достаточно комментария вида "-- справочник политических строев". Для более сложных таблиц, реализующих связи, комментарий должен выглядеть так: "-- звездолёт spacecraft_id совершил полёт на планету planet_id под управлением капитана commander_id в дату date". Комментарий должен находиться перед оператором CREATE TABLE и выглядеть как однострочный SQL комментарий, то есть начинаться с двух минусов. **цель B и выше**
    ```
    -- звездолёт spacecraft_id совершил полёт на планету planet_id под управлением капитана commander_id в дату date
    CREATE TABLE Flight(spacecraft_id INT, planet_id INT, commander_id INT, date DATE)
    ```
1. В таблицах должны быть объявлены все уместные CHECK ограничения. **цель C и выше**
1. В таблицах должны быть объявлены все уместные естественные ключи (UNIQUE). К каждому объявленному ключу должен быть комментарий, объясняющий, какую цель преследует этот ключ. Это должен быть ответ на вопрос вида "чтобы что?" и он должен быть в виде SQL комментария перед определением ключа:
    ```
    -- звездолёт spacecraft_id совершил полёт на планету planet_id под управлением капитана commander_id в дату date
    CREATE TABLE Flight(spacecraft_id INT, planet_id INT, commander_id INT, date DATE, 
      -- чтобы в один и тот же день не могло быть два разных полёта
      UNIQUE(date)
    )
    ```
    Вне зависимости от того, сколько ключей в ней объявлено, должен быть комментарий вида "-- других ключей нет". Это будет сигналом того, что про таблицу не забыли. **цель D и выше**
1. К каждому внешнему ключу или паре внешних ключей должен быть комментарий, объясняющий какого вида связь (1:N, M:N, N:1, 1:1) он реализует. Так и должно быть записано:
    ```
    CREATE TABLE Booking(
      -- Связь N:M между полётами и пассажирами. Каждый пассажир может летать много раз. На каждом полёте может быть много пассажиров.
      flight_id INT REFERENCES Flight, pax_id INT REFERENCES Pax
    )
    ```
    **цель D и выше**
