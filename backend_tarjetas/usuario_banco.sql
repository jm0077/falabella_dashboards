CREATE TABLE `usuario_banco` (
   `id` int NOT NULL AUTO_INCREMENT,
   `userId` varchar(36) DEFAULT NULL,
   `banco_id` int DEFAULT NULL,
   `habilitado` tinyint(1) DEFAULT '0',
   PRIMARY KEY (`id`),
   KEY `idx_banco_id` (`banco_id`),
   KEY `idx_user_id` (`userId`),
   CONSTRAINT `usuario_banco_ibfk_1` FOREIGN KEY (`banco_id`) REFERENCES `banco` (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci