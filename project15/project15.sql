--Уникальная модель тс с описанием ее характеристик(тип, название, вместимость)
--Модель тс(id_vehicle, тип тс, название модели, вместимость)

CREATE TYPE model_type AS ENUM ('автобус', 'троллейбус', 'трамвай', 'ТУАХ', 'электробус');

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    type model_type NOT NULL,
    name TEXT NOT NULL,
    capacity INT CHECK(capacity > 0)
);


--Транспортные средства:
--модель транспортного средства с уникальным номером-идентификатором, определенного года выпуска и его актуальным состоянием.
--ТС(бортовой номер-идентификатор, год выпуска, состояние тс, модель тс(id_vehicle))

CREATE TYPE vehicle_state AS ENUM ('исправен', 'некритические неисправности', 'требует ремонта');

CREATE TABLE vehicle (
    -- 1:M одному тс соответствует одна модель, одной модели - много тс
    id SERIAL PRIMARY KEY,
    year_release INT NOT NULL CHECK(year_release BETWEEN 1800 AND 2200),
    state vehicle_state NOT NULL,
    model_id INT REFERENCES model(id)
);


--Остановки и маршруты:
--Уникальный номер остановки, с точным адресом и количеством платформ
--Остановки(номер остановки, адрес, количество платформ)

 CREATE TABLE stop (
    id  SERIAL PRIMARY KEY,
    address TEXT NOT NULL UNIQUE,
    platforms_count INT CHECK(platforms_count > 0)
);


--Номер маршрута известный пассажирам, начало и конец маршрута.
--Маршрут(уникальный номер, тип ТС который обслуживает, начальная остановка, конечная остановка)

CREATE TABLE route (
-- Связь 1:M у одного маршрута одна конечная остановка, у одной конечной остановки много маршрутов
    id INT PRIMARY KEY,
    type model_type NOT NULL,
    start_id INT REFERENCES stop(id),
    end_id INT REFERENCES stop(id),
);


--Номер ТС который выйдет на “номер маршрута” и время прибытия на определенную платформу в выходной или рабочий день.
--Расписание(тс, номер маршрута, день недели, время прибытия, номер остановки, платформа, выходной или рабочий день) (то есть время до минуты уникальное)

CREATE TABLE time_table (
    vehicle_id INT REFERENCES vehicle(id),
    route_id INT REFERENCES route(id),
    is_weekend BOOl NOT NULL,
    stop_id INT REFERENCES stop(id),
    platform_number INT CHECK(platform_number > 0) NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    UNIQUE(stop_id, platform_number, arrival_time)
-- На одной остановке у одной платформы в одно время может стоять одно тс
);


--Водитель с данным "номером служебного удостоверения" имеет данные "ФИО"
--Водитель(номер служебного удостоверения, фамилия, имя, отчество)

CREATE TABLE driver (
    id SERIAL PRIMARY KEY,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    patronymic TEXT
);


--Наряд с данным "ид наряда" дан ТС с "номером-идентификатором ТС" в данную "дату" с остановки с данным "персональным номером остановки"
--Наряд(ид наряда, ид маршрута, номер-идентификатор ТС, ид остановки, день, время, ид водителя)

CREATE TABLE work_order (
    -- 1:M одному наряду соответствует 1 маршрут, одному маршрут много нарядов
    -- 1:M одному наряду соответствует 1 тс, одному тс много нарядов
    -- 1:M одному наряду соответствует 1 начальная остановка, одной начальной остановке много нарядов
    -- 1:M одному наряду соответствует 1 водитель, одному водителю много нарядов
    id SERIAL PRIMARY KEY,
    route_id INT REFERENCES route(id),
    vehicle_id INT REFERENCES vehicle(id),
    stop_id INT REFERENCES stop(id),
    day DATE NOT NULL,
    start_time TIMESTAMP NOT NULL,
    driver_id INT REFERENCES driver(id),
    UNIQUE (day, vehicle_id)
);


--"Фактическое время прибытия" и “предполагаемое время прибытия”, когда водителем с данным “ид водителя” в наряде с данным "ид наряда" была посещена остановка с данным "персональным номером остановки"
--Диспетчерская(ид наряда, ид остановки, фактическое время прибытия, предполагаемое время прибытия)

CREATE TABLE control (
-- N:M одному наряду соответствует много остановок, одной остановке - много нарядов
    work_order_id INT REFERENCES work_order(id),
    stop_id INT REFERENCES stop(id),
    appointed_time TIMESTAMP NOT NULL,
    real_time TIMESTAMP NOT NULL,
);


--Пункт билетного меню с данным "ид" и "названием"
--БилетноеМеню(ид, название, стоимость)

CREATE TABLE ticket_menu (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price INT CHECK(price > 0)
);


--СтатистикаОплаты(ид пункта билетного меню, день, количество валидаций билета)

CREATE TABLE statistic (
    ticket_menu_id INT REFERENCES ticket_menu(id),
    day DATE NOT NULL,
    validations_count INT CHECK (validations_count >= 0),
    UNIQUE (ticket_menu_id, day)
);
