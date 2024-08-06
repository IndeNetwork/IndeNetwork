CREATE DATABASE IndeNetwork;

USE IndeNetwork;

CREATE TABLE PROFESORES (
    id_profesor INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    numDocumento_profesor INT(12) UNIQUE NOT NULL,
    nombre_profesor CHAR(50) NOT NULL,
    apellido_profesor CHAR(50) NOT NULL,
    foto_profesor VARCHAR(1000) NOT NULL DEFAULT '/static/archivos_subidos/miembros/imgs/perfiles/imagenDefault.png'
);

CREATE TABLE GRADOS (
    id_grado INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    num_grado INT NOT NULL,
    numGrupo_grado INT NOT NULL,
    UNIQUE (num_grado, numGrupo_grado)
);

CREATE TABLE ESTUDIANTES (
    id_estudiante INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    numMatricula_estudiante INT(12) UNIQUE NOT NULL,
    numDocumento_estudiante INT(12) UNIQUE NOT NULL,
    nombre_estudiante CHAR(50) NOT NULL,
    apellido_estudiante CHAR(50) NOT NULL,
    fk_grado INT NOT NULL,
    foto_estudiante VARCHAR(1000) NOT NULL DEFAULT '/static/archivos_subidos/miembros/imgs/perfiles/imagenDefault.png',
    FOREIGN KEY (fk_grado) REFERENCES GRADOS (id_grado)
);

CREATE TABLE MIEMBROS (
    id_miembro INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    tipo_miembro ENUM('Profesor', 'Estudiante') NOT NULL,
    fk_profesor INT,
    fk_estudiante INT,
    FOREIGN KEY (fk_profesor) REFERENCES PROFESORES (id_profesor) ON DELETE CASCADE,
    FOREIGN KEY (fk_estudiante) REFERENCES ESTUDIANTES (id_estudiante) ON DELETE CASCADE,
    CHECK ((fk_profesor IS NOT NULL AND fk_estudiante IS NULL) OR (fk_profesor IS NULL AND fk_estudiante IS NOT NULL))
);

CREATE TABLE AMIGOS (
    id_amigo INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro1 INT NOT NULL,
    fk_miembro2 INT NOT NULL,
    fechaHora_amigo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro1) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE,
    FOREIGN KEY (fk_miembro2) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE
);

CREATE TABLE MENSAJES (
    id_mensaje INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro1 INT NOT NULL,
    fk_miembro2 INT NOT NULL,
    contenido_mensaje VARCHAR(200) NOT NULL,
    fechaHora_mensaje TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro1) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE,
    FOREIGN KEY (fk_miembro2) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE
);

CREATE TABLE PUBLICACIONES (
    id_publicacion INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro INT NOT NULL,
    texto_publicacion VARCHAR(200) NOT NULL,
    archivo_publicacion VARCHAR(1000),
    imagen_publicacion VARCHAR(1000),
    fechaHora_publicacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE
);

CREATE TABLE COM_PUBLICACION (
    id_comPublicacion INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_publicacion INT NOT NULL,
    fk_miembro INT NOT NULL,
    texto_comPublicacion VARCHAR(200) NOT NULL,
    archivo_comPublicacion VARCHAR(1000),
    fechaHora_comPublicacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_publicacion) REFERENCES PUBLICACIONES (id_publicacion) ON DELETE CASCADE,
    FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE
);

CREATE TABLE ASIGNATURAS (
    id_asignatura INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_asignatura CHAR(50) NOT NULL
);

CREATE TABLE GRUPOS (
    id_grupo INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_profesor INT NOT NULL,
    fk_grado INT NOT NULL,
    descripcion_grupo VARCHAR(200) NOT NULL,
    fk_asignatura INT NOT NULL,
    fechaHora_grupo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_profesor) REFERENCES PROFESORES (id_profesor) ON DELETE CASCADE,
    FOREIGN KEY (fk_grado) REFERENCES GRADOS (id_grado) ON DELETE CASCADE,
    FOREIGN KEY (fk_asignatura) REFERENCES ASIGNATURAS (id_asignatura) ON DELETE CASCADE
);

