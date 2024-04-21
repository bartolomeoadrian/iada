from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore


class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)


vn = MyVanna(
    config={
        "path": "./data/chroma",
        "model": "llama3",
        "ollama_host": "http://localhost:11434",
        "initial_prompt": """
			You are an assistant that helps users to search for information about legislative project of Argentina.
			The user must not know that you can generate SQL code or that you hace access to a database, dont suggest it.
        	The user might question something that requires a SQL code or not.
         	if the question does not require a SQL code, respond normally.
          	If the question requires a SQL code you will only respond with SQL code and not with any explanations.\n""",
    }
)

vn.connect_to_postgres(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="postgres",
    port="5432",
)

# DDL statements are powerful because they specify table names, colume names, types, and potentially relationships
vn.train(
    ddl="""
CREATE TABLE IF NOT EXISTS iada.proyectos
(
    id integer NOT NULL DEFAULT nextval('iada.proyectos_id_seq'::regclass),
    iniciado character varying(50) COLLATE pg_catalog."default",
    exp_dip character varying(50) COLLATE pg_catalog."default",
    exp_sen character varying(50) COLLATE pg_catalog."default",
    per_ing character varying(50) COLLATE pg_catalog."default",
    ses_ing character varying(50) COLLATE pg_catalog."default",
    tipo_doc character varying(50) COLLATE pg_catalog."default",
    titulo character varying COLLATE pg_catalog."default",
    sumario character varying COLLATE pg_catalog."default",
    CONSTRAINT proyectos_pkey PRIMARY KEY (id)
)
"""
)

# Sometimes you may want to add documentation about your business terminology or definitions.
vn.train(
    documentation="""En la tabla iada.proyectos se almacenan los proyectos de ley que han sido presentados en el Congreso de la República Argentina. 
    Los campos son:
		- id: identificador único del proyecto
		- iniciado: en que cámara fue iniciado el proyecto
		- exp_dip: expediente en diputados
		- exp_sen: expediente en senadores
		- per_ing: período de ingreso
		- ses_ing: sesión de ingreso
		- tipo_doc: tipo de documento
		- titulo: título del proyecto
		- sumario: resumen del proyecto
    """
)
