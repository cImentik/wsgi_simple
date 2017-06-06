--
-- Comment
--
CREATE TABLE IF NOT EXISTS comment
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT NOT NULL,
    firstname TEXT NOT NULL,
    patronymic TEXT,
    region_id INTEGER,
    city_id INTEGER,
    phone TEXT,
    email TEXT,
    comment TEXT NOT NULL,
    CONSTRAINT comment_city_id_fk FOREIGN KEY (city_id) REFERENCES city (id),
    CONSTRAINT comment_region_id_fk FOREIGN KEY (region_id) REFERENCES region (id)
);


--
-- City
--
CREATE TABLE IF NOT EXISTS city
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    region_id INTEGER,
    CONSTRAINT city_region_id_fk FOREIGN KEY (region_id) REFERENCES region (id)
);

--
-- Region
--
CREATE TABLE IF NOT EXISTS region
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

--
-- Insert Region
--
INSERT INTO region VALUES(NULL, 'Краснодарский край');
INSERT INTO region VALUES(NULL, 'Ростовская область');
INSERT INTO region VALUES(NULL, 'Ставропольский край');

--
-- Insert City for Regions
--
INSERT INTO city VALUES(NULL, 'Краснодар', 1);
INSERT INTO city VALUES(NULL, 'Кропоткин', 1);
INSERT INTO city VALUES(NULL, 'Славянск', 1);

INSERT INTO city VALUES(NULL, 'Ростов', 2);
INSERT INTO city VALUES(NULL, 'Шахты', 2);
INSERT INTO city VALUES(NULL, 'Батайск', 2);

INSERT INTO city VALUES(NULL, 'Ставрополь', 3);
INSERT INTO city VALUES(NULL, 'Пятигорск', 3);
INSERT INTO city VALUES(NULL, 'Кисловодск', 3);

--
-- Insert Comment with 5 comment for Region 1 City 1
--
INSERT INTO comment VALUES (NULL, 'Иванов1', 'Иван1', 'Иванович1', 1, 1, '(123) 4567890', 'mail@email.me', 'Комментарий1');
INSERT INTO comment VALUES (NULL, 'Иванов2', 'Иван2', 'Иванович2', 1, 1, '(123) 4567890', 'mail@email.me', 'Комментарий2');
INSERT INTO comment VALUES (NULL, 'Иванов3', 'Иван3', 'Иванович3', 1, 1, '(123) 4567890', 'mail@email.me', 'Комментарий3');
INSERT INTO comment VALUES (NULL, 'Иванов4', 'Иван4', 'Иванович4', 1, 1, '(123) 4567890', 'mail@email.me', 'Комментарий4');
INSERT INTO comment VALUES (NULL, 'Иванов5', 'Иван5', 'Иванович5', 1, 1, '(123) 4567890', 'mail@email.me', 'Комментарий5');

--
-- Insert Comment
--
INSERT INTO comment VALUES (NULL, 'Иванов6', 'Иван6', 'Иванович6', 1, 2, '(123) 4567890', 'mail@email.me', 'Комментарий6');
INSERT INTO comment VALUES (NULL, 'Иванов7', 'Иван7', 'Иванович7', 1, 3, '(123) 4567890', 'mail@email.me', 'Комментарий7');

INSERT INTO comment VALUES (NULL, 'Иванов8', 'Иван8', 'Иванович8', 2, 4, '(123) 4567890', 'mail@email.me', 'Комментарий8');
INSERT INTO comment VALUES (NULL, 'Иванов9', 'Иван9', 'Иванович9', 2, 5, '(123) 4567890', 'mail@email.me', 'Комментарий9');
INSERT INTO comment VALUES (NULL, 'Иванов10', 'Иван10', 'Иванович10', 2, 6, '(123) 4567890', 'mail@email.me', 'Комментарий10');

INSERT INTO comment VALUES (NULL, 'Иванов11', 'Иван11', 'Иванович11', 3, 7, '(123) 4567890', 'mail@email.me', 'Комментарий11');
INSERT INTO comment VALUES (NULL, 'Иванов12', 'Иван12', 'Иванович12', 3, 8, '(123) 4567890', 'mail@email.me', 'Комментарий12');
INSERT INTO comment VALUES (NULL, 'Иванов13', 'Иван13', 'Иванович13', 3, 9, '(123) 4567890', 'mail@email.me', 'Комментарий13');
INSERT INTO comment VALUES (NULL, 'Иванов13', 'Иван13', 'Иванович13', 3, 9, '(123) 4567890', 'mail@email.me', 'Комментарий13');
INSERT INTO comment VALUES (NULL, 'Иванов13', 'Иван13', 'Иванович13', 3, 9, '(123) 4567890', 'mail@email.me', 'Комментарий13');
INSERT INTO comment VALUES (NULL, 'Иванов13', 'Иван13', 'Иванович13', 3, 9, '(123) 4567890', 'mail@email.me', 'Комментарий13');