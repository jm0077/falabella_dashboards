CREATE TABLE `banco` (
   `id` int NOT NULL AUTO_INCREMENT,
   `nombre` varchar(255) NOT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `nombre` (`nombre`)
 ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci