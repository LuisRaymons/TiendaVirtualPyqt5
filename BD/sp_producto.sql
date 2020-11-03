/*
	SpName: sp_producto
	Autor: Luis Ramon Valencia Aguayo
	Fecha: 25-10-2020
	Desarroll: CRUD de productos
	Modulo: Productos
*/

DELIMITER //
DROP PROCEDURE IF EXISTS sp_producto //

CREATE PROCEDURE sp_producto(IN v_id INT,v_nombre VARCHAR(200),IN v_descripcion VARCHAR(400),IN v_costo DECIMAL(10,2),IN v_precioPorKilo CHAR(10),IN v_caducidad DATE,IN v_img VARCHAR(200),IN v_id_categoria BIGINT(20), IN vtipo CHAR(30))
	BEGIN
		IF (vtipo = 'CREATE') THEN
			INSERT INTO tiendavirtual.producto(nombre,descripcion,costo,precioPorKilo,caducidad,img,id_categoria,created_at,updated_at) 
					VALUES(v_nombre,v_descripcion,v_costo,v_precioPorKilo,v_caducidad,v_img,v_id_categoria,NOW(),NOW());
			SELECT 'Registro agregado con exito';
		ELSEIF(vtipo = 'READ') THEN
			SELECT * FROM tiendavirtual.producto WHERE deleted_at IS NULL;
		ELSEIF(vtipo = 'UPDATE') THEN
			UPDATE tiendavirtual.producto SET 
				nombre=v_nombre,
				descripcion=v_descripcion,
				costo=v_costo,
				precioPorKilo=v_precioPorKilo,
				caducidad=v_ducidad,
				img=v_img,
				id_categoria=v_id_categoria,
				updated_at = NOW()
			WHERE id=v_id;

		ELSEIF(vtipo = 'DELETE') THEN
			UPDATE tiendavirtual.producto SET
				deleted_at = NOW()
			WHERE id=v_id; 
		ELSEIF(vtipo = 'COLUMNS') THEN
			SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='producto' AND table_schema='tiendavirtual';
		ELSEIF(vtipo = 'COUNTCOLUMN') THEN
			SELECT COUNT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'producto' AND table_schema='tiendavirtual';
		ELSEIF(vtipo = 'COUNTDATA') THEN
			SELECT COUNT(*) FROM tiendavirtual.producto WHERE deleted_at IS NULL;
		ELSEIF(vtipo = 'COUNTEXIST') THEN
			SELECT COUNT(*) as total FROM tiendavirtual.producto WHERE deleted_at IS NULL AND nombre=v_nombre and descripcion=v_descripcion;
		ELSEIF(vtipo = 'CATEGORIAS') THEN
			SELECT * FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL;
		ELSEIF(vtipo = 'CATEGORIASEXISTS') THEN
			SELECT * FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL AND nombre=v_nombre;
		ELSEIF(vtipo = 'CATEGORIABYID') THEN
			SELECT * FROM tiendavirtual.categoria_producto WHERE deleted_at IS NULL AND id= v_id;
		END IF;

	END //
DELIMITER ;