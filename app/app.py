"""Aplicación web de la calculadora."""

import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from .calculadora import sumar, restar, multiplicar, dividir, potencia, modulo

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(app)

# Cada operación del formulario apunta a su función (evita una cadena de if/elif)
OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
    "modulo": modulo,
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Renderiza la calculadora y procesa las operaciones enviadas."""
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            funcion = OPERACIONES.get(request.form["operacion"])

            if funcion is None:
                resultado = "Operación no válida"
            else:
                resultado = funcion(num1, num2)
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"
        except OverflowError:
            resultado = "Error: El resultado es demasiado grande"

    return render_template("index.html", resultado=resultado)


@app.route("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=False, port=5000, host="127.0.0.1")
