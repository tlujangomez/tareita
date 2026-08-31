async def obtener_autores(conn) -> list[dict]:
    rows = await conn.fetch("SELECT * FROM autores ORDER BY id")
    return [dict(row) for row in rows]


async def obtener_autor(conn, autor_id: int) -> dict | None:
    row = await conn.fetchrow("SELECT * FROM autores WHERE id = $1", autor_id)
    return dict(row) if row else None


async def crear_autor(conn, nombre: str, pais: str | None, nacimiento: int | None) -> dict:
    row = await conn.fetchrow(
        "INSERT INTO autores (nombre, pais, nacimiento) VALUES ($1, $2, $3) RETURNING *",
        nombre,
        pais,
        nacimiento,
    )
    return dict(row)


async def actualizar_autor(
    conn, autor_id: int, nombre: str, pais: str | None, nacimiento: int | None
) -> dict | None:
    row = await conn.fetchrow(
        "UPDATE autores SET nombre = $1, pais = $2, nacimiento = $3 WHERE id = $4 RETURNING *",
        nombre,
        pais,
        nacimiento,
        autor_id,
    )
    return dict(row) if row else None


async def eliminar_autor(conn, autor_id: int) -> bool:
    result = await conn.execute("DELETE FROM autores WHERE id = $1", autor_id)
    return result == "DELETE 1"


async def upsert_autores_bulk(
    conn, registros: list[dict], *, tabla: str = "autores"
) -> int:
    """Inserta o actualiza (UPSERT) autores en bulk en ``tabla``.

    Cada registro debe ser un dict con las claves: ``id``, ``nombre``, ``pais``,
    ``nacimiento``. ``pais`` y ``nacimiento`` pueden ser ``None``.

    La ``tabla`` debe tener la misma estructura que ``autores`` (columnas
    ``id``, ``nombre``, ``pais``, ``nacimiento``). Se valida el nombre para
    evitar inyección SQL.
    """
    if not tabla.replace("_", "").isalnum():
        raise ValueError(f"Nombre de tabla inválido: {tabla!r}")
    sql = f"""
        INSERT INTO {tabla} (id, nombre, pais, nacimiento)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (id) DO UPDATE
        SET nombre = EXCLUDED.nombre,
            pais = EXCLUDED.pais,
            nacimiento = EXCLUDED.nacimiento
    """
    count = 0
    async with conn.transaction():
        for r in registros:
            await conn.execute(
                sql,
                r["id"],
                r["nombre"],
                r.get("pais"),
                r.get("nacimiento"),
            )
            count += 1
    return count
async def obtener_libros(conn) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT
            libros.id,
            libros.titulo,
            libros.autor_id,
            autores.nombre AS autor
        FROM libros
        INNER JOIN autores ON libros.autor_id = autores.id
        ORDER BY libros.id
        """
    )
    return [dict(row) for row in rows]

async def obtener_libros_autor(conn, autor_id: int) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT
            libros.id,
            libros.titulo,
            STRING_AGG(autores.nombre, ', ' ORDER BY autores.nombre) AS autores
        FROM libros
        INNER JOIN autor_libro
            ON libros.id = autor_libro.libro_id
        INNER JOIN autores
            ON autor_libro.autor_id = autores.id
        WHERE libros.id IN (
            SELECT libro_id
            FROM autor_libro
            WHERE autor_id = $1
        )
        GROUP BY libros.id, libros.titulo
        ORDER BY libros.id
        """,
        autor_id,
    )

    return [dict(row) for row in rows]