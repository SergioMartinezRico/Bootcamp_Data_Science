INSERT INTO Campus (campus_id, nombre, ciudad) VALUES
(1, 'Madrid', 'Madrid'),
(2, 'Valencia', 'Valencia');


INSERT INTO Modalidad (modalidad_id, nombre_modalidad) VALUES
(1, 'Presencial'),
(2, 'Online');

INSERT INTO Promocion (promocion_id, nombre, modalidad_id, campus_id) VALUES
(1, 'Septiembre', 1, 1),
(2, 'Febrero', 1, 1),
(3, 'Febrero', 1, 2);

INSERT INTO Tipo_Bootcamp (tipo_bootcamp_id, nombre_tipo, duracion_semanas) VALUES
(1, 'Data', 12),
(2, 'Full Stack', 16);

-- Proyectos Data
INSERT INTO Proyecto (proyecto_id, nombre_proyecto, tipo_bootcamp_id) VALUES
(1, 'HLF', 1),
(2, 'EDA', 1),
(3, 'BBDD', 1),
(4, 'ML', 1),
(5, 'Deployment', 1);

-- Proyectos Full Stack
INSERT INTO Proyecto (proyecto_id, nombre_proyecto, tipo_bootcamp_id) VALUES
(6, 'WebDev', 2),
(7, 'FrontEnd', 2),
(8, 'Backend', 2),
(9, 'React', 2),
(10, 'FullStack', 2);



INSERT INTO Rol (rol_id, tipo_rol) VALUES
(1, 'TA'),
(2, 'LI');


INSERT INTO Profesor (profesor_id, nombre, apellido, email, rol_id, campus_id) VALUES
(1, 'Noa', 'Yáñez', 'Noa_Yáñez@gmail.com', 1, 1),
(2, 'Saturnina', 'Benitez', 'Saturnina_Benitez@gmail.com', 1, 1),
(3, 'Anna', 'Feliu', 'Anna_Feliu@gmail.com', 1, 1),
(4, 'Rosalva', 'Ayuso', 'Rosalva_Ayuso@gmail.com', 1, 2),
(5, 'Ana Sofía', 'Ferrer', 'Ana_Sofía_Ferrer@gmail.com', 1, 2),
(6, 'Angélica', 'Corral', 'Angélica_Corral@gmail.com', 1, 1),
(7, 'Ariel', 'Lledó', 'Ariel_Lledó@gmail.com', 1, 1),
(8, 'Mario', 'Prats', 'Mario_Prats@gmail.com', 2, 2),
(9, 'Luis Ángel', 'Suárez', 'Luis_Ángel_Suárez@gmail.com', 2, 1),
(10, 'María Dolores', 'Diaz', 'Maria_Dolores_Diaz@gmail.com', 2, 1);


-- ============================
-- Tabla Alumno
-- ============================

-- Data Madrid Septiembre (15 alumnos)
INSERT INTO Alumno (alumno_id, nombre, apellido, email, fecha_comienzo, promocion_id) VALUES
(1, 'Jafet', 'Casals', 'Jafet_Casals@gmail.com', '2023-09-18', 1),
(2, 'Jorge', 'Manzanares', 'Jorge_Manzanares@gmail.com', '2023-09-18', 1),
(3, 'Onofre', 'Adadia', 'Onofre_Adadia@gmail.com', '2023-09-18', 1),
(4, 'Merche', 'Prada', 'Merche_Prada@gmail.com', '2023-09-18', 1),
(5, 'Pilar', 'Abella', 'Pilar_Abella@gmail.com', '2023-09-18', 1),
(6, 'Leoncio', 'Tena', 'Leoncio_Tena@gmail.com', '2023-09-18', 1),
(7, 'Odalys', 'Torrijos', 'Odalys_Torrijos@gmail.com', '2023-09-18', 1),
(8, 'Eduardo', 'Caparrós', 'Eduardo_Caparrós@gmail.com', '2023-09-18', 1),
(9, 'Ignacio', 'Goicoechea', 'Ignacio_Goicoechea@gmail.com', '2023-09-18', 1),
(10, 'Clementina', 'Santos', 'Clementina_Santos@gmail.com', '2023-09-18', 1),
(11, 'Daniela', 'Falcó', 'Daniela_Falcó@gmail.com', '2023-09-18', 1),
(12, 'Abraham', 'Vélez', 'Abraham_Vélez@gmail.com', '2023-09-18', 1),
(13, 'Maximiliano', 'Menéndez', 'Maximiliano_Menéndez@gmail.com', '2023-09-18', 1),
(14, 'Anita', 'Heredia', 'Anita_Heredia@gmail.com', '2023-09-18', 1),
(15, 'Eli', 'Casas', 'Eli_Casas@gmail.com', '2023-09-18', 1);

