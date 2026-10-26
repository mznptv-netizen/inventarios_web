#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INVENTARIOS_IPSICOL - Servidor Web Local (Flask), SQLite.

Ejecutar localmente: python ipsicol.py
Acceso en red local: http://<IP-DEL-SERVIDOR>:5000
"""

from __future__ import annotations

import base64
import calendar
import io
import logging
import os
import re
import shutil
import sqlite3
import sys
import uuid
from datetime import date, datetime
from pathlib import Path

# Importación para el servidor web incrustado
from flask import Flask, render_template_string, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.secret_key = os.urandom(24)

APP_NAME = "INVENTARIOS_IPSICOL"
REGIONALES = ("Bogotá", "Cundinamarca")
UBICACIONES = ("REDENTOR", "CIPLA", "CAJICA", "ESMERALDA")
NO_SOPORTE = "No es necesario"
TODOS = "Todos"
MAGENTA = "#BF1672"
MAGENTA_HOVER = "#99115B"
BG = "#F6F3F7"
INK = "#302637"
MUTED = "#605567"
WHITE = "#FFFFFF"
MAX_CANTIDAD = 2_000_000_000

# Base de datos local segura en AppData de Windows
def data_directory() -> Path:
    if sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    else:
        root = Path.home() / ".local" / "share"
    folder = root / APP_NAME
    folder.mkdir(parents=True, exist_ok=True)
    return folder

DB_PATH = data_directory() / "ipsicol.db"

def validate_support(path: Path):
    if not path.is_file():
        raise ValueError("El archivo ya no existe. Selecciónalo nuevamente.")
    if not 0 < path.stat().st_size <= 25 * 1024 * 1024:
        raise ValueError("El archivo debe tener contenido y no superar 25 MB.")

def required_text(value: str, field: str, limit: int = 180) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"Completa el campo {field}.")
    if len(value) > limit:
        raise ValueError(f"{field}: máximo {limit} caracteres.")
    return value

def quantity(value) -> int:
    text = str(value).strip()
    if not re.fullmatch(r"[0-9]{1,10}", text):
        raise ValueError("La cantidad debe ser un número entero positivo.")
    number = int(text)
    if not 1 <= number <= MAX_CANTIDAD:
        raise ValueError(f"La cantidad debe estar entre 1 y {MAX_CANTIDAD:,}.")
    return number

# Inicializador de base de datos SQLite segura con WAL mode para concurrencia
def get_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS regionales (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS inventarios (
            id INTEGER PRIMARY KEY,
            regional_id INTEGER NOT NULL REFERENCES regionales(id),
            nombre TEXT NOT NULL,
            nombre_clave TEXT NOT NULL,
            creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            eliminado INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            inventario_id INTEGER NOT NULL REFERENCES inventarios(id),
            objeto TEXT NOT NULL,
            objeto_clave TEXT NOT NULL,
            cantidad_inicial INTEGER NOT NULL,
            salidas_totales INTEGER NOT NULL DEFAULT 0,
            cantidad_actual INTEGER NOT NULL,
            eliminado INTEGER NOT NULL DEFAULT 0
        );
        INSERT OR IGNORE INTO regionales(nombre) VALUES ('Bogotá'), ('Cundinamarca');
    """)
    conn.close()

# --- Rutas de la Aplicación Web (Flask) ---
@app.route("/")
def index():
    conn = get_db()
    inventarios = conn.execute("SELECT i.*, r.nombre as regional_nombre FROM inventarios i JOIN regionales r ON r.id = i.regional_id WHERE i.eliminado = 0").fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Inventarios IPSICOL</title>
        <style>
            body { font-family: Arial, sans-serif; background: #F6F3F7; color: #302637; margin: 0; padding: 20px; }
            h1 { color: #BF1672; }
            table { width: 100%; border-collapse: collapse; background: white; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #BF1672; color: white; }
            .btn { background: #BF1672; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; }
            .btn:hover { background: #99115B; }
        </style>
    </head>
    <body>
        <h1>Inventarios IPSICOL - Panel de Control</h1>
        <a class="btn" href="/nuevo_inventario">Crear Nuevo Inventario</a>
        <table>
            <tr><th>ID</th><th>Regional</th><th>Nombre</th><th>Fecha Creación</th></tr>
            {% for inv in inventarios %}
            <tr>
                <td>{{ inv.id }}</td>
                <td>{{ inv.regional_nombre }}</td>
                <td>{{ inv.nombre }}</td>
                <td>{{ inv.creado_en }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, inventarios=inventarios)

@app.route("/nuevo_inventario", methods=["GET", "POST"])
def nuevo_inventario():
    if request.method == "POST":
        regional_id = request.form.get("regional_id")
        nombre = request.form.get("nombre")
        try:
            conn = get_db()
            conn.execute("INSERT INTO inventarios (regional_id, nombre, nombre_clave) VALUES (?, ?, ?)",
                         (regional_id, nombre, nombre.casefold()))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        except Exception as e:
            return f"Error al guardar: {e}"
            
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Nuevo Inventario</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Crear Inventario</h2>
        <form method="POST">
            <label>Regional:</label><br>
            <select name="regional_id">
                <option value="1">Bogotá</option>
                <option value="2">Cundinamarca</option>
            </select><br><br>
            <label>Nombre del Inventario:</label><br>
            <input type="text" name="nombre" required style="width: 300px; padding: 8px;"><br><br>
            <button type="submit" style="background: #BF1672; color: white; padding: 10px 15px; border: none;">Guardar</button>
        </form>
        <br><a href="/">Volver</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    init_db()
    # Se ejecuta abierto en la red local para que otros ordenadores accedan por IP
    app.run(host="0.0.0.0", port=5000, debug=False)
