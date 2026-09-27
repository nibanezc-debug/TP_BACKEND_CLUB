CREATE DATABASE IF NOT EXISTS CLUB;
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
email VARCHAR(80) NOT NULL UNIQUE,
activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE RESERVAS
(
id_reserva INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
id_socio INT NOT NULL,
id_cancha INT NOT NULL,
fecha_inicio VARCHAR(35) NOT NULL,
fecha_fin VARCHAR(35) NOT NULL,
tarifa_historica INT NOT NULL,
total INT NOT NULL,
estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
foreign key (id_socio) references SOCIOS(id_socio),
foreign key (id_cancha) references CANCHAS(id_cancha)
);


