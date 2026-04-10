# Problemática: dag-factory en entornos productivos

## Contexto

`dag-factory` es una librería de Apache Airflow que permite definir DAGs de forma declarativa usando archivos YAML, eliminando la necesidad de escribir Python directamente. Su funcionamiento actual depende de que la librería esté instalada y activa en el servidor de Airflow en producción.

## El problema

### dag-factory vive en producción

El modelo actual requiere que dag-factory esté instalado en el entorno de Airflow productivo. Los archivos `.py` en la carpeta `dags/` contienen código como:

```python
from dagfactory import load_yaml_dags
load_yaml_dags(globals(), "/path/to/dags/")
```

Esto significa que en cada ciclo del DAG Processor, Airflow ejecuta dag-factory para:

1. Leer cada archivo YAML del disco
2. Parsearlo y convertirlo a un diccionario Python
3. Construir dinámicamente los objetos `DAG` y `Task`
trabajo de construcción de los DAGs que se repite innecesariamente
4. Registrarlos en `globals()` para que Airflow los descubra

### Consecuencias

**Performance degradada a escala**

El DAG Processor corre en un loop continuo (por defecto cada 30 segundos). Con pocos YAMLs el impacto es invisible, pero a medida que crecen los DAGs:

- Cada ciclo repite el proceso completo de parseo y construcción para todos los archivos, hayan cambiado o no
- El Scheduler queda esperando que el DAG Processor termine para tomar decisiones
- El tiempo de ciclo crece linealmente con la cantidad de DAGs
- Mayor consumo de CPU en el worker del DAG Processor

**Dependencia de una librería de terceros en producción**

- Un bug en dag-factory puede romper el entorno productivo completo
- Actualizaciones de dag-factory requieren coordinar con el despliegue de Airflow
- No hay separación entre el tooling de desarrollo y el runtime de producción

**Falta de auditabilidad**

- Los DAGs reales (objetos Python) se generan dinámicamente en runtime y nunca son visibles
- No es posible hacer code review del DAG que efectivamente correrá en producción
- No hay trazabilidad entre una versión del YAML y el DAG que generó

**Fragilidad ante errores de configuración**

- Un error en un YAML puede impedir que el DAG Processor termine su ciclo
- El error aparece tarde, en runtime, en el servidor de producción
- No hay validación previa antes de que el YAML llegue al entorno productivo
