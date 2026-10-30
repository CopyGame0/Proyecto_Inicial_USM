// Abre la receta completa en una ventana emergente, sin salir de la página.
// Lo usan tanto el formulario como la página /plan/.


//entiedno super poco JS pero funciona bien asiq NO SE TOCA ESTO//

const dialogo = document.getElementById("detalle");
const contenido = document.getElementById("detalle-contenido");

document.addEventListener("click", async (evento) => {
    // 1) Click en "Ver receta" -> abrir la ventana y cargar la receta
    const boton = evento.target.closest(".ver-receta");
    if (boton) {
        contenido.innerHTML = '<p class="cargando">Cargando receta...</p>';
        dialogo.showModal();
        try {
            const respuesta = await fetch(boton.dataset.url);
            contenido.innerHTML = await respuesta.text();
        } catch (error) {
            contenido.innerHTML = '<p class="mensaje-error">No se pudo cargar la receta. Intente de nuevo.</p>';
        }
        return;
    }

    // 2) Click en "Cerrar" o en el fondo oscuro -> cerrar la ventana
    if (evento.target.closest(".cerrar-detalle") || evento.target === dialogo) {
        dialogo.close();
    }
});