-- Data Madrid Febrero (10 alumnos)
INSERT INTO Alumno (alumno_id, nombre, apellido, email, fecha_comienzo, promocion_id) VALUES
(16, 'Guillermo', 'Borrego', 'Guillermo_Borrego@gmail.com', '2024-02-12', 2),
(17, 'Sergio', 'Aguirre', 'Sergio_Aguirre@gmail.com', '2024-02-12', 2),
(18, 'Carlito', 'Carrión', 'Carlito_Carrión@gmail.com', '2024-02-12', 2),
(19, 'Haydée', 'Figueroa', 'Haydée_Figueroa@gmail.com', '2024-02-12', 2),
(20, 'Chita', 'Mancebo', 'Chita_Mancebo@gmail.com', '2024-02-12', 2),
(21, 'Joaquina', 'Asensio', 'Joaquina_Asensio@gmail.com', '2024-02-12', 2),
(22, 'Cristian', 'Sarabia', 'Cristian_Sarabia@gmail.com', '2024-02-12', 2),
(23, 'Isabel', 'Ibáñez', 'Isabel_Ibáñez@gmail.com', '2024-02-12', 2),
(24, 'Desiderio', 'Jordá', 'Desiderio_Jordá@gmail.com', '2024-02-12', 2),
(25, 'Rosalina', 'Llanos', 'Rosalina_Llanos@gmail.com', '2024-02-12', 2);

-- Full Stack Madrid Septiembre (14 alumnos)
INSERT INTO Alumno (alumno_id, nombre, apellido, email, fecha_comienzo, promocion_id) VALUES
(26, 'Amor', 'Larrañaga', 'Amor_Larrañaga@gmail.com', '2023-09-18', 3),
(27, 'Teodoro', 'Alberola', 'Teodoro_Alberola@gmail.com', '2023-09-18', 3),
(28, 'Cleto', 'Plana', 'Cleto_Plana@gmail.com', '2023-09-18', 3),
(29, 'Aitana', 'Sebastián', 'Aitana_Sebastián@gmail.com', '2023-09-18', 3),
(30, 'Dolores', 'Valbuena', 'Dolores_Valbuena@gmail.com', '2023-09-18', 3),
(31, 'Julie', 'Ferrer', 'Julie_Ferrer@gmail.com', '2023-09-18', 3),
(32, 'Mireia', 'Cabañas', 'Mireia_Cabañas@gmail.com', '2023-09-18', 3),
(33, 'Flavia', 'Amador', 'Flavia_Amador@gmail.com', '2023-09-18', 3),
(34, 'Albino', 'Macias', 'Albino_Macias@gmail.com', '2023-09-18', 3),
(35, 'Ester', 'Sánchez', 'Ester_Sánchez@gmail.com', '2023-09-18', 3),
(36, 'Luis Miguel', 'Galvez', 'Luis_Miguel_Galvez@gmail.com', '2023-09-18', 3),
(37, 'Loida', 'Arellano', 'Loida_Arellano@gmail.com', '2023-09-18', 3),
(38, 'Heraclio', 'Duque', 'Heraclio_Duque@gmail.com', '2023-09-18', 3),
(39, 'Herberto', 'Figueras', 'Herberto_Figueras@gmail.com', '2023-09-18', 3);