CREATE TABLE INTEGRANTES (
    id_integrante INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_estudiante INT NOT NULL,
    fk_grupo INT NOT NULL,
    FOREIGN KEY (fk_estudiante) REFERENCES ESTUDIANTES (id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (fk_grupo) REFERENCES GRUPOS (id_grupo) ON DELETE CASCADE
);

CREATE TABLE TAREAS (
    id_tarea INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_grupo INT NOT NULL,
    titulo_tarea VARCHAR(50) NOT NULL,
    descripcion_tarea VARCHAR(500) NOT NULL,
    archivo_tarea VARCHAR(1000),
    fechaHora_tarea TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fechaHoraVen_tarea DATETIME,
    accesoCom_tarea ENUM('SI', 'NO') NOT NULL DEFAULT 'SI',
    FOREIGN KEY (fk_grupo) REFERENCES GRUPOS (id_grupo) ON DELETE CASCADE
);

CREATE TABLE COM_TAREA (
    id_comTarea INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_tarea INT NOT NULL,
    fk_miembro INT NOT NULL,
    texto_comTarea VARCHAR(200) NOT NULL,
    archivo_comTarea VARCHAR(1000),
    fechaHora_comTarea TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_tarea) REFERENCES TAREAS (id_tarea) ON DELETE CASCADE,
    FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro) ON DELETE CASCADE
);

INSERT INTO PROFESORES (numDocumento_profesor, nombre_profesor, apellido_profesor)
VALUES
(123456789, 'Juan', 'Pérez'),
(987654321, 'María', 'García'),
(456789123, 'Pedro', 'López'),
(789123456, 'Ana', 'Martínez'),
(321654987, 'Luis', 'Rodríguez'),
(654987321, 'Laura', 'Sánchez'),
(111222333, 'Carlos', 'Gómez'),
(444555666, 'Sofía', 'Hernández'),
(777888999, 'Javier', 'Díaz'),
(999888777, 'Elena', 'Fernández'),
(666555444, 'Miguel', 'Ruiz'),
(333222111, 'Carmen', 'Torres'),
(222333444, 'Alberto', 'Vega'),
(555444333, 'Isabel', 'Jiménez'),
(888999000, 'Francisco', 'Molina'),
(333666999, 'Antonia', 'Santos'),
(666999333, 'Roberto', 'Ramírez'),
(111444777, 'Paula', 'Iglesias'),
(444777111, 'Diego', 'Navarro'),
(777111444, 'Lucía', 'Ortega'),
(888111222, 'Alejandro', 'Gutiérrez'),
(111888222, 'Raquel', 'Cabrera'),
(888222111, 'Gonzalo', 'Reyes'),
(222111888, 'Beatriz', 'Pérez'),
(555777999, 'Pablo', 'Herrera');

INSERT INTO GRADOS (num_grado, numGrupo_grado)
VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(3, 3),
(4, 1),
(4, 2),
(5, 1),
(5, 2),
(6, 1),
(6, 2),
(6, 3),
(7, 1),
(7, 2),
(8, 1),
(8, 2),
(9, 1),
(9, 2),
(10, 1),
(10, 2),
(11, 1),
(11, 2),
(12, 1);

