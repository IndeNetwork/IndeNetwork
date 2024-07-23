CREATE DATABASE IndeNetwork;

CREATE TABLE PROFESORES (
    id_profesor INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    numDocumento_profesor INT(12) UNIQUE NOT NULL,
    nombre_profesor CHAR(50) NOT NULL,
    apellido_profesor CHAR(50) NOT NULL,
    foto_profesor VARCHAR(1000) NOT NULL DEFAULT ‘/static/archivos_subidos/miembros/imgs/perfiles/imagenDefault.png’
);

CREATE TABLE GRADOS (
	id_grado INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	num_grado INT NOT NULL,
	numGrupo_grado INT NOT NULL,
	UNIQUE (num_grado,numGrupo_grado)
);

CREATE TABLE ESTUDIANTES (
    id_estudiante INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    numMatricula_estudiante INT(12) UNIQUE NOT NULL,
    numDocumento_estudiante INT(12) UNIQUE NOT NULL,
    nombre_estudiante CHAR(50) NOT NULL,
    apellido_estudiante CHAR(50) NOT NULL,
    fk_grado INT NOT NULL,
    foto_estudiante VARCHAR(1000) NOT NULL DEFAULT ‘/static/archivos_subidos/miembros/imgs/perfiles/imagenDefault.png’,
    FOREIGN KEY (fk_grado) REFERENCES GRADOS (id_grado)
);

CREATE TABLE MIEMBROS (
    id_miembro INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    tipo_miembro ENUM('Profesor','Estudiante') NOT NULL,
    fk_tipoMiembro INT NOT NULL UNIQUE,
    FOREIGN KEY (fk_tipoMiembro) REFERENCES ESTUDIANTES (id_estudiante),
    FOREIGN KEY (fk_tipoMiembro) REFERENCES PROFESORES (id_profesor)
);	

CREATE TABLE AMIGOS (
	id_amigo INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro1 INT NOT NULL,
    fk_miembro2 INT NOT NULL,	
    fechaHora_amigo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro1) REFERENCES MIEMBROS (id_miembro),
    FOREIGN KEY (fk_miembro2) REFERENCES MIEMBROS (id_miembro)
);
	
CREATE TABLE MENSAJES (
	id_mensaje INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro1 INT NOT NULL,
    fk_miembro2 INT NOT NULL,
	contenido_mensaje VARCHAR(200) NOT NULL,
    fechaHora_mensaje TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro1) REFERENCES MIEMBROS (id_miembro),
    FOREIGN KEY (fk_miembro2) REFERENCES MIEMBROS (id_miembro)
);

CREATE TABLE PUBLICACIONES (
    id_publicacion INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_miembro INT NOT NULL,
    texto_publicacion VARCHAR(200) NOT NULL,
    archivo_publicacion VARCHAR(1000),
    imagen_publicacion VARCHAR(1000),
    fechaHora_publicacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro)
);
CREATE TABLE COM_PUBLICACION (
    id_comPublicacion INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_publicacion INT NOT NULL,
    fk_miembro INT NOT NULL,
    texto_comPublicacion VARCHAR(200) NOT NULL,
    archivo_comPublicacion VARCHAR(1000),
    fechaHora_comPublicacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_publicacion) REFERENCES PUBLICACIONES (id_publicacion),
    FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro)
);

CREATE TABLE ASIGNATURAS (
    id_asignatura INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_asignatura CHAR(50) NOT NULL
);

CREATE TABLE GRUPOS (
	id_grupo INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_profesor INT NOT NULL,
    fk_grado INT NOT NULL,
    descripción_grupo VARCHAR(200) NOT NULL,
    fk_asignatura INT NOT NULL,
    fechaHora_grupo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_miembro) REFERENCES PROFESORES (id_profesor),
    FOREIGN KEY (fk_grado) REFERENCES GRADOS (id_grado),
    FOREIGN KEY (fk_asignatura) REFERENCES ASIGNATURAS (id_asignatura)
);
CREATE TABLE INTEGRANTES (
    id_integrante INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	fk_estudiante INT NOT NULL,
	fk_grupo INT NOT NULL,
	FOREIGN KEY (fk_miembro) REFERENCES ESTUDIANTES (id_estudiante),
	FOREIGN KEY (fk_grado) REFERENCES GRUPO (id_grupo)
);

CREATE TABLE TAREAS (
	id_tarea INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    fk_grupo INT NOT NULL,
	titulo_tarea VARCHAR(50) NOT NULL,
	descripcion_tarea VARCHAR(500) NOT NULL,
	archivo_tarea VARCHAR(1000),
    fechaHora_tarea TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	fechaHoraVen_tarea DATETIME,
    accesoCom_tarea ENUM(“SI”,”NO”) NOT NULL DEFAULT ‘SI’,
    FOREIGN KEY (fk_grupo) REFERENCES GRUPOS (id_grupo)
);

CREATE TABLE COM_TAREA (
    id_comTarea INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	fk_tarea INT NOT NULL,
	fk_miembro INT NOT NULL,
	texto_comTarea VARCHAR(200) NOT NULL,
	archivo_comTarea VARCHAR(1000),
    fechaHora_comTarea TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (fk_tarea) REFERENCES TAREAS (id_tarea),
	FOREIGN KEY (fk_miembro) REFERENCES MIEMBROS (id_miembro)
);
