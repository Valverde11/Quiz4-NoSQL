# Quiz #4 - NoSQL (CE 2103)

**Instituto Tecnológico de Costa Rica**  
**Curso:** Algoritmos y Estructuras de Datos II  
**Semestre:** II Semestre 2026

### Integrantes
- José Pablo Valverde Durán
- Juan José Rodríguez Chaves

## 1. Tipo de base de datos elegida

Para este trabajo elegimos una base de datos de tipo **llave-valor**, utilizando **Redis** desde Python.

## 2. Escenario (contexto del problema)

Para este ejemplo imaginamos que estamos trabajando en el backend de una plataforma de streaming parecida a la del proyecto.

En una plataforma de este tipo hay muchos usuarios consultando información de películas y series al mismo tiempo. Además, existen datos que se actualizan constantemente. Algunos ejemplos son:

- La información de cada video, como el título, género y duración, que se muestra cuando un usuario entra a ver una película.
- La cantidad de reproducciones de cada video, que aumenta cada vez que alguien lo ve.
- Un ranking para mostrar cuáles son los videos más populares.
- Las sesiones de los usuarios, que deben cerrarse automáticamente después de cierto tiempo.
- Un historial con los últimos videos que ha visto cada usuario.

Si utilizáramos solamente una base de datos relacional para manejar todo esto, tendríamos que realizar muchas consultas y actualizaciones constantemente. Por eso consideramos que Redis es una buena opción, ya que permite guardar y consultar información rápidamente utilizando llaves.

## 3. ¿Cómo utilizamos Redis para resolver el problema?

Para cada una de las necesidades anteriores utilizamos diferentes estructuras que ofrece Redis:

| Necesidad | Estructura de Redis | Comandos utilizados | Ejemplo de llave |
|---|---|---|---|
| Guardar información de los videos | Hash | `HSET`, `HGETALL` | `video:v1` |
| Contar las reproducciones | String | `INCR` | `vistas:v1` |
| Crear un ranking de videos más vistos | Sorted Set | `ZINCRBY`, `ZREVRANGE` | `ranking:vistas` |
| Guardar sesiones con tiempo de expiración | String con TTL | `SET ... EX`, `GET` | `sesion:<token>` |
| Guardar los últimos videos vistos | List | `LPUSH`, `LTRIM`, `LRANGE` | `historial:pablo` |

Una de las cosas que nos parecieron más útiles de Redis es que tiene comandos que facilitan bastante el manejo de estos datos.

Por ejemplo, `INCR` permite aumentar un contador de forma atómica, lo que evita que se pierdan reproducciones cuando varios usuarios ven el mismo video al mismo tiempo.

También utilizamos `SET` con `EX` para establecer cuánto tiempo puede mantenerse activa una sesión. Cuando se cumple ese tiempo, Redis elimina automáticamente la llave, sin necesidad de hacerlo manualmente.

Otra cosa que utilizamos fue una forma de nombrar las llaves siguiendo el formato `tipo:id`. Esto ayuda a mantener la información más ordenada y facilita encontrar los datos que necesitamos.

### Limitaciones

Aunque Redis tiene varias ventajas, también tiene algunas limitaciones. Por ejemplo, no permite realizar consultas complejas ni manejar relaciones entre diferentes datos de la misma forma que una base de datos relacional.

Por esta razón, consideramos que Redis funciona muy bien como complemento de una base de datos principal, especialmente para manejar caché, contadores, sesiones e información que se consulta frecuentemente.

## 4. Estructura del repositorio

El proyecto está organizado en los siguientes archivos:

```text
main.py              # Contiene las funciones y una demostración
docker-compose.yml   # Permite levantar Redis utilizando Docker
```

## 5. ¿Cómo ejecutar el programa?

Para probar el programa es necesario tener Docker y Python instalados.

**1.** Primero levantamos el servidor de Redis utilizando Docker:

```bash
docker compose up -d
```

**2.** Instalamos la librería necesaria para conectar Python con Redis:

```bash
pip install redis
```

**3.** Finalmente ejecutamos el programa:

```bash
python main.py
```

## 6. Salida esperada

Al ejecutar el programa, se espera obtener una salida similar a la siguiente:

```text
=== 2. Vistas y ranking ===
1. Coco - 3 vistas
2. Interestelar - 2 vistas
3. El Padrino - 1 vistas

=== 3. Sesiones con expiracion ===
Sesion valida: {'usuario': 'pablo'}
Despues de expirar: None
```

## 7. Conclusión

Con este ejemplo pudimos conocer cómo funciona una base de datos NoSQL de tipo llave-valor utilizando Redis y Python. También vimos que Redis permite trabajar con diferentes estructuras, como Hash, List y Sorted Set, dependiendo de lo que necesitemos almacenar.

En nuestro caso, nos pareció una buena alternativa para una plataforma como Tecflix, porque permite acceder rápidamente a información que se consulta y actualiza constantemente. Sin embargo, también hay que tomar en cuenta sus limitaciones, por lo que no necesariamente reemplaza una base de datos relacional, sino que puede trabajar junto a ella para mejorar el rendimiento del sistema.