INSERT INTO ESTUDIANTES (id_estudiante, numMatricula_estudiante, numDocumento_estudiante, nombre_estudiante, apellido_estudiante, fk_grado)
VALUES
(1, 1001, 111111112, 'José', 'Gómez', 1),
(2, 1002, 222222221, 'María', 'Rodríguez', 1),
(3, 1003, 333333332, 'Carlos', 'Fernández', 2),
(4, 1004, 444444443, 'Laura', 'López', 2),
(5, 1005, 555555554, 'Daniel', 'Martínez', 3),
(6, 1006, 666666665, 'Ana', 'Sánchez', 3),
(7, 1007, 777777776, 'Pablo', 'Pérez', 4),
(8, 1008, 888888887, 'Sofía', 'García', 4),
(9, 1009, 999999998, 'Alejandro', 'Martín', 5),
(10, 1010, 101010109, 'Lucía', 'Hernández', 5),
(11, 1011, 111111110, 'Diego', 'Gutiérrez', 6),
(12, 1012, 121212122, 'Carmen', 'Díaz', 6),
(13, 1013, 131313133, 'Javier', 'Ruiz', 7),
(14, 1014, 141414144, 'Elena', 'Torres', 7),
(15, 1015, 151515155, 'Marcos', 'Santos', 8),
(16, 1016, 161616166, 'Isabel', 'Jiménez', 8),
(17, 1017, 171717177, 'Gabriel', 'Ortega', 9),
(18, 1018, 181818188, 'Ana', 'Navarro', 9),
(19, 1019, 191919199, 'Hugo', 'Iglesias', 10),
(20, 1020, 202020200, 'Clara', 'Cabrera', 10),
(21, 1021, 212121213, 'Fernando', 'Reyes', 11),
(22, 1022, 222222224, 'Adriana', 'Pérez', 11),
(23, 1023, 232323235, 'Martín', 'Herrera', 12),
(24, 1024, 242424246, 'Sara', 'Molina', 12),
(25, 1025, 252525257, 'Andrés', 'Gómez', 1);

INSERT INTO MIEMBROS (tipo_miembro, fk_profesor, fk_estudiante) VALUES
('Profesor', 1, NULL),
('Profesor', 2, NULL),
('Profesor', 3, NULL),
('Profesor', 4, NULL),
('Profesor', 5, NULL),
('Profesor', 6, NULL),
('Profesor', 7, NULL),
('Profesor', 8, NULL),
('Profesor', 9, NULL),
('Profesor', 10, NULL),
('Estudiante', NULL, 1),
('Estudiante', NULL, 2),
('Estudiante', NULL, 3),
('Estudiante', NULL, 4),
('Estudiante', NULL, 5),
('Estudiante', NULL, 6),
('Estudiante', NULL, 7),
('Estudiante', NULL, 8),
('Estudiante', NULL, 9),
('Estudiante', NULL, 10),
('Estudiante', NULL, 11),
('Estudiante', NULL, 12),
('Estudiante', NULL, 13),
('Estudiante', NULL, 14),
('Estudiante', NULL, 15),
('Estudiante', NULL, 16);

INSERT INTO AMIGOS (fk_miembro1, fk_miembro2)
VALUES
(1, 16),
(2, 17),
(3, 18),
(4, 19),
(5, 20),
(6, 21),
(7, 22),
(8, 23),
(9, 24),
(10, 25),
(11, 16),
(12, 17),
(13, 18),
(14, 19),
(15, 20),
(1, 17),
(2, 18),
(3, 19),
(4, 20),
(5, 21),
(6, 22),
(7, 23),
(8, 24),
(9, 25),
(10, 16);

INSERT INTO MENSAJES (fk_miembro1, fk_miembro2, contenido_mensaje)
VALUES
(1, 16, 'Hola, ¿cómo estás?'),
(2, 17, 'Buenos días.'),
(3, 18, '¿Ya terminaste la tarea?'),
(4, 19, '¿Quieres salir esta tarde?'),
(5, 20, 'Feliz cumpleaños.'),
(6, 21, '¿Viste el partido anoche?'),
(7, 22, 'Necesito tu ayuda con el proyecto.'),
(8, 23, '¿A qué hora es la reunión?'),
(9, 24, '¡Felicitaciones por tu logro!'),
(10, 25, 'Nos vemos mañana.'),
(11, 16, 'Hola de nuevo.'),
(12, 17, '¿Te interesa participar en el evento?'),
(13, 18, '¿Cómo va todo?'),
(14, 19, '¿Tienes algún plan para el fin de semana?'),
(15, 20, '¡Buen trabajo en la presentación!'),
(1, 17, '¿Qué opinas sobre el tema?'),
(2, 18, 'Necesito algunos consejos.'),
(3, 19, 'Gracias por tu ayuda.'),
(4, 20, '¿Dónde nos encontramos?'),
(5, 21, '¡Hasta luego!'),
(6, 22, '¡Nos vemos pronto!'),
(7, 23, '¿Cómo te fue en el examen?'),
(8, 24, '¿Qué tal tu día?'),
(9, 25, '¿Quieres estudiar juntos?'),
(10, 16, 'Buen día.');