-- Full Stack Valencia Febrero (13 alumnos)
INSERT INTO Alumno (alumno_id, nombre, apellido, email, fecha_comienzo, promocion_id) VALUES
(40, 'Teresa', 'Laguna', 'Teresa_Laguna@gmail.com', '2024-02-12', 4),
(41, 'Estrella', 'Murillo', 'Estrella_Murillo@gmail.com', '2024-02-12', 4),
(42, 'Ernesto', 'Uriarte', 'Ernesto_Uriarte@gmail.com', '2024-02-12', 4),
(43, 'Daniela', 'Guitart', 'Daniela_Guitart@gmail.com', '2024-02-12', 4),
(44, 'Timoteo', 'Trillo', 'Timoteo_Trillo@gmail.com', '2024-02-12', 4),
(45, 'Ricarda', 'Tovar', 'Ricarda_Tovar@gmail.com', '2024-02-12', 4),
(46, 'Alejandra', 'Vilaplana', 'Alejandra_Vilaplana@gmail.com', '2024-02-12', 4),
(47, 'Daniel', 'Rosselló', 'Daniel_Rosselló@gmail.com', '2024-02-12', 4),
(48, 'Rita', 'Olivares', 'Rita_Olivares@gmail.com', '2024-02-12', 4),
(49, 'Cleto', 'Montes', 'Cleto_Montes@gmail.com', '2024-02-12', 4),
(50, 'Marino', 'Castilla', 'Marino_Castilla@gmail.com', '2024-02-12', 4),
(51, 'Estefanía', 'Valcárcel', 'Estefanía_Valcárcel@gmail.com', '2024-02-12', 4),
(52, 'Noemí', 'Vilanova', 'Noemí_Vilanova@gmail.com', '2024-02-12', 4);

-- ============================
-- Tabla Alumno_Proyecto
-- ============================

-- Para simplificar, se sigue este orden:
-- Data: proyecto_id 1-5 (HLF, EDA, BBDD, ML, Deployment)
-- Full Stack: proyecto_id 6-10 (WebDev, FrontEnd, Backend, React, FullStack)
-- alumno_proyecto_id = 1..260

-- INSERTS generados automáticamente según CSVs:

-- Data Madrid Septiembre (alumnos 1-15)
INSERT INTO Alumno_Proyecto (alumno_proyecto_id, alumno_id, proyecto_id, resultado) VALUES
(1,1,1,'Apto'),(2,1,2,'No Apto'),(3,1,3,'Apto'),(4,1,4,'Apto'),(5,1,5,'Apto'),
(6,2,1,'Apto'),(7,2,2,'No Apto'),(8,2,3,'Apto'),(9,2,4,'Apto'),(10,2,5,'Apto'),
(11,3,1,'Apto'),(12,3,2,'Apto'),(13,3,3,'Apto'),(14,3,4,'No Apto'),(15,3,5,'Apto'),
(16,4,1,'Apto'),(17,4,2,'No Apto'),(18,4,3,'No Apto'),(19,4,4,'Apto'),(20,4,5,'No Apto'),
(21,5,1,'Apto'),(22,5,2,'No Apto'),(23,5,3,'Apto'),(24,5,4,'Apto'),(25,5,5,'Apto'),
(26,6,1,'Apto'),(27,6,2,'Apto'),(28,6,3,'Apto'),(29,6,4,'Apto'),(30,6,5,'Apto'),
(31,7,1,'No Apto'),(32,7,2,'Apto'),(33,7,3,'Apto'),(34,7,4,'Apto'),(35,7,5,'Apto'),
(36,8,1,'No Apto'),(37,8,2,'Apto'),(38,8,3,'Apto'),(39,8,4,'Apto'),(40,8,5,'Apto'),
(41,9,1,'Apto'),(42,9,2,'Apto'),(43,9,3,'Apto'),(44,9,4,'No Apto'),(45,9,5,'Apto'),
(46,10,1,'Apto'),(47,10,2,'No Apto'),(48,10,3,'Apto'),(49,10,4,'Apto'),(50,10,5,'Apto'),
(51,11,1,'Apto'),(52,11,2,'Apto'),(53,11,3,'Apto'),(54,11,4,'Apto'),(55,11,5,'Apto'),
(56,12,1,'Apto'),(57,12,2,'No Apto'),(58,12,3,'No Apto'),(59,12,4,'Apto'),(60,12,5,'Apto'),
(61,13,1,'Apto'),(62,13,2,'No Apto'),(63,13,3,'Apto'),(64,13,4,'Apto'),(65,13,5,'Apto'),
(66,14,1,'Apto'),(67,14,2,'Apto'),(68,14,3,'Apto'),(69,14,4,'Apto'),(70,14,5,'Apto'),
(71,15,1,'Apto'),(72,15,2,'Apto'),(73,15,3,'Apto'),(74,15,4,'Apto'),(75,15,5,'Apto');

