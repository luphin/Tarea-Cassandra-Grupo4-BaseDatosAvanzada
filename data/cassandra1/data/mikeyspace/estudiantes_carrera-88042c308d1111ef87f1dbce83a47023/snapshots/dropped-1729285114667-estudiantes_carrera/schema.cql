CREATE TABLE IF NOT EXISTS mikeyspace.estudiantes_carrera (
    matriculado text,
    carrera text,
    region text,
    periodo int,
    cedula text,
    facultad text,
    gratuidad text,
    grupo_depen text,
    latitud float,
    longitud float,
    pace text,
    preferencia int,
    psu_promlm float,
    ptje_nem float,
    puntaje float,
    sexo text,
    PRIMARY KEY ((matriculado, carrera), region, periodo, cedula)
) WITH ID = 88042c30-8d11-11ef-87f1-dbce83a47023
    AND CLUSTERING ORDER BY (region ASC, periodo ASC, cedula ASC)
    AND additional_write_policy = '99p'
    AND allow_auto_snapshot = true
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND memtable = 'default'
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND extensions = {}
    AND gc_grace_seconds = 864000
    AND incremental_backups = true
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';
