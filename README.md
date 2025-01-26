# reservas_canchas_deportivas

¡Bienvenido a **Reservas de canchas deportivas**! Esta es una aplicación web desarrollada con Flask(python), HTML, Javascript y CSS, además la base de datos está en MySQL. A continuación, te explicamos cómo configurar y ejecutar la aplicación en tu entorno local.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

1. **Docker**: Necesitarás Docker para ejecutar la aplicación en un contenedor.
   - [Instrucciones para instalar Docker](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Docker Compose se utiliza para gestionar múltiples contenedores.
   - [Instrucciones para instalar Docker Compose](https://docs.docker.com/compose/install/).

---

## Configuración del Proyecto

Sigue estos pasos para configurar y ejecutar la aplicación:

1. **Clona el Repositorio**:
   ```bash
   git clone https://github.com/vcornejo22/reservas_canchas_deportivas.git
   cd reservar_canchas_deportivas
   ```
2.  **Construye y ejecuta los contenedores**:  
    ```bash
    docker-compose up --build
    ```
3.  **Abre tu navegador**:
    ```bash
    http:localhost:8000/
    ```