-- Data Madrid Febrero (alumnos 16-25)
INSERT INTO Alumno_Proyecto (alumno_proyecto_id, alumno_id, proyecto_id, resultado) VALUES
(76,16,1,'Apto'),(77,16,2,'No Apto'),(78,16,3,'No Apto'),(79,16,4,'Apto'),(80,16,5,'No Apto'),
(81,17,1,'Apto'),(82,17,2,'No Apto'),(83,17,3,'Apto'),(84,17,4,'Apto'),(85,17,5,'No Apto'),
(86,18,1,'Apto'),(87,18,2,'No Apto'),(88,18,3,'Apto'),(89,18,4,'Apto'),(90,18,5,'Apto'),
(91,19,1,'Apto'),(92,19,2,'Apto'),(93,19,3,'Apto'),(94,19,4,'Apto'),(95,19,5,'Apto'),
(96,20,1,'No Apto'),(97,20,2,'Apto'),(98,20,3,'No Apto'),(99,20,4,'Apto'),(100,20,5,'Apto'),
(101,21,1,'No Apto'),(102,21,2,'No Apto'),(103,21,3,'Apto'),(104,21,4,'Apto'),(105,21,5,'Apto'),
(106,22,1,'Apto'),(107,22,2,'Apto'),(108,22,3,'No Apto'),(109,22,4,'Apto'),(110,22,5,'Apto'),
(111,23,1,'No Apto'),(112,23,2,'Apto'),(113,23,3,'No Apto'),(114,23,4,'Apto'),(115,23,5,'Apto'),
(116,24,1,'No Apto'),(117,24,2,'Apto'),(118,24,3,'No Apto'),(119,24,4,'No Apto'),(120,24,5,'Apto'),
(121,25,1,'Apto'),(122,25,2,'Apto'),(123,25,3,'Apto'),(124,25,4,'Apto'),(125,25,5,'Apto');

