"""
Quiz #4 - NoSQL (CE 2103)
Base de datos tipo llave-valor (Redis) usada desde Python.

Escenario: mini backend de un servicio de streaming (tipo Tecflix) que usa
Redis para: cache de metadatos de videos, contador de vistas, ranking de
mas vistos y sesiones de usuario con expiracion.
"""
import json
import time
import uuid

import redis

# Conexion a Redis (el contenedor de docker-compose lo expone en el 6379)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


# ---------- 1. Cache de metadatos de videos (hash) ----------
def guardar_video(video_id, titulo, genero, duracion_min):
    # Un hash es como un diccionario guardado bajo una sola llave
    r.hset(f"video:{video_id}", mapping={
        "titulo": titulo,
        "genero": genero,
        "duracion_min": duracion_min,
    })


def obtener_video(video_id):
    datos = r.hgetall(f"video:{video_id}")
    return datos if datos else None


# ---------- 2. Contador de vistas + ranking (string/INCR y sorted set) ----------
def registrar_vista(video_id):
    r.incr(f"vistas:{video_id}")             # contador atomico
    r.zincrby("ranking:vistas", 1, video_id)  # actualiza el ranking


def top_videos(n=3):
    ranking = r.zrevrange("ranking:vistas", 0, n - 1, withscores=True)
    resultado = []
    for video_id, vistas in ranking:
        video = obtener_video(video_id)
        titulo = video["titulo"] if video else "(desconocido)"
        resultado.append((titulo, int(vistas)))
    return resultado


# ---------- 3. Sesiones con expiracion (string con TTL) ----------
def crear_sesion(usuario, segundos=5):
    token = str(uuid.uuid4())
    r.set(f"sesion:{token}", json.dumps({"usuario": usuario}), ex=segundos)
    return token


def validar_sesion(token):
    datos = r.get(f"sesion:{token}")
    return json.loads(datos) if datos else None


# ---------- 4. Lista de reproduccion reciente (list) ----------
def agregar_historial(usuario, video_id, maximo=3):
    r.lpush(f"historial:{usuario}", video_id)
    r.ltrim(f"historial:{usuario}", 0, maximo - 1)  # solo deja los ultimos


def ver_historial(usuario):
    return r.lrange(f"historial:{usuario}", 0, -1)


def main():
    r.flushdb()  # limpiar para que la demo sea repetible

    print("=== 1. Guardando videos ===")
    guardar_video("v1", "Interestelar", "Ciencia ficcion", 169)
    guardar_video("v2", "Coco", "Animacion", 105)
    guardar_video("v3", "El Padrino", "Drama", 175)
    print(obtener_video("v1"))
    print("Video que no existe:", obtener_video("v99"))

    print("\n=== 2. Vistas y ranking ===")
    for vid in ["v1", "v2", "v2", "v3", "v2", "v1"]:
        registrar_vista(vid)
    print("Vistas de v2:", r.get("vistas:v2"))
    for i, (titulo, vistas) in enumerate(top_videos(), start=1):
        print(f"{i}. {titulo} - {vistas} vistas")

    print("\n=== 3. Sesiones con expiracion ===")
    token = crear_sesion("pablo", segundos=3)
    print("Sesion valida:", validar_sesion(token))
    print("Esperando 4 segundos...")
    time.sleep(4)
    print("Despues de expirar:", validar_sesion(token))

    print("\n=== 4. Historial de reproduccion ===")
    for vid in ["v1", "v2", "v3", "v1"]:
        agregar_historial("pablo", vid)
    print("Ultimos videos vistos:", ver_historial("pablo"))


if __name__ == "__main__":
    main()