INSERT INTO PUBLICACIONES (fk_miembro, texto_publicacion, archivo_publicacion, imagen_publicacion)
VALUES
(1, 'Esta es mi primera publicación.', NULL, NULL),
(2, 'Estoy muy contento con el progreso de mis estudiantes.', NULL, NULL),
(3, 'Aquí hay un enlace interesante para ustedes.', NULL, NULL),
(4, '¡Feliz viernes a todos!', NULL, NULL),
(5, 'Recuerden la tarea para mañana.', NULL, NULL),
(6, 'Compartiendo un recurso útil para el proyecto.', NULL, NULL),
(7, '¿Qué opinan sobre la nueva asignatura?', NULL, NULL),
(8, 'Fotos del último evento.', NULL, '/static/archivos_subidos/miembros/imgs/publicaciones/evento.jpg'),
(9, '¡Gran trabajo en equipo!', NULL, NULL),
(10, 'Recordatorio: reunión a las 3 PM.', NULL, NULL),
(11, 'Novedades sobre la clase de la próxima semana.', NULL, NULL),
(12, 'Felicitaciones a todos los estudiantes.', NULL, NULL),
(13, 'Aquí hay algunas notas adicionales.', NULL, NULL),
(14, 'Información sobre el examen final.', NULL, NULL),
(15, 'Gracias por su participación en la encuesta.', NULL, NULL),
(16, 'Ideas para mejorar nuestra clase.', NULL, NULL),
(17, 'Anuncios importantes sobre el curso.', NULL, NULL),
(18, 'Material complementario para el tema de hoy.', NULL, NULL),
(19, 'Reflexiones sobre la clase de hoy.', NULL, NULL),
(20, '¡Buen trabajo a todos!', NULL, NULL),
(21, 'Recursos adicionales para estudiar.', NULL, NULL),
(22, 'Información sobre el próximo proyecto.', NULL, NULL),
(23, 'Gracias por sus comentarios.', NULL, NULL),
(24, 'Un saludo a todos mis estudiantes.', NULL, NULL),
(25, 'Aquí hay un artículo interesante.', NULL, NULL);

INSERT INTO COM_PUBLICACION (fk_publicacion, fk_miembro, texto_comPublicacion, archivo_comPublicacion)
VALUES
(1, 16, '¡Qué buena noticia!', NULL),
(2, 17, 'Gracias por la información.', NULL),
(3, 18, 'Muy interesante, gracias por compartir.', NULL),
(4, 19, '¡Feliz viernes!', NULL),
(5, 20, 'Entendido, trabajaré en ello.', NULL),
(6, 21, 'Gracias por el recurso.', NULL),
(7, 22, 'Me parece una buena asignatura.', NULL),
(8, 23, 'Las fotos están geniales.', NULL),
(9, 24, 'Buen trabajo a todos.', NULL),
(10, 25, 'Nos vemos en la reunión.', NULL),
(11, 16, 'Esperando las novedades.', NULL),
(12, 17, 'Felicitaciones a todos.', NULL),
(13, 18, 'Gracias por las notas adicionales.', NULL),
(14, 19, 'Tomaré nota para el examen.', NULL),
(15, 20, 'De nada, fue un placer participar.', NULL),
(16, 21, 'Aquí van algunas ideas.', NULL),
(17, 22, 'Gracias por los anuncios.', NULL),
(18, 23, 'Gracias por el material complementario.', NULL),
(19, 24, 'Reflexionando sobre la clase.', NULL),
(20, 25, 'Buen trabajo, equipo.', NULL),
(21, 16, 'Gracias por los recursos.', NULL),
(22, 17, 'Empezaré a trabajar en el proyecto.', NULL),
(23, 18, 'De nada, gracias a ti.', NULL),
(24, 19, 'Un saludo para ti también.', NULL),
(25, 20, 'Leeré el artículo.', NULL);

