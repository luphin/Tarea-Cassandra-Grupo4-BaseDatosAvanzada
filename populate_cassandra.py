import pandas as pd
from cassandra.cluster import Cluster

# Leer el archivo Excel
df = pd.read_excel('postulaciones.xlsx')

# Eliminar espacios en blanco de los nombres de las columnas
df.columns = df.columns.str.strip()

# Reemplazar NaN con una cadena vacía o un valor por defecto
df = df.fillna({
    'CEDULA': '',
    'PERIODO': 0,
    'SEXO': '',
    'PREFERENCIA': 0,
    'CARRERA': '',
    'MATRICULADO': '',
    'FACULTAD': '',
    'PUNTAJE': 0.0,
    'GRUPO_DEPEN': '',
    'REGION': '',
    'LATITUD': 0.0,
    'LONGITUD': 0.0,
    'PTJE_NEM': 0.0,
    'PSU_PROMLM': 0.0,
    'PACE': '',
    'GRATUIDAD': ''
})

# Convertir los tipos de datos
df['CEDULA'] = df['CEDULA'].astype(str)
df['PERIODO'] = df['PERIODO'].astype(int)
df['PREFERENCIA'] = df['PREFERENCIA'].astype(int)
df['PUNTAJE'] = df['PUNTAJE'].astype(float)
df['LATITUD'] = df['LATITUD'].astype(float)
df['LONGITUD'] = df['LONGITUD'].astype(float)
df['PTJE_NEM'] = df['PTJE_NEM'].astype(float)
df['PSU_PROMLM'] = df['PSU_PROMLM'].astype(float)

# Imprimir las primeras filas y las columnas del DataFrame
print(df.head())  # Verifica que los datos se carguen correctamente
print(df.columns)  # Verifica que los nombres de las columnas son correctos
print('Se están agregando los datos...')  # Mensaje de observabilidad

# Conectar a Cassandra
cluster = Cluster(['127.0.0.1', '127.0.0.1', '127.0.0.1'])  # Todos los nodos en la misma IP
session = cluster.connect('mikeyspace')  # Nombre del keyspace

# Crear la tabla 'estudiantes_carrera' si no existe
session.execute("""
CREATE TABLE IF NOT EXISTS estudiantes_carrera (
    cedula TEXT,
    periodo INT,
    sexo TEXT,
    preferencia INT,
    carrera TEXT,
    matriculado TEXT,
    facultad TEXT,
    puntaje FLOAT,
    grupo_depen TEXT,
    region TEXT,
    latitud FLOAT,
    longitud FLOAT,
    ptje_nem FLOAT,
    psu_promlm FLOAT,
    pace TEXT,
    gratuidad TEXT,
    PRIMARY KEY ((matriculado, carrera), periodo, cedula)
) WITH CLUSTERING ORDER BY (periodo DESC);
""")

# Crear la tabla 'estudiantes_region' si no existe
session.execute("""
CREATE TABLE IF NOT EXISTS estudiantes_region (
    cedula TEXT,
    periodo INT,
    sexo TEXT,
    preferencia INT,
    carrera TEXT,
    matriculado TEXT,
    facultad TEXT,
    puntaje FLOAT,
    grupo_depen TEXT,
    region TEXT,
    latitud FLOAT,
    longitud FLOAT,
    ptje_nem FLOAT,
    psu_promlm FLOAT,
    pace TEXT,
    gratuidad TEXT,
    PRIMARY KEY ((matriculado, carrera), region, periodo, cedula)
) WITH CLUSTERING ORDER BY (region DESC, periodo DESC);
""")

# Crear la tabla 'estudiantes_facultad' para la consulta 3 si no existe
session.execute("""
CREATE TABLE IF NOT EXISTS estudiantes_facultad (
    cedula TEXT,
    periodo INT,
    sexo TEXT,
    preferencia INT,
    carrera TEXT,
    matriculado TEXT,
    facultad TEXT,
    puntaje FLOAT,
    grupo_depen TEXT,
    region TEXT,
    latitud FLOAT,
    longitud FLOAT,
    ptje_nem FLOAT,
    psu_promlm FLOAT,
    pace TEXT,
    gratuidad TEXT,
    PRIMARY KEY ((matriculado, facultad), puntaje, cedula)
) WITH CLUSTERING ORDER BY (puntaje DESC);
""")

# Cargar los datos en ambas tablas
for index, row in df.iterrows():
    # Insertar en la tabla 'estudiantes_carrera'
    session.execute("""
    INSERT INTO estudiantes_carrera (cedula, periodo, sexo, preferencia, carrera, matriculado,
                             facultad, puntaje, grupo_depen, region, latitud, longitud,
                             ptje_nem, psu_promlm, pace, gratuidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['CEDULA'], row['PERIODO'], row['SEXO'], row['PREFERENCIA'], row['CARRERA'],
          row['MATRICULADO'], row['FACULTAD'], row['PUNTAJE'], row['GRUPO_DEPEN'],
          row['REGION'], row['LATITUD'], row['LONGITUD'], row['PTJE_NEM'],
          row['PSU_PROMLM'], row['PACE'], row['GRATUIDAD']))
    
    # Insertar en la tabla 'estudiantes_region'
    session.execute("""
    INSERT INTO estudiantes_region (cedula, periodo, sexo, preferencia, carrera, matriculado,
                             facultad, puntaje, grupo_depen, region, latitud, longitud,
                             ptje_nem, psu_promlm, pace, gratuidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['CEDULA'], row['PERIODO'], row['SEXO'], row['PREFERENCIA'], row['CARRERA'],
          row['MATRICULADO'], row['FACULTAD'], row['PUNTAJE'], row['GRUPO_DEPEN'],
          row['REGION'], row['LATITUD'], row['LONGITUD'], row['PTJE_NEM'],
          row['PSU_PROMLM'], row['PACE'], row['GRATUIDAD']))

    # Insertar en la tabla 'estudiantes_facultad'
    session.execute("""
    INSERT INTO estudiantes_facultad (cedula, periodo, sexo, preferencia, carrera, matriculado,
                                       facultad, puntaje, grupo_depen, region, latitud, longitud,
                                       ptje_nem, psu_promlm, pace, gratuidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['CEDULA'], row['PERIODO'], row['SEXO'], row['PREFERENCIA'], row['CARRERA'],
          row['MATRICULADO'], row['FACULTAD'], row['PUNTAJE'], row['GRUPO_DEPEN'],
          row['REGION'], row['LATITUD'], row['LONGITUD'], row['PTJE_NEM'],
          row['PSU_PROMLM'], row['PACE'], row['GRATUIDAD']))

# Cerrar la conexión
cluster.shutdown()

print('Los datos fueron agregados.')  # Mensaje de observabilidad

