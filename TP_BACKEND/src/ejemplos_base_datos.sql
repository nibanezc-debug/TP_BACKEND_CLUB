USE CLUB;

-- Reinicio limpio de tablas para poder correr la prueba las veces que quieras en clase
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE RESERVAS;
TRUNCATE TABLE CANCHAS;
TRUNCATE TABLE SOCIOS;
TRUNCATE TABLE DEPORTES;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. DEPORTES
INSERT INTO DEPORTES (id_deporte, deporte) VALUES 
(1, 'Fútbol'),
(2, 'Tenis'),
(3, 'Pádel');

-- 2. CANCHAS
INSERT INTO CANCHAS (id_cancha, nombre, id_deporte, precio_hora, techada, activa) VALUES
(1, 'Cancha 1 - Césped Sintético', 1, 15000, FALSE, TRUE),   -- Con reservas
(2, 'Cancha Central - Ladrillo',    2, 12000, FALSE, TRUE),   -- Con reservas
(3, 'Pista Pádel Crystal 1',        3, 10000, TRUE,  TRUE),   -- Con reservas
(4, 'Cancha 2 - Fútbol Techado',   1, 18000, TRUE,  TRUE),   -- Con reservas
(5, 'Pista Pádel Panorama (Baja)', 3, 9500,  FALSE, FALSE),  -- Inactiva
(6, 'Cancha 3 - Fútbol 5 Nuevo',   1, 14000, FALSE, TRUE);   -- SIN reservas (Ideal para probar DELETE)

-- 3. SOCIOS
INSERT INTO SOCIOS (id_socio, nombre, email, activo) VALUES
(1, 'Lionel Messi', 'leo.messi@club.com', TRUE),
(2, 'Franco Colapinto', 'franco.colapinto@club.com', TRUE),
(3, 'Gabriela Sabatini', 'gabi.sabatini@club.com', TRUE),
(4, 'Agustín Tapia', 'agustin.tapia@club.com', TRUE);

-- 4. RESERVAS
INSERT INTO RESERVAS (id_reserva, id_socio, id_cancha, fecha_inicio, fecha_fin, tarifa_historica, total, estado) VALUES
(1, 1, 1, '2026-10-10T18:00:00', '2026-10-10T20:00:00', 15000, 30000, 'confirmada'),
(2, 2, 2, '2026-10-11T09:00:00', '2026-10-11T10:00:00', 12000, 12000, 'confirmada'),
(3, 3, 3, '2026-10-12T15:00:00', '2026-10-12T17:00:00', 10000, 20000, 'confirmada'),
(4, 4, 4, '2026-10-13T20:00:00', '2026-10-13T21:00:00', 18000, 18000, 'confirmada'),
(5, 1, 1, '2026-10-14T19:00:00', '2026-10-14T20:00:00', 15000, 15000, 'cancelada');