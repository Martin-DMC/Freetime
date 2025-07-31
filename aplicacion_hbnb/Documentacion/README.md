# Documentación del Proyecto

## Diagramas del Sistema

### Diagrama de Clases
Este diagrama define la estructura del sistema, mostrando las clases principales y sus relaciones. Representa los atributos y métodos de cada entidad, junto con las relaciones clave:

- **Herencia:** `User`, `Place`, `Review` y `Amenity` heredan de `Base`, compartiendo atributos fundamentales.
- **Agregación:** `User` posee varios `Place`, mientras que `Place` agrupa múltiples `Amenity`.
- **Composición:** `Place` está compuesto por varias `Review`, lo que indica una relación fuerte de dependencia.
- **Asociación:** `User` escribe `Review`, estableciendo una relación directa sin control total sobre su ciclo de vida.

---

### Diagrama de Paquetes
Organiza las clases en módulos lógicos, mejorando la modularidad y estructura del código. Los paquetes clave son:

---

## Diagramas de Secuencia

### Listar Lugares
Este diagrama representa el flujo para obtener lugares según criterios de filtro:

- **Caso exitoso** → Se envían los filtros y el sistema devuelve una lista de lugares (`200 OK`).
- **Lista vacía** → No hay coincidencias, pero la consulta es válida (`200 OK`).
- **Error interno** → Fallo en la base de datos (`500 Internal Server Error`).

---

### Crear un Lugar
Define el proceso de creación de un nuevo lugar en la plataforma:

1. El cliente envía datos a la API.
2. La API valida la información y la almacena en la base de datos.
3. Si todo es correcto, devuelve `201 Created`.

**Errores posibles:**
- Problemas de validación (`400 Bad Request`).
- Fallo interno en el servidor (`500 Internal Server Error`).

---

### Crear una Reseña
Ilustra el proceso de publicación de una reseña, mostrando errores primero y luego el éxito:

- **Flujo principal:**
  - El cliente envía datos a la API.
  - La API valida la información con la Lógica de Negocio.

**Resultados posibles:**
- Error de validación (`400 Bad Request`).
- Fallo en el guardado (`500 Internal Server Error`).
- Éxito al guardar (`200 OK`).

---

### Crear un Usuario
Muestra el proceso completo de registro de usuario:

1. El cliente envía los datos a la API.
2. La capa `Business Logic` verifica la información.

**Resultados posibles:**
- Datos válidos → Usuario guardado (`201 Created`).
- Datos incorrectos → Error de validación (`400 Bad Request`).
- Fallo en la base de datos → Error interno (`500 Internal Server Error`).
