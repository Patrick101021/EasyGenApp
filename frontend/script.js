function mostrarRegistro() {
    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("registerSection").classList.remove("hidden");
    document.getElementById("generadorSection").classList.add("hidden");
}

function mostrarLogin() {
    document.getElementById("registerSection").classList.add("hidden");
    document.getElementById("loginSection").classList.remove("hidden");
    document.getElementById("generadorSection").classList.add("hidden");
}

function mostrarGenerador() {
    document.getElementById("registerSection").classList.add("hidden");
    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("generadorSection").classList.remove("hidden");
}

function cerrarSesion() {
    alert("Sesión cerrada.");
    document.getElementById("descripcion").value = "";
    document.getElementById("resultado").textContent = "";
    mostrarLogin();
}

const baseUrl = "https://easygenapp-de607d464285.herokuapp.com";  // Cambié la URL base para producción

async function registrarUsuario() {
    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("emailRegistro").value.trim();
    const password = document.getElementById("passwordRegistro").value;

    if (!nombre || !email || !password) {
        alert("Completa todos los campos.");
        return;
    }

    try {
        const response = await fetch(`${baseUrl}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Registro exitoso. Ahora inicia sesión.");
            mostrarLogin();
        } else {
            alert(data.error || "Error al registrarse.");
        }
    } catch (error) {
        alert("Error de conexión con el servidor.");
    }
}

async function iniciarSesion() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Completa todos los campos.");
        return;
    }

    try {
        const response = await fetch(`${baseUrl}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Inicio de sesión exitoso.");
            mostrarGenerador();
        } else {
            alert(data.error || "Credenciales incorrectas.");
        }
    } catch (error) {
        alert("Error de conexión con el servidor.");
    }
}

async function generarCodigo() {
    const descripcion = document.getElementById("descripcion").value.trim();
    const resultado = document.getElementById("resultado");

    if (!descripcion) {
        alert("Debes escribir una descripción para generar el código.");
        return;
    }

    resultado.textContent = "⏳ Generando código, por favor espera...";

    try {
        const response = await fetch(`${baseUrl}/generar_codigo`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ descripcion })
        });

        const data = await response.json();
        if (response.ok) {
            resultado.textContent = data.codigo;
        } else {
            resultado.textContent = data.error || "Error al generar el código.";
        }
    } catch (error) {
        resultado.textContent = "❌ Error de conexión con el servidor.";
    }
}

