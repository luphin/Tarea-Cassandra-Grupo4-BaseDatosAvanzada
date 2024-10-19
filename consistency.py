from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel

# Conectar al clúster de Cassandra
cluster = Cluster(['127.0.0.1'])  # Cambia la IP por la de tu nodo Cassandra
session = cluster.connect('mikeyspace')  # Asegúrate de que 'mikeyspace' es tu keyspace

# Establecer el nivel de consistencia a QUORUM
session.default_consistency_level = ConsistencyLevel.QUORUM

# Consulta de escritura: Insertar datos en la tabla
insert_query = """
    INSERT INTO estudiantes_facultad (cedula, periodo, sexo, preferencia, carrera, matriculado, facultad, puntaje, grupo_depen, region, latitud, longitud, ptje_nem, psu_promlm, pace, gratuidad)
    VALUES ('12345678-9', 2024, 'MASCULINO', 1, 'MEDICINA', 'SI', 'CIENCIAS DE LA SALUD', 650.5, 'MUNICIPAL', 'RM', -33.4378, -70.6505, 550, 600, 'SI', 'SI');
"""

# Ejecutar la consulta de inserción
session.execute(insert_query)

# Confirmar que los datos fueron insertados (opcional)
print("Datos insertados correctamente.")

# Consulta de lectura: Seleccionar datos de la tabla
select_query = """
    SELECT cedula, facultad, matriculado, puntaje, carrera, sexo 
    FROM estudiantes_facultad 
    WHERE matriculado = 'SI' AND facultad = 'CIENCIAS DE LA SALUD' 
    AND puntaje >= 500;
"""

# Ejecutar la consulta de lectura
rows = session.execute(select_query)

# Mostrar los resultados
for row in rows:
    print(row)