INSERT INTO ASIGNATURAS (nombre_asignatura)
VALUES
('Matemáticas'),
('Lengua Española'),
('Ciencias Naturales'),
('Historia'),
('Geografía'),
('Inglés'),
('Educación Física'),
('Arte'),
('Música'),
('Tecnología'),
('Filosofía'),
('Biología'),
('Química'),
('Física'),
('Literatura'),
('Economía'),
('Psicología'),
('Sociología'),
('Educación Cívica'),
('Informática'),
('Religión'),
('Teatro'),
('Dibujo Técnico'),
('Fotografía'),
('Astronomía');

INSERT INTO GRUPOS (fk_profesor, fk_grado, descripcion_grupo, fk_asignatura)
VALUES
(1, 1, 'Grupo de Matemáticas avanzado', 1),
(2, 1, 'Lengua Española nivel básico', 2),
(3, 2, 'Ciencias Naturales y biología', 3),
(4, 2, 'Historia moderna', 4),
(5, 3, 'Geografía y mapas', 5),
(6, 3, 'Inglés intermedio', 6),
(7, 4, 'Educación Física y deportes', 7),
(8, 4, 'Arte y creatividad', 8),
(9, 5, 'Música y teoría musical', 9),
(10, 5, 'Tecnología y programación', 10),
(11, 6, 'Filosofía y ética', 11),
(12, 6, 'Biología aplicada', 12),
(13, 7, 'Química y experimentos', 13),
(14, 7, 'Física y mecánica', 14),
(15, 8, 'Literatura y lectura crítica', 15),
(16, 8, 'Economía y finanzas', 16),
(17, 9, 'Psicología y comportamiento', 17),
(18, 9, 'Sociología y cultura', 18),
(19, 10, 'Educación Cívica y ciudadanía', 19),
(20, 10, 'Informática y diseño gráfico', 20),
(21, 11, 'Religión y filosofía', 21),
(22, 11, 'Teatro y expresión dramática', 22),
(23, 12, 'Dibujo Técnico y diseño', 23),
(24, 12, 'Fotografía y edición', 24),
(25, 1, 'Astronomía y exploración espacial', 25);

INSERT INTO INTEGRANTES (fk_estudiante, fk_grupo)
VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 4),
(8, 4),
(9, 5),
(10, 5),
(11, 6),
(12, 6),
(13, 7),
(14, 7),
(15, 8),
(16, 8),
(17, 9),
(18, 9),
(19, 10),
(20, 10),
(21, 11),
(22, 11),
(23, 12),
(24, 12),
(25, 1);

