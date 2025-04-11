-- MySQL dump 10.13  Distrib 8.0.41, for macos15.2 (arm64)
--
-- Host: localhost    Database: Semanarios
-- ------------------------------------------------------
-- Server version	8.0.41
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'Semanarios'
--
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `carreras_corridas`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos WHERE idCaballo = id_caballo AND corrio = 1 AND puesto <> 99;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `carreras_ganadas`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos WHERE idCaballo = id_caballo AND corrio = 1 AND puesto = 1;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `centesimos_a_cadena`(tiempo_centesimos INT) RETURNS varchar(10) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
    DECLARE minutos INT;
    DECLARE segundos INT;
    DECLARE centesimos INT;
    DECLARE resultado VARCHAR(10);

    
    SET minutos = tiempo_centesimos DIV 6000;
    SET segundos = (tiempo_centesimos MOD 6000) DIV 100;
    SET centesimos = tiempo_centesimos MOD 100;

    
    SET resultado = CONCAT(minutos, '\'', LPAD(segundos, 2, '0'), '"', LPAD(centesimos, 2, '0'));

    RETURN resultado;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_con_el_jinete`(id_caballo INT, id_jinete INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos WHERE idCaballo = id_caballo AND idJinete = id_jinete AND corrio = 1;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_en_arena`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.pista = 'A' AND corrio = 1;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_en_cesped`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.pista = 'C' AND corrio = 1;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_en_la_distancia`(id_caballo INT, distancia INT, pista CHAR(1)) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.distancia = distancia AND rcar.pista = pista AND corrio = 1 AND rcab.puesto <> 99;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_jinete`(id_jinete INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE corridas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO corridas 
    FROM ReunionCaballos
    WHERE idJinete = id_jinete
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    RETURN (corridas);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_preparador`(id_preparador INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE corridas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO corridas 
    FROM ReunionCaballos
    WHERE idPreparador = id_preparador
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    RETURN corridas;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corridas_prep_jin`(id_preparador INT, id_jinete INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE corridas INT;
		DECLARE fecha_inicio DATE;
		SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;
		SELECT COUNT(*) INTO corridas FROM ReunionCaballos 
		WHERE idPreparador = id_preparador 
		AND idJinete = id_jinete 
		AND puesto > 0 
		AND corrio = 1
		AND fecha >= fecha_inicio AND fecha < fecha_hasta;
		RETURN (corridas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `corrieron`(fec DATE, refe INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE cor INT;
	SELECT COUNT(*) INTO cor FROM ReunionCaballos
	WHERE fecha = fec AND referencia = refe AND puesto > 0 AND corrio = 1;
	RETURN (cor);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `cuarto`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE cuarto VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO cuarto from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 4 limit 1;
    RETURN(cuarto);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `dividendoGanador`(fec DATE, refe INT, id_caballo INT) RETURNS decimal(7,2)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE dividendo DECIMAL(7,2);
	DECLARE total DECIMAL(7,2);
	DECLARE boletos DECIMAL(7,2); 
	SELECT totalBoletos INTO total from ReunionCarreras reucar 
		where reucar.fecha = fec and reucar.referencia = refe;
	select boletosReales INTO boletos from ReunionCaballos reucab WHERE reucab.fecha = fec and reucab.referencia = refe and reucab.idCaballo = id_caballo;
	if boletos = 0 then
		set dividendo = 0;
	else
		SET dividendo = (total * 0.74)/ boletos * 3;
	end if;
    RETURN(dividendo);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `efectividad_jinete`(id_jinete INT, fecha_hasta DATE) RETURNS float
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE ganadas INT;
    DECLARE corridas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO ganadas 
    FROM ReunionCaballos
    WHERE idJinete = id_jinete
    AND puesto = 1
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    
    SELECT COUNT(*) INTO corridas 
    FROM ReunionCaballos
    WHERE idJinete = id_jinete
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    
    IF corridas = 0 THEN
        RETURN 0;
    END IF;

    
    RETURN (ganadas / corridas) * 100;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `efectividad_preparador`(id_preparador INT, fecha_hasta DATE) RETURNS float
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE ganadas INT;
    DECLARE corridas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO ganadas 
    FROM ReunionCaballos
    WHERE idPreparador = id_preparador
    AND puesto = 1
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    
    SELECT COUNT(*) INTO corridas 
    FROM ReunionCaballos
    WHERE idPreparador = id_preparador
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    
    IF corridas = 0 THEN
        RETURN 0;
    END IF;

    
    RETURN (ganadas / corridas) * 100;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `f_marcador`(fec DATE, refe INT, pto INT) RETURNS varchar(255) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE v_ganadores VARCHAR(255) DEFAULT '';
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_idCaballo INT;
    DECLARE v_nombre VARCHAR(30);
    DECLARE v_kilos INT;
    
    DECLARE cur_ganadores CURSOR FOR 
        SELECT cab.idCaballo, cab.breve, reucab.kilos 
        FROM ReunionCaballos reucab
        JOIN Caballos cab ON cab.idCaballo = reucab.idCaballo
        WHERE reucab.fecha = fec AND reucab.referencia = refe AND reucab.puesto = pto;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur_ganadores;
    
    read_loop: LOOP
        FETCH cur_ganadores INTO v_idCaballo, v_nombre, v_kilos;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET v_ganadores = CONCAT(v_ganadores, IF(LENGTH(v_ganadores) > 0, '; ', ''), v_idCaballo, ',', v_nombre, ',', v_kilos);
    END LOOP;
    
    CLOSE cur_ganadores;
    
    RETURN v_ganadores;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_con_el_jinete`(id_caballo INT, id_jinete INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos WHERE idCaballo = id_caballo AND idJinete = id_jinete AND puesto = 1;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_en_arena`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.pista = 'A' AND corrio = 1 AND puesto = 1;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_en_cesped`(id_caballo INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.pista = 'C' AND corrio = 1 AND puesto = 1;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_en_la_distancia`(id_caballo INT, distancia INT, pista CHAR(1)) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos rcab 
			RIGHT JOIN ReunionCarreras rcar ON rcar.fecha = rcab.fecha AND rcar.referencia = rcab.referencia 
			WHERE rcab.idCaballo = id_caballo AND rcar.distancia = distancia AND rcar.pista = pista AND corrio = 1 AND puesto = 1;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_jinete`(id_jinete INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE ganadas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO ganadas 
    FROM ReunionCaballos
    WHERE idJinete = id_jinete
    AND puesto = 1
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    RETURN (ganadas);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_preparador`(id_preparador INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE ganadas INT;
    DECLARE fecha_inicio DATE;

    
    SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;

    
    SELECT COUNT(*) INTO ganadas 
    FROM ReunionCaballos
    WHERE idPreparador = id_preparador
    AND puesto = 1
    AND corrio = 1
    AND fecha >= fecha_inicio AND fecha < fecha_hasta;

    RETURN ganadas;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadas_prep_jin`(id_preparador INT, id_jinete INT, fecha_hasta DATE) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN	
		DECLARE ganadas INT;
		DECLARE fecha_inicio DATE;
		SELECT inicioTemporada INTO fecha_inicio FROM fechasSemana LIMIT 1;
		SELECT COUNT(*) INTO ganadas FROM ReunionCaballos 
		WHERE idPreparador = id_preparador 
		AND idJinete = id_jinete 
		AND puesto = 1 
		AND corrio = 1
		AND fecha >= fecha_inicio AND fecha < fecha_hasta;
		RETURN (ganadas);
	END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganador`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE ganador VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO ganador from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 1 limit 1;
    RETURN(ganador);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadores`(fec DATE, refe INT) RETURNS varchar(255) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE v_ganadores VARCHAR(255) DEFAULT '';
    DECLARE finalizado INT DEFAULT 0;
    DECLARE ganadorCur CURSOR FOR 
        SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos)
        FROM ReunionCaballos reucab
        JOIN Caballos cab ON cab.idCaballo = reucab.idCaballo
        WHERE reucab.fecha = fec AND reucab.referencia = refe AND reucab.puesto = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finalizado = 1;

    OPEN ganadorCur;

    bucle: LOOP
        FETCH ganadorCur INTO v_ganadores;
        IF finalizado = 1 THEN 
            LEAVE bucle;
        END IF;
        
        IF LENGTH(v_ganadores) > 0 THEN
            SET v_ganadores = CONCAT(v_ganadores, '; ');
        END IF;
        
        SET v_ganadores = CONCAT(v_ganadores, ganador);
    END LOOP;

    CLOSE ganadorCur;

    RETURN v_ganadores;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `ganadores_empates`(fec DATE, refe INT) RETURNS varchar(255) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE v_ganadores VARCHAR(255) DEFAULT '';
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_idCaballo INT;
    DECLARE v_nombre VARCHAR(30);
    DECLARE v_kilos INT;
    
    DECLARE cur_ganadores CURSOR FOR 
        SELECT cab.idCaballo, cab.breve, reucab.kilos 
        FROM ReunionCaballos reucab
        JOIN Caballos cab ON cab.idCaballo = reucab.idCaballo
        WHERE reucab.fecha = fec AND reucab.referencia = refe AND reucab.puesto = 4;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur_ganadores;
    
    read_loop: LOOP
        FETCH cur_ganadores INTO v_idCaballo, v_nombre, v_kilos;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET v_ganadores = CONCAT(v_ganadores, IF(LENGTH(v_ganadores) > 0, '; ', ''), v_idCaballo, ',', v_nombre, ',', v_kilos);
    END LOOP;
    
    CLOSE cur_ganadores;
    
    RETURN v_ganadores;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `gano_siguiente`(fec DATE, id INT) RETURNS tinyint(1)
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE pto INT;
    SELECT puesto INTO pto
    FROM ReunionCaballos
    WHERE fecha >= fec AND corrio = 1 and puesto <> 99 and idCaballo = id
    ORDER BY fecha
    LIMIT 1, 1;
    IF pto = 1 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `getEstilo`(id VARCHAR(100)) RETURNS varchar(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci
    DETERMINISTIC
BEGIN
    DECLARE nombreQuark VARCHAR(255);
    SELECT nombreQuark INTO nombreQuark
    FROM Estilos
    WHERE idEstilo = id;
    RETURN nombreQuark;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `g_empates`(fec DATE, refe INT) RETURNS varchar(255) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE v_ganadores VARCHAR(255) DEFAULT '';
    DECLARE finalizado INT DEFAULT 0;
    DECLARE ganadorCur CURSOR FOR 
        SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos)
        FROM ReunionCaballos reucab
        JOIN Caballos cab ON cab.idCaballo = reucab.idCaballo
        WHERE reucab.fecha = fec AND reucab.referencia = refe AND reucab.puesto = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finalizado = 1;

    OPEN ganadorCur;

    bucle: LOOP
        FETCH ganadorCur INTO v_ganadores;
        IF finalizado = 1 THEN 
            LEAVE bucle;
        END IF;
        
        IF LENGTH(v_ganadores) > 0 THEN
            SET v_ganadores = CONCAT(v_ganadores, '; ');
        END IF;
        
        SET v_ganadores = CONCAT(v_ganadores, ganador);
    END LOOP;

    CLOSE ganadorCur;

    RETURN v_ganadores;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `negrita_caballo_estudio`(
    fec DATE,
    ref INT,
    idCab INT
) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    DECLARE resultado INT;

    SELECT COUNT(*)
    INTO resultado
    FROM ReunionCaballos
    WHERE fecha = fec
    AND referencia = ref
    AND idCaballo = idCab;

    IF resultado > 0 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `n_ganador`(fec DATE, refe INT) RETURNS varchar(255) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE v_ganadores VARCHAR(255) DEFAULT '';
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_idCaballo INT;
    DECLARE v_nombre VARCHAR(30);
    DECLARE v_kilos INT;
    
    DECLARE cur_ganadores CURSOR FOR 
        SELECT cab.idCaballo, cab.breve, reucab.kilos 
        FROM ReunionCaballos reucab
        JOIN Caballos cab ON cab.idCaballo = reucab.idCaballo
        WHERE reucab.fecha = fec AND reucab.referencia = refe AND reucab.puesto = 1;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur_ganadores;
    
    read_loop: LOOP
        FETCH cur_ganadores INTO v_idCaballo, v_nombre, v_kilos;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET v_ganadores = CONCAT(v_ganadores, IF(LENGTH(v_ganadores) > 0, '; ', ''), v_idCaballo, ',', v_nombre, ',', v_kilos);
    END LOOP;
    
    CLOSE cur_ganadores;
    
    RETURN v_ganadores;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `quinto`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE quinto VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO quinto from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 5 limit 1;
    RETURN(quinto);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `segundo`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE segundo VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO segundo from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 2 limit 1;
    RETURN(segundo);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sexto`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE sexto VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO sexto from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 6 limit 1;
    RETURN(sexto);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sumas_ganadas`(idCaballo INT) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT SUM(premioGanado) INTO total
    FROM ReunionCaballos rc 
    JOIN ReunionCarreras rcar ON rcar.fecha = rc.fecha AND rcar.referencia = rc.referencia
    WHERE rc.idCaballo = idCaballo;
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sumas_ganadas_arena`(idCaballo INT) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(premioGanado), 0) INTO total
    FROM ReunionCaballos rc 
    JOIN ReunionCarreras rcar ON rcar.fecha = rc.fecha AND rcar.referencia = rc.referencia
    WHERE rc.idCaballo = idCaballo AND rcar.pista = 'A';
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sumas_ganadas_cesped`(idCaballo INT) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(premioGanado), 0) INTO total
    FROM ReunionCaballos rc 
    JOIN ReunionCarreras rcar ON rcar.fecha = rc.fecha AND rcar.referencia = rc.referencia
    WHERE rc.idCaballo = idCaballo AND rcar.pista = 'C';
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sumas_ganadas_distancia`(idCaballo INT, distancia INT, pista CHAR(2)) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT SUM(premioGanado) INTO total
    FROM ReunionCaballos rc 
    JOIN ReunionCarreras rcar ON rcar.fecha = rc.fecha AND rcar.referencia = rc.referencia
    WHERE rc.idCaballo = idCaballo and rcar.distancia = distancia and rcar.pista = pista;
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `sumas_ganadas_pista`(idCaballo INT, pist CHAR(1)) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT SUM(premioGanado) INTO total
    FROM ReunionCaballos rc 
    JOIN ReunionCarreras rcar ON rcar.fecha = rc.fecha AND rcar.referencia = rc.referencia
    WHERE rc.idCaballo = idCaballo and rcar.pista = pist;
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `tercero`(fec DATE, refe INT) RETURNS varchar(30) CHARSET utf8mb4
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE tercero VARCHAR(30);
	SELECT concat(cab.idCaballo, ',', cab.breve, ',', reucab.kilos) INTO tercero from ReunionCaballos reucab
    join Caballos cab on cab.idCaballo = reucab.idCaballo
    where reucab.fecha = fec and reucab.referencia = refe and reucab.puesto = 3 limit 1;
    RETURN(tercero);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `total_boletos`(fec DATE, refe INT) RETURNS decimal(7,2)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE total INT;
	SELECT SUM(boletosGanador) INTO total from ReunionCaballos rc 
	where rc.fecha = fec and rc.referencia = refe;
    RETURN(total);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ActualizarEstadisticasJinetes`(IN fechaInicio DATE, IN fechaFin DATE)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
    UPDATE Jinetes
    JOIN (
        SELECT
            rc.idJinete,
            COUNT(*) AS corridas,
            SUM(CASE WHEN rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadas,
            SUM(CASE WHEN rc.puesto = 2 THEN 1 ELSE 0 END) AS places,
            SUM(CASE WHEN rc.puesto = 3 THEN 1 ELSE 0 END) AS terceros,
            SUM(CASE WHEN rc.puesto = 4 THEN 1 ELSE 0 END) AS cuartos,
            SUM(CASE WHEN rc.puesto = 5 THEN 1 ELSE 0 END) AS quintos,
            SUM(CASE WHEN rc.favorito = 1 THEN 1 ELSE 0 END) AS favorito,
            SUM(CASE WHEN rc.favorito = 1 AND rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadasFavorito,
            
            SUM(CASE WHEN rcar.idClasico != 378 AND rcar.idClasico != 0 THEN 1 ELSE 0 END) AS corridasClasicos,
            SUM(CASE WHEN rc.puesto = 1 AND rcar.idClasico != 378 AND rcar.idClasico != 0 THEN 1 ELSE 0 END) AS ganadasClasicos
        FROM ReunionCaballos rc
        INNER JOIN ReunionCarreras rcar ON rc.fecha = rcar.fecha AND rc.referencia = rcar.referencia
        WHERE rc.fecha BETWEEN fechaInicio AND fechaFin
              AND rc.corrio = 1
        GROUP BY rc.idJinete
    ) AS Estadisticas ON Jinetes.idJinete = Estadisticas.idJinete
    SET
        Jinetes.corridas = Estadisticas.corridas,
        Jinetes.ganadas = Estadisticas.ganadas,
        Jinetes.places = Estadisticas.places,
        Jinetes.terceros = Estadisticas.terceros,
        Jinetes.cuartos = Estadisticas.cuartos,
        Jinetes.quintos = Estadisticas.quintos,
        Jinetes.favorito = Estadisticas.favorito,
        Jinetes.ganadasFavorito = Estadisticas.ganadasFavorito,
        
        Jinetes.corridasClasicos = Estadisticas.corridasClasicos,
        Jinetes.ganadasClasicos = Estadisticas.ganadasClasicos;
        
    
    UPDATE Jinetes j
	JOIN (
		SELECT 
			rc.idJinete,
			COUNT(*) AS VecesUltimo
		FROM 
			ReunionCaballos rc
		INNER JOIN (
			SELECT 
				fecha,
				referencia,
				MAX(puesto) AS UltimoPuesto
			FROM 
				ReunionCaballos
			WHERE 
				fecha between '2024-01-01' and '2024-02-26' and corrio = 1 
			GROUP BY 
				fecha, referencia
		) AS Ultimos ON rc.fecha = Ultimos.fecha AND rc.referencia = Ultimos.referencia AND rc.puesto = Ultimos.UltimoPuesto
		GROUP BY 
			rc.idJinete
	) AS Resultados ON j.idJinete = Resultados.idJinete
	SET 
		j.ultimo = Resultados.VecesUltimo;
    SET SQL_SAFE_UPDATES = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ActualizarEstadisticasPreparadores`(IN fechaInicio DATE, IN fechaFin DATE)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
    UPDATE Preparadores
    JOIN (
        SELECT
            rc.idPreparador,
            COUNT(*) AS corridas,
            SUM(CASE WHEN rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadas,
            SUM(CASE WHEN rc.puesto = 2 THEN 1 ELSE 0 END) AS places,
            SUM(CASE WHEN rc.puesto = 3 THEN 1 ELSE 0 END) AS terceros,
            SUM(CASE WHEN rc.puesto = 4 THEN 1 ELSE 0 END) AS cuartos,
            SUM(CASE WHEN rc.puesto = 5 THEN 1 ELSE 0 END) AS quintos,
            SUM(CASE WHEN rc.favorito = 1 THEN 1 ELSE 0 END) AS favorito,
            SUM(CASE WHEN rc.favorito = 1 AND rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadasFavorito,
            
            SUM(CASE WHEN rcar.idClasico != 378 AND rcar.idClasico != 0 THEN 1 ELSE 0 END) AS corridasClasicos,
            SUM(CASE WHEN rc.puesto = 1 AND rcar.idClasico != 378 AND rcar.idClasico != 0 THEN 1 ELSE 0 END) AS ganadasClasicos
        FROM ReunionCaballos rc
        INNER JOIN ReunionCarreras rcar ON rc.fecha = rcar.fecha AND rc.referencia = rcar.referencia
        WHERE rc.fecha BETWEEN fechaInicio AND fechaFin
              AND rc.corrio = 1
        GROUP BY rc.idPreparador
    ) AS Estadisticas ON Preparadores.idPreparador = Estadisticas.idPreparador
    SET
        Preparadores.corridas = Estadisticas.corridas,
        Preparadores.ganadas = Estadisticas.ganadas,
        Preparadores.places = Estadisticas.places,
        Preparadores.terceros = Estadisticas.terceros,
        Preparadores.cuartos = Estadisticas.cuartos,
        Preparadores.quintos = Estadisticas.quintos,
        Preparadores.favorito = Estadisticas.favorito,
        Preparadores.ganadasFavorito = Estadisticas.ganadasFavorito,
        
        Preparadores.corridasClasicos = Estadisticas.corridasClasicos,
        Preparadores.ganadasClasicos = Estadisticas.ganadasClasicos;    
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ActualizarEstadisticasPreparadoresCompleto`(IN fechaInicio DATE, IN fechaFin DATE)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
    UPDATE Preparadores
    JOIN (
        SELECT
            rc.idPreparador,
            pre.preparador,
            COUNT(*) AS corridas,
            SUM(CASE WHEN rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadas,
            SUM(CASE WHEN rc.puesto = 2 THEN 1 ELSE 0 END) AS places,
            SUM(CASE WHEN rc.puesto = 3 THEN 1 ELSE 0 END) AS terceros,
            SUM(CASE WHEN rc.puesto = 4 THEN 1 ELSE 0 END) AS cuartos,
            SUM(CASE WHEN rc.puesto = 5 THEN 1 ELSE 0 END) AS quintos,
            SUM(CASE WHEN rc.favorito = 1 THEN 1 ELSE 0 END) AS favorito,
            SUM(CASE WHEN rc.favorito = 1 AND rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadasFavorito,
            
            SUM(CASE WHEN rcar.idClasico IS NOT NULL THEN 1 ELSE 0 END) AS corridasClasicos,
            SUM(CASE WHEN rcar.idClasico IS NOT NULL AND rc.puesto = 1 THEN 1 ELSE 0 END) AS ganadasClasicos,
            sum(case when cc.startRefe = 'H' THEN 1 ELSE 0 end) as corridasHandicap,
            sum(case when cc.startRefe = 'H' AND rc.puesto = 1 THEN 1 ELSE 0 end) as ganadasHandicap,
            sum(case when cc.startRefe = 'c'  AND rcar.idclasico is NULL THEN 1 ELSE 0 end) as corridasCondic,
            sum(case when cc.startRefe = 'c'  AND rcar.idclasico is NULL AND rc.puesto = 1 THEN 1 ELSE 0 end) as ganadasCondic,
            sum(case when rc.debutante = 1 THEN 1 ELSE 0 end) as corridasDebut,
            sum(case when rc.debutante = 1 AND rc.puesto = 1 THEN 1 ELSE 0 end) as ganadasDebut,
            sum(case when rc.cambioPasto = 1 then 1 else 0 end) as corridasCambioCesped,
            sum(case when rc.cambioPasto = 1 and rc.puesto = 1 then 1 else 0 end) as ganadasCambioCesped,
            sum(case when rc.cambioArena = 1 then 1 else 0 end) as corridasCambioArena,
            sum(case when rc.cambioArena = 1 and rc.puesto = 1 then 1 else 0 end) as ganadasCambioArena,
            sum(case when rc.cambioCorta = 1 then 1 else 0 end) as corridasCambioCorta,
            sum(case when rc.cambioCorta = 1 and rc.puesto = 1 then 1 else 0 end) as ganadasCambioCorta,
            sum(case when rc.cambioLarga = 1 then 1 else 0 end) as corridasCambioLarga,
            sum(case when rc.cambioLarga = 1 and rc.puesto = 1 then 1 else 0 end) as ganadasCambioLarga,
            sum(case when rc.cambioPreparador = 1 then 1 else 0 end) as corridasCambioPrep,
            sum(case when rc.cambioPreparador = 1 and rc.puesto = 1 then 1 else 0 end) as ganadasCambioPrep,
            sum(case when rc.reaparicion >= 31 and rc.reaparicion <= 60 then 1 else 0 end) as corridasReap1,
            sum(case when rc.reaparicion >= 31 and rc.reaparicion <= 60 and rc.puesto = 1 then 1 else 0 end) as ganadasReap1,
            sum(case when rc.reaparicion >= 61 and rc.reaparicion <= 180 then 1 else 0 end) as corridasReap2,
            sum(case when rc.reaparicion >= 61 and rc.reaparicion <= 180 and rc.puesto = 1 then 1 else 0 end) as ganadasReap2,
            sum(case when rc.reaparicion > 180 then 1 else 0 end) as corridasReap3,
            sum(case when rc.reaparicion > 180 and rc.puesto = 1 then 1 else 0 end) as ganadasReap3,
            
            SUM(rc.premioGanado) as sumasGanadas
        FROM ReunionCaballos rc
        INNER JOIN ReunionCarreras rcar ON rc.fecha = rcar.fecha AND rc.referencia = rcar.referencia
        inner join CondicionesClave cc on rcar.idCondicionEstudie = cc.idCondicion
        inner join Preparadores pre on rc.idPreparador = pre.idPreparador
        WHERE rc.fecha BETWEEN fechaInicio AND fechaFin
              AND rc.corrio = 1
        GROUP BY rc.idPreparador
    )   AS Estadisticas ON Preparadores.idPreparador = Estadisticas.idPreparador
    SET
        Preparadores.corridas = Estadisticas.corridas,
        Preparadores.ganadas = Estadisticas.ganadas,
        Preparadores.places = Estadisticas.places,
        Preparadores.terceros = Estadisticas.terceros,
        Preparadores.cuartos = Estadisticas.cuartos,
        Preparadores.quintos = Estadisticas.quintos,
        Preparadores.favorito = Estadisticas.favorito,
        Preparadores.ganadasFavorito = Estadisticas.ganadasFavorito,
        Preparadores.corridasClasicos = Estadisticas.corridasClasicos,
        Preparadores.ganadasClasicos = Estadisticas.ganadasClasicos,
       	Preparadores.corridasHandicap = Estadisticas.corridasHandicap,
       	Preparadores.ganadasHandicap = Estadisticas.ganadasHandicap,
        Preparadores.corridasCondicional = Estadisticas.corridasCondic,
        Preparadores.ganadasCondicional = Estadisticas.ganadasCondic,
        Preparadores.corridasDebutantes = Estadisticas.corridasDebut,
        Preparadores.ganadasDebutantes = Estadisticas.ganadasDebut,
        Preparadores.corridasCambioCesped = Estadisticas.corridasCambioCesped,
        Preparadores.ganadasCambioCesped = Estadisticas.ganadasCambioCesped,
        Preparadores.corridasCambioCesped = Estadisticas.corridasCambioArena,
        Preparadores.ganadasCambioArena = Estadisticas.ganadasCambioArena,
        Preparadores.corridasCambioCorta = Estadisticas.corridasCambioCorta,
        Preparadores.ganadasCambioCorta = Estadisticas.ganadasCambioCorta,
        Preparadores.corridasCambioLarga = Estadisticas.corridasCambioLarga,
        Preparadores.ganadasCambioLarga = Estadisticas.ganadasCambioLarga,
        Preparadores.corridasCambioPrep = Estadisticas.corridasCambioPrep,
        Preparadores.ganadasCambioPrep = Estadisticas.ganadasCambioPrep,
        Preparadores.corridasReap1 = Estadisticas.corridasReap1,
        Preparadores.ganadasReap2 = Estadisticas.ganadasReap2,
        Preparadores.corridasReap2 = Estadisticas.corridasReap2,
        Preparadores.ganadasReap2 = Estadisticas.ganadasReap2,
        Preparadores.corridasReap3 = Estadisticas.corridasReap3,
        Preparadores.ganadasReap3 = Estadisticas.ganadasReap3,
		Preparadores.sumasGanadas = Estadisticas.sumasGanadas;
    SET SQL_SAFE_UPDATES = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CrearTablaEncuentros`(IN p_fecha DATE, IN p_referencia INT)
BEGIN
    DROP TABLE IF EXISTS Encuentros;
    
    SET @s = CONCAT('
        CREATE TABLE Encuentros AS
        WITH CarrerasRecientes AS (
            SELECT 
                idCaballo, 
                fecha, 
                referencia,
                ROW_NUMBER() OVER (PARTITION BY idCaballo ORDER BY fecha DESC, referencia DESC) as CarreraReciente
            FROM 
                ReunionCaballos
            WHERE 
                idCaballo IN (SELECT idCaballo FROM ReunionCaballos WHERE fecha = ''', p_fecha, ''' AND referencia = ', p_referencia, ')
                AND corrio = 1
        ),
        Coincidencias AS (
            SELECT 
                ''', p_fecha, ''' AS FechaCarrera,
                ', p_referencia, ' AS ReferenciaCarrera,
                cr1.fecha AS FechaEncuentro, 
                cr1.referencia AS ReferenciaEncuentro, 
                c1.nombre AS NombreCaballo1, 
                c2.nombre AS NombreCaballo2
            FROM 
                CarrerasRecientes cr1
            JOIN 
                CarrerasRecientes cr2 ON cr1.fecha = cr2.fecha AND cr1.referencia = cr2.referencia AND cr1.idCaballo < cr2.idCaballo
            JOIN 
                Caballos c1 ON cr1.idCaballo = c1.idCaballo
            JOIN 
                Caballos c2 ON cr2.idCaballo = c2.idCaballo
            WHERE 
                cr1.CarreraReciente <= 8 AND cr2.CarreraReciente <= 8
        )
        SELECT 
            FechaCarrera, 
            ReferenciaCarrera, 
            FechaEncuentro, 
            ReferenciaEncuentro, 
            NombreCaballo1, 
            NombreCaballo2
        FROM Coincidencias
        GROUP BY FechaCarrera, ReferenciaCarrera, FechaEncuentro, ReferenciaEncuentro, NombreCaballo1, NombreCaballo2
        ORDER BY FechaCarrera DESC, ReferenciaCarrera DESC, FechaEncuentro DESC, ReferenciaEncuentro DESC;
    ');
    
    PREPARE stmt FROM @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `estudios_reunion`(IN id_caballo INT)
BEGIN
	SET @query = CONCAT ('select
	*
FROM
	(
	SELECT
		cab.referencia,
		cab.fecha,
		cab.kilos,
		jin.jinete,
		cab.realCajon,
		car.pista,
		car.distancia,
		car.baranda,
		centesimos_a_cadena(car.tiempoCentesimos),
		corrieron(car.fecha,
		car.referencia),
		cab.puesto AS pto
	FROM
		ReunionCarreras car
	join ReunionCaballos cab on
		cab.fecha = car.fecha
		and cab.referencia = car.referencia
	join Jinetes jin on
		jin.idJinete = cab.idJinete
	WHERE
		cab.idCaballo = ', 'id_caballo',
		' AND cab.corrio = 1 AND puesto <> 0
	order by
		cab.fecha desc,
		cab.referencia
	LIMIT 6)
	AS subconsulta
order by
	fecha'
);
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetHermanosEnteros`(IN idCaballo INT)
BEGIN
    DECLARE idPadre INT;
    DECLARE idMadre INT;
    DECLARE fechaNacimiento DATE;

    
    SELECT idPadre, idMadre, fechaNacimiento INTO idPadre, idMadre, fechaNacimiento
    FROM Caballos
    WHERE idCaballo = idCaballo;

    
    SELECT idCaballo
    FROM Caballos
    WHERE idPadre = idPadre AND idMadre = idMadre AND fechaNacimiento < fechaNacimiento AND idCaballo != idCaballo LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerHermanosEnteros`(IN idCaballo INT)
BEGIN
    SELECT c.idCaballo, c.minusculas, c.fechaNac
    FROM Caballos c
    INNER JOIN Caballos caballo_origen ON c.idPadre = caballo_origen.idPadre AND c.idMadre = caballo_origen.idMadre
    WHERE caballo_origen.idCaballo = idCaballo 
      AND c.idCaballo != idCaballo 
      AND c.fechaNac < caballo_origen.fechaNac;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerHermanosMaternos`(IN idCaballo INT)
BEGIN
    SELECT c.idCaballo, c.minusculas, c.fechaNac
    FROM Caballos c
    INNER JOIN Caballos caballo_origen 
        ON c.idMadre = caballo_origen.idMadre
    WHERE caballo_origen.idCaballo = idCaballo 
      AND c.idCaballo != idCaballo 
      AND c.idPadre != caballo_origen.idPadre  
      AND c.fechaNac < caballo_origen.fechaNac; 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-04 19:35:50
