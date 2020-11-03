/*
	SpName: sp_categoria_producto
	Autor: Luis Ramon Valencia Aguayo
	Fecha: 25-10-2020
	Desarroll: CRUD de categoria de productos
	Modulo: Categoria Productos
*/

DELIMITER //
DROP PROCEDURE IF EXISTS sp_categoria_producto //

CREATE PROCEDURE sp_categoria_producto(IN v_id INT,IN v_nombre VARCHAR(200),IN vtipo CHAR(30))
	BEGIN

		IF (vtipo = 'CREATE') THEN
			INSERT INTO tiendavirtual.categoria_producto(nombre,created_at,updated_at) VALUES(v_nombre,NOW(),NOW());
			SELECT 'Registro agregado con exito';
		ELSEIF(vtipo = 'READ') THEN
			SELECT * FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL;
		ELSEIF(vtipo = 'UPDATE') THEN
			UPDATE tiendavirtual.categoria_producto SET nombre = v_nombre, updated_at = NOW() WHERE id = v_id;
			SELECT 'Registro modificado con exito';
		ELSEIF(vtipo = 'DELETE') THEN
				UPDATE tiendavirtual.categoria_producto SET deleted_at=NOW() WHERE id = v_id;
				SELECT 'Registro eliminado con exito';
		ELSEIF(vtipo = 'COLUMNS') THEN
			SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='categoria_producto' AND table_schema='tiendavirtual';
		ELSEIF(vtipo = 'COUNTCOLUMN') THEN
			SELECT COUNT(COLUMN_NAME ) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'categoria_producto' AND table_schema='tiendavirtual';
		ELSEIF(vtipo = 'COUNTDATA') THEN
			SELECT COUNT(*) FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL;
		ELSEIF(vtipo = 'COUNTEXIST') THEN
			SELECT COUNT(*) as total FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL AND nombre = v_nombre;
		END IF;
	END //
DELIMITER ;