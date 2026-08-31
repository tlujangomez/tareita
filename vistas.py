from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from dependencias import ConnectionDep
from esquemas import AutorActualizar, AutorCrear
from repositorio import (
    actualizar_autor,
    crear_autor,
    eliminar_autor,
    obtener_autor,
    obtener_autores,
    obtener_libros,
    obtener_libros_autor,
)

router = APIRouter(tags=["vistas"])

@router.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="inicio.html",
        context={},
    )



templates = Jinja2Templates(directory="templates")


@router.get("/autores")
async def listar_autores(request: Request, conn: ConnectionDep):
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="autores.html",
        context={"autores": autores},
    )


@router.post("/autores")
async def crear_autor_vista(
    request: Request,
    conn: ConnectionDep,
    nombre: str = Form(),
    pais: str | None = Form(default=None),
    nacimiento: int | None = Form(default=None),
):
    autor = AutorCrear(nombre=nombre, pais=pais, nacimiento=nacimiento)
    await crear_autor(conn, autor.nombre, autor.pais, autor.nacimiento)
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_autores.html",
        context={"autores": autores},
    )


@router.get("/autores/{autor_id}/editar")
async def editar_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_editar_autor.html",
        context={"autor": autor},
    )


@router.get("/autores/{autor_id}/cancelar")
async def cancelar_edicion_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autor.html",
        context={"autor": autor},
    )


@router.put("/autores/{autor_id}")
async def actualizar_autor_vista(
    request: Request,
    conn: ConnectionDep,
    autor_id: int,
    nombre: str = Form(),
    pais: str | None = Form(default=None),
    nacimiento: int | None = Form(default=None),
):
    autor = AutorActualizar(nombre=nombre, pais=pais, nacimiento=nacimiento)
    await actualizar_autor(conn, autor_id, autor.nombre, autor.pais, autor.nacimiento)
    autor_actualizado = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autor.html",
        context={"autor": autor_actualizado},
    )


@router.delete("/autores/{autor_id}")
async def eliminar_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    await eliminar_autor(conn, autor_id)
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_autores.html",
        context={"autores": autores},
    )
@router.get("/libros")
async def listar_libros(request: Request, conn: ConnectionDep):
    libros = await obtener_libros(conn)

    return templates.TemplateResponse(
        request=request,
        name="libros.html",
        context={"libros": libros},
    )
@router.get("/autores/{autor_id}/libros")
async def mostrar_libros_autor(
    request: Request,
    conn: ConnectionDep,
    autor_id: int,
):
    libros = await obtener_libros_autor(conn, autor_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/libros_autor.html",
        context={
            "libros": libros,
            "autor_id": autor_id,
        },
    )
@router.get("/autores/{autor_id}/ocultar-libros")
async def ocultar_libros_autor(
    request: Request,
    autor_id: int,
):
    return templates.TemplateResponse(
        request=request,
        name="partials/libros_ocultos.html",
        context={},
    )