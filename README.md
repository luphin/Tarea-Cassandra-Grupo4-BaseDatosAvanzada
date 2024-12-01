# Tarea sobre el Sistema de Gestión de Bases de Datos NoSQL: Apache Cassandra

En esta tarea, se requiere la creación de un clúster compuesto por tres nodos, con el objetivo de lograr la distribución eficiente de los datos.
- [01 Tarea-Laboratorio-1-Cassandra](https://github.com/luphin/Tarea-Cassandra-Grupo4-BaseDatosAvanzada/blob/main/documents/01%20Tarea-Laboratorio-1-Cassandra.pdf)
- [InformeGrupo4](https://github.com/luphin/Tarea-Cassandra-Grupo4-BaseDatosAvanzada/blob/main/documents/InformeGrupo4.pdf)

>[!IMPORTANT]
> La version de python que fue utilizada fue la v.3.9.6

## Instrucciones de uso 

### 1. Iniciar Cassandra en docker
```
## Creacion del Cluster 
docker network create cassandra-cluster

## docker-compose
docker-compose up -d 
```

### 2.Crear un espacio dentro del Cluster
```
# Acceder al contenedor y a cqlsh
docker exec -it cassandra1 bash

cqlsh
# Caso de no funcionar, probar uno de los siguientes:
# cqlsh 127.20.0.1 
# cqlsh 127.20.0.2 
# cqlsh 127.20.0.3 
```

>[!NOTE]
> Si hay problemas al iniciar el cqlsh, revisar que el puerto este escuchando.
> ```
> ss -tuln | grep 9042
> ```

#### Verificar si exite `KEYSPACE`

>[!IMPORTANT]
> El `KEYSPACE` mikeyspace esta creado y con los datos cargados (utilizado para la tarea). Solo hacer este paso si se quiere agregar 
> un nuevo `KEYSPACE`, en ese caso se deben descargar las librerias de python.

```
DESCRIBE KEYSPACES;
```
en el caso que diga que no existe ninguno ejecutar: 
```
## keyspace se llama 'mikeyspace'
CREATE KEYSPACE mikeyspace WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};
```
luego: 
```
##Cambiar al keyspace
USE mikeyspace;  
```

### 3. Poblar los nodos
#### Instalar dependencias si no las tienes
Dentro de la consola, ejecutar:

```
## pandas 
pip install pandas

## cassandra-driver
pip install cassandra-driver

## openpyxl
pip install openpyxl

```
#### Poblar nodos
>[!CAUTION]
> Revisar si en el `KEYSPACE` no esta cargada ya, la tabla `poblaciones`, en caso que exista, verificar sus datos.

```
python3 populate_cassandra.py 
```

### 4. Comprobar que estan los datos en los nodos
Ingresar a `cqlsh` en caso de haberse salido, reingresar con:

```
docker exec -it cassandra1 bash

cqlsh 

## Conectar a cqlsh (ya lo hiciste)
## Listar KEYSPACES
cqlsh> DESCRIBE KEYSPACES; 

## Suponiendo que tu keyspace se llama 'mikeyspace'
cqlsh> USE mikeyspace;  ## Cambiar al keyspace

## Listar tablas en el keyspace
cqlsh> DESCRIBE TABLES; 
```

### 5. Operaciones solicitadas para requisito 3

1. . Devolver todos los postulantes matriculados en la carrera de medicina ordenados por periodo.

En este caso se utiliza la tabla estudiantes_carrera.
```
SELECT * FROM estudiantes_carrera WHERE matriculado = 'SI' AND carrera = 'MEDICINA';

```

2. Devolver todos los postulantes matriculados provenientes de la región del Maule en la carrera Ingeniería Civil Informática ordenados por periodo.

En este caso se utiliza la tabla estudiantes_region.
```
SELECT * FROM estudiantes_region WHERE matriculado = 'SI' AND carrera = 'INGENIERÍA CIVIL INFORMÁTICA' AND region = 'MAULE';
```

3. Devolver todos los postulantes matriculados en la facultad de Ciencias de la Salud ordenado por puntaje PSU.

En este caso se utiliza la tabla estudiantes_facultad.
```
SELECT * FROM estudiantes_facultad WHERE matriculado = 'SI' AND facultad = 'CIENCIAS DE LA SALUD';
```

### 5. Detener el contenedor 

```
## Detener el contenedor cassandra1
docker stop cassandra1

## Detener todos los contenedores
docker stop $(docker ps -q)

```

para detener y eliminar los contenedores: 

```
## Detener y eliminar el contenedor cassandra1
docker rm -f cassandra1

## Detener y eliminar todos los contenedores
docker rm -f $(docker ps -q)

```

detener el cluster

```
docker network rm cassandra-cluster
```

## Verificar consistencia
Ejecutar:
```
python3 consintency.py
```
>[!NOTE]
> Cambiar los datos a ingresar, porque al hacer la prueba los datos dentro del archivo, ya fueron agregados.

## Autores
### Grupo4
1. Ernesto Sebastián Barria Andrade
2. Camilo Días Galaz
3. Sebastian Gutiérrez Milla
4. Carlos Lago Cortes
5. Luis Zegarra Stuardo

