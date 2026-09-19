CREATE DATABASE CLUB;
USE CLUB;

CREATE TABLE DEPORTES
(
id_deporte INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
deporte VARCHAR(50)
);

CREATE TABLE CANCHAS
(
id_cancha INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL,
id_deporte INT,
precio_hora INT,
techada BOOLEAN DEFAULT FALSE,
activa BOOLEAN DEFAULT TRUE,
foreign key (id_deporte) references DEPORTES(id_deporte)
);

CREATE TABLE SOCIOS
(
id_socio INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(80) NOT NULL,
email VARCHAR(80),
activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE RESERVAS
(
id_reserva INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
id_socio INT,
id_cancha INT,
fecha_inicio VARCHAR(35),
fecha_fin VARCHAR(35),
tarifa_historica INT,
total INT,
estado BOOLEAN,
foreign key (id_socio) references SOCIOS(id_socio),
foreign key (id_cancha) references CANCHAS(id_cancha)
);

