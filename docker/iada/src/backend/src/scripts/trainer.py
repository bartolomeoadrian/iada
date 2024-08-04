from ..utils.vanna import vn

vn.train(
    ddl="""
-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS proyectos_id_seq;

-- Table Definition
CREATE TABLE "public"."proyectos" (
    "id" int4 NOT NULL DEFAULT nextval('proyectos_id_seq'::regclass),
    "titulo" varchar,
    "publicacion_fecha" date,
    "camara_origen" varchar,
    "exp_diputados" varchar,
    "exp_senado" varchar,
    "tipo" varchar
);
"""
)

vn.train(
    documentation="""En la tabla proyectos se almacenan los proyectos de ley que han sido presentados en el Congreso de la República Argentina.
    Los campos son:
		- id: identificador único del proyecto
		- titulo: título del proyecto
		- publicacion_fecha: fecha de publicación del proyecto
		- camara_origen: cámara de origen del proyecto
		- exp_dipt: expediente en diputados
		- exp_senado: expediente en el senado
		- tipo: tipo de proyecto
	"""
)
