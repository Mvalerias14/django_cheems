-- Esquema de la base de datos del proyecto.
-- Ejecutar en una base vacía (el nombre da igual, pero debe coincidir
-- con tu variable de entorno DB_NAME).
--
-- Si tu base ya tiene las tablas, solo falta la columna "action":
--   ALTER TABLE work_order_history ADD COLUMN action VARCHAR(200) NULL;
--
-- Valores numéricos que usa la aplicación:
--   user.profile        1 = Administrador, 2 = Operador
--   work_order.status   1 = Pendiente, 2 = En proceso, 3 = Terminada, 4 = Cancelada
--   log.module          1 = Usuarios, 2 = Órdenes

CREATE TABLE IF NOT EXISTS `user` (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NULL,
    account VARCHAR(100) NULL,
    password VARCHAR(255) NULL,
    profile INT NULL
);

CREATE TABLE IF NOT EXISTS work_order (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tittle VARCHAR(70) NULL,
    description TEXT NULL,
    status INT NULL
);

CREATE TABLE IF NOT EXISTS work_order_history (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NULL,
    id_user INT NULL,
    module INT NULL,
    id_work_order INT NULL,
    action VARCHAR(200) NULL
);

CREATE TABLE IF NOT EXISTS log (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NULL,
    description VARCHAR(155) NULL,
    id_user INT NULL,
    module INT NULL
);