INSERT INTO TAREAS (fk_grupo, titulo_tarea, descripcion_tarea, archivo_tarea, fechaHoraVen_tarea, accesoCom_tarea)
VALUES
(1, 'Tarea 1', 'Descripción de la tarea 1', NULL, '2024-07-30 23:59:59', 'SI'),
(2, 'Tarea 2', 'Descripción de la tarea 2', NULL, '2024-07-31 23:59:59', 'SI'),
(3, 'Tarea 3', 'Descripción de la tarea 3', NULL, '2024-08-01 23:59:59', 'NO'),
(4, 'Tarea 4', 'Descripción de la tarea 4', NULL, '2024-08-02 23:59:59', 'SI'),
(5, 'Tarea 5', 'Descripción de la tarea 5', NULL, '2024-08-03 23:59:59', 'NO'),
(6, 'Tarea 6', 'Descripción de la tarea 6', NULL, '2024-08-04 23:59:59', 'SI'),
(7, 'Tarea 7', 'Descripción de la tarea 7', NULL, '2024-08-05 23:59:59', 'SI'),
(8, 'Tarea 8', 'Descripción de la tarea 8', NULL, '2024-08-06 23:59:59', 'NO'),
(9, 'Tarea 9', 'Descripción de la tarea 9', NULL, '2024-08-07 23:59:59', 'SI'),
(10, 'Tarea 10', 'Descripción de la tarea 10', NULL, '2024-08-08 23:59:59', 'NO'),
(11, 'Tarea 11', 'Descripción de la tarea 11', NULL, '2024-08-09 23:59:59', 'SI'),
(12, 'Tarea 12', 'Descripción de la tarea 12', NULL, '2024-08-10 23:59:59', 'SI'),
(13, 'Tarea 13', 'Descripción de la tarea 13', NULL, '2024-08-11 23:59:59', 'NO'),
(14, 'Tarea 14', 'Descripción de la tarea 14', NULL, '2024-08-12 23:59:59', 'SI'),
(15, 'Tarea 15', 'Descripción de la tarea 15', NULL, '2024-08-13 23:59:59', 'NO'),
(16, 'Tarea 16', 'Descripción de la tarea 16', NULL, '2024-08-14 23:59:59', 'SI'),
(17, 'Tarea 17', 'Descripción de la tarea 17', NULL, '2024-08-15 23:59:59', 'SI'),
(18, 'Tarea 18', 'Descripción de la tarea 18', NULL, '2024-08-16 23:59:59', 'NO'),
(19, 'Tarea 19', 'Descripción de la tarea 19', NULL, '2024-08-17 23:59:59', 'SI'),
(20, 'Tarea 20', 'Descripción de la tarea 20', NULL, '2024-08-18 23:59:59', 'NO'),
(21, 'Tarea 21', 'Descripción de la tarea 21', NULL, '2024-08-19 23:59:59', 'SI'),
(22, 'Tarea 22', 'Descripción de la tarea 22', NULL, '2024-08-20 23:59:59', 'SI'),
(23, 'Tarea 23', 'Descripción de la tarea 23', NULL, '2024-08-21 23:59:59', 'NO'),
(24, 'Tarea 24', 'Descripción de la tarea 24', NULL, '2024-08-22 23:59:59', 'SI'),
(25, 'Tarea 25', 'Descripción de la tarea 25', NULL, '2024-08-23 23:59:59', 'NO');

INSERT INTO COM_TAREA (fk_tarea, fk_miembro, texto_comTarea, archivo_comTarea)
VALUES
(1, 16, 'Completé la tarea y la subí.', NULL),
(2, 17, 'Tengo algunas dudas sobre esta tarea.', NULL),
(3, 18, 'Entiendo la tarea, pero necesito ayuda con algunos puntos.', NULL),
(4, 19, 'La tarea está casi lista, solo me falta un detalle.', NULL),
(5, 20, 'He enviado la tarea por correo.', NULL),
(6, 21, '¿Podrías revisar mi tarea y darme feedback?', NULL),
(7, 22, 'La tarea se hizo siguiendo las indicaciones.', NULL),
(8, 23, 'Subí la tarea al sistema.', NULL),
(9, 24, 'Estoy trabajando en la tarea, pero me llevará un poco más de tiempo.', NULL),
(10, 25, 'La tarea está en progreso, espero terminarla pronto.', NULL),
(11, 16, 'Tuve algunos problemas con la tarea, pero ya está casi lista.', NULL),
(12, 17, '¿Qué opinas de mi enfoque para esta tarea?', NULL),
(13, 18, 'Subí la tarea y envié una copia al profesor.', NULL),
(14, 19, 'La tarea fue difícil, pero logré completarla.', NULL),
(15, 20, 'Estoy revisando la tarea antes de entregarla.', NULL),
(16, 21, 'Por favor, revisa el archivo que te envié.', NULL),
(17, 22, '¿Te parece bien el resultado de la tarea?', NULL),
(18, 23, 'Revisé y corregí algunos errores en la tarea.', NULL),
(19, 24, 'Envié la tarea con un par de horas de antelación.', NULL),
(20, 25, 'La tarea está lista, solo falta un pequeño ajuste.', NULL),
(21, 16, 'Subí una versión corregida de la tarea.', NULL),
(22, 17, 'Tuve que rehacer parte de la tarea, pero ya está completa.', NULL),
(23, 18, 'Revisé todos los puntos de la tarea y la entregué.', NULL),
(24, 19, 'La tarea fue entregada a tiempo.', NULL),
(25, 20, '¿Puedes confirmar si recibiste mi tarea?', NULL);


