# YouTube Comments Analyzer

Proyecto para la recopilación, análisis y visualización de métricas de canales y vídeos de YouTube sobre true crime español, incluyendo estadísticas históricas, sentimientos y emociones de comentarios.

## Tecnologías utilizadas

- Python 3.10+
- PostgreSQL
- SQLAlchemy
- Docker y Docker Compose
- Streamlit
- Git

## Arquitectura general

- PostgreSQL almacena los datos y expone vistas SQL optimizadas para análisis.
- El backend en Python gestiona la ingesta de datos, la inicialización de la base de datos y el análisis mediante modelos PLN.
- Streamlit actúa como frontend para visualización de métricas, gráficos y KPIs.

## Estructura del proyecto

- back-end/
  - docker-compose.yml: servicios Docker (PostgreSQL)
  - src/
    - analysis/: definición de modelos PLN
    - config/: configuración de base de datos y de las variables de entorno
    - models/: modelos SQLAlchemy
    - repositories/: repositorios
    - services/: servicios
    - tests/: test funcionales
    - views/: vistas SQL consumidas por Streamlit
    - workers/: youtube_crawler y comments_analyzer
  - main.py: creación de tablas y vistas
  - .env.template: plantilla de variables de entorno

- front-end/
  - cards/: tarjetas reutilizadas para las 3 entidades (canal, video y comentario)
  - components/: filtros y paginacion reutilizados
  - db/: consultas a las vistas SQL
  - pages/: vistas presentes en la app (Canales, Videos, Comentarios, Analisis de canal y Analis de video)
  - plots/: funciones reutilizadas para pintar elementos de Plotly
  - services/: servicios
  - utils/: constantes y mapeos
  - 01_📊_Dashboard_general.py: aplicación frontend en Streamlit
  - .env.template: plantilla de variables de entorno
- README.md: documentación

## Configuración del entorno

1. Clonar el repositorio:

git clone https://github.com/sararoca/youtube-comments-analyzer.git
cd youtube-comments-analyzer

## Levantar la base de datos

Desde la raíz del proyecto:

docker compose up -d

Esto levantará PostgreSQL y creará el volumen persistente de datos.

## Inicializar la base de datos

Con el entorno virtual activado e instalaciones completadas:

Desde youtube_comments_analyzer/back-end:

Crear archivo de entorno editando las variables:

cp .env.template .env

Lanzar la inicialización de la base de datos:

python src/main.py

Este script:

- Crea las tablas con SQLAlchemy
- Ejecuta el archivo views.sql
- Deja la base de datos lista para consultas analíticas

## Lanzar el crawler de comentarios

python src/workers/youtube_crawler.py

Este script:

- Recupera los datos de la API de YouTube
- Almacena los datos en la BD

## Lanzar el analizador de comentarios

python src/workers/comments_analyzer.py

Este script:

- Recupera los comentarios que no han sido analizados
- Analiza los comentarios para detectar emociones
- Analiza los comentarios para detectar sentimientos
- Almacena los nuevos datos de emocion y sentimiento en la BD
- Actualiza los comentarios en la BD para que no aparezcan como NO analizados

## Ejecutar el frontend (Streamlit)

Con el entorno virtual activado e instalaciones completadas:

Desde youtube_comments_analyzer/front-end:

Crear archivo de entorno editando las variables:

cp .env.template .env

Lanzar el dashboard:

streamlit run .\01_📊_Dashboard_general.py

La aplicación quedará accesible por defecto en:

http://localhost:8501

## Funcionalidades del frontend

- KPIs de canales y vídeos
- Evolución temporal de métricas
- Análisis de emociones y sentimientos
- Filtros por canal, vídeo y métricas

## Control de versiones

Se sube al repositorio:

- Código fuente
- docker-compose.yml
- views.sql
- .env.template

No se sube:

- .env
- Volúmenes de Docker
- Datos de PostgreSQL
- Cachés y entornos virtuales

## Notas

- Docker Compose puede compartirse sin problema.
- Las credenciales reales nunca deben incluirse en el repositorio.
- Las vistas SQL son la capa principal de consulta para el frontend.