-- Full Stack Madrid Septiembre (alumnos 26-39)
INSERT INTO Alumno_Proyecto (alumno_proyecto_id, alumno_id, proyecto_id, resultado) VALUES
(126,26,6,'Apto'),(127,26,7,'Apto'),(128,26,8,'Apto'),(129,26,9,'Apto'),(130,26,10,'No Apto'),
(131,27,6,'No Apto'),(132,27,7,'No Apto'),(133,27,8,'Apto'),(134,27,9,'No Apto'),(135,27,10,'Apto'),
(136,28,6,'Apto'),(137,28,7,'No Apto'),(138,28,8,'Apto'),(139,28,9,'No Apto'),(140,28,10,'Apto'),
(141,29,6,'Apto'),(142,29,7,'No Apto'),(143,29,8,'Apto'),(144,29,9,'No Apto'),(145,29,10,'Apto'),
(146,30,6,'Apto'),(147,30,7,'Apto'),(148,30,8,'Apto'),(149,30,9,'Apto'),(150,30,10,'No Apto'),
(151,31,6,'No Apto'),(152,31,7,'No Apto'),(153,31,8,'No Apto'),(154,31,9,'Apto'),(155,31,10,'No Apto'),
(156,32,6,'No Apto'),(157,32,7,'Apto'),(158,32,8,'Apto'),(159,32,9,'Apto'),(160,32,10,'Apto'),
(161,33,6,'Apto'),(162,33,7,'Apto'),(163,33,8,'No Apto'),(164,33,9,'Apto'),(165,33,10,'Apto'),
(166,34,6,'No Apto'),(167,34,7,'Apto'),(168,34,8,'Apto'),(169,34,9,'Apto'),(170,34,10,'Apto'),
(171,35,6,'No Apto'),(172,35,7,'Apto'),(173,35,8,'Apto'),(174,35,9,'No Apto'),(175,35,10,'Apto'),
(176,36,6,'No Apto'),(177,36,7,'Apto'),(178,36,8,'Apto'),(179,36,9,'Apto'),(180,36,10,'Apto'),
(181,37,6,'Apto'),(182,37,7,'Apto'),(183,37,8,'Apto'),(184,37,9,'Apto'),(185,37,10,'Apto'),
(186,38,6,'Apto'),(187,38,7,'Apto'),(188,38,8,'No Apto'),(189,38,9,'No Apto'),(190,38,10,'No Apto'),
(191,39,6,'Apto'),(192,39,7,'Apto'),(193,39,8,'Apto'),(194,39,9,'Apto'),(195,39,10,'Apto');

-- Full Stack Valencia Febrero (alumnos 40-52)
INSERT INTO Alumno_Proyecto (alumno_proyecto_id, alumno_id, proyecto_id, resultado) VALUES
(196,40,6,'Apto'),(197,40,7,'Apto'),(198,40,8,'Apto'),(199,40,9,'Apto'),(200,40,10,'Apto'),
(201,41,6,'Apto'),(202,41,7,'Apto'),(203,41,8,'No Apto'),(204,41,9,'Apto'),(205,41,10,'Apto'),
(206,42,6,'Apto'),(207,42,7,'Apto'),(208,42,8,'Apto'),(209,42,9,'Apto'),(210,42,10,'Apto'),
(211,43,6,'Apto'),(212,43,7,'No Apto'),(213,43,8,'No Apto'),(214,43,9,'Apto'),(215,43,10,'Apto'),
(216,44,6,'No Apto'),(217,44,7,'Apto'),(218,44,8,'Apto'),(219,44,9,'Apto'),(220,44,10,'No Apto'),
(221,45,6,'Apto'),(222,45,7,'Apto'),(223,45,8,'Apto'),(224,45,9,'Apto'),(225,45,10,'Apto'),
(226,46,6,'No Apto'),(227,46,7,'No Apto'),(228,46,8,'No Apto'),(229,46,9,'Apto'),(230,46,10,'Apto'),
(231,47,6,'No Apto'),(232,47,7,'No Apto'),(233,47,8,'Apto'),(234,47,9,'No Apto'),(235,47,10,'No Apto'),
(236,48,6,'No Apto'),(237,48,7,'No Apto'),(238,48,8,'No Apto'),(239,48,9,'Apto'),(240,48,10,'Apto'),
(241,49,6,'No Apto'),(242,49,7,'No Apto'),(243,49,8,'No Apto'),(244,49,9,'No Apto'),(245,49,10,'Apto'),
(246,50,6,'Apto'),(247,50,7,'Apto'),(248,50,8,'No Apto'),(249,50,9,'Apto'),(250,50,10,'Apto'),
(251,51,6,'No Apto'),(252,51,7,'Apto'),(253,51,8,'No Apto'),(254,51,9,'No Apto'),(255,51,10,'Apto'),
(256,52,6,'Apto'),(257,52,7,'No Apto'),(258,52,8,'No Apto'),(259,52,9,'Apto'),(260,52,10,'Apto');