/*INSERT INTO*/
INSERT INTO indenetwork.asignaturas (id_asignatura, nombre_asignatura) VALUES (9999, 'Fisica Matematica');
INSERT INTO indenetwork.profesores (id_profesor, numDocumento_profesor, nombre_profesor, apellido_profesor) VALUES (9999, 1938475, 'Maicol', 'Moreno');
INSERT INTO indenetwork.miembros (id_miembro, tipo_miembro, fk_profesor) VALUES (9999, 'Profesor', 9999);

/*UPDATE*/
UPDATE indenetwork.asignaturas SET nombre_asignatura = 'Física' WHERE id_asignatura = 9999;
UPDATE indenetwork.profesores SET nombre_profesor = 'Smith' WHERE id_profesor = 9999;
UPDATE indenetwork.miembros SET tipo_miembro = 'Estudiante' WHERE id_miembro = 9999;

/*SELECT*/
SELECT nombre_profesor, apellido_profesor FROM indenetwork.profesores WHERE id_profesor = 9999;
SELECT nombre_asignatura FROM indenetwork.asignaturas WHERE id_asignatura = 9999;
SELECT tipo_miembro, fk_profesor FROM indenetwork.miembros WHERE id_miembro = 9999;

/*DELETE*/
DELETE FROM indenetwork.miembros WHERE id_miembro = 9999;
DELETE FROM indenetwork.asignaturas WHERE id_asignatura = 9999;
DELETE FROM indenetwork.profesores WHERE id_profesor = 9999;

#Dame 3 consultas sql con el operador de multiplicacion

/*MULTIPLICACION*/
SELECT COUNT(*) * 2 FROM indenetwork.miembros;
SELECT AVG(id_miembro) * 2 FROM indenetwork.miembros;

/*RESTA*/
SELECT id_miembro - 5 FROM indenetwork.miembros LIMIT 5;
SELECT id_tarea - 10 FROM indenetwork.tareas LIMIT 5;
SELECT fk_miembro1 - 2 FROM indenetwork.mensajes LIMIT 5;

/*SUMA*/
SELECT id_miembro + 5 FROM indenetwork.miembros LIMIT 5;
SELECT id_tarea + 10 FROM indenetwork.tareas LIMIT 5;
SELECT fk_miembro1 + 2 FROM indenetwork.mensajes LIMIT 5;

/*SUM*/
SELECT SUM(id_miembro) FROM indenetwork.miembros;
SELECT SUM(id_tarea) FROM indenetwork.tareas;
SELECT SUM(fk_miembro1) FROM indenetwork.mensajes;

/*SELECT*/
SELECT COUNT(*) / 2 FROM indenetwork.miembros;
SELECT AVG(id_miembro) / 2 FROM indenetwork.miembros;
SELECT id_miembro / 2 FROM indenetwork.miembros;

/*COUNT*/
SELECT COUNT(*) FROM indenetwork.miembros WHERE tipo_miembro = 'Profesor';
SELECT COUNT(*) FROM indenetwork.miembros WHERE tipo_miembro = 'Estudiante';
SELECT COUNT(fk_miembro1) FROM indenetwork.mensajes;

/*AVG o PROMEDIO*/
SELECT AVG(id_miembro) FROM indenetwork.miembros;
SELECT AVG(id_tarea) FROM indenetwork.tareas;
SELECT AVG(id_miembro) FROM indenetwork.miembros WHERE tipo_miembro = 'Estudiante';

/*MIN*/
SELECT MIN(id_miembro) FROM indenetwork.miembros;
SELECT MIN(id_tarea) FROM indenetwork.tareas;
SELECT MIN(id_miembro) FROM indenetwork.miembros WHERE tipo_miembro = 'Estudiante';

/*MAX*/
SELECT MAX(id_miembro) FROM indenetwork.miembros;
SELECT MAX(id_tarea) FROM indenetwork.tareas;
SELECT MAX(id_miembro) FROM indenetwork.miembros WHERE tipo_miembro = 'Estudiante';