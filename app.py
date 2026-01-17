from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import unicodedata
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "iago_aspas"

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Llamar a init_db al iniciar la aplicación
init_db()

# Lista de palabras
palabras = [
    "arbol", "boca", "bruja", "casa", "cabra", "cafe", "campana", "caramelos", "clavo",
    "cuchara", "dedo", "ducha", "escoba", "flan", "fresa", "fuma", "gafas", "globo",
    "gorro", "grifo", "indio", "jarra", "jaula", "lapiz", "lavadora", "llaves", "luna",
    "mar", "mariposa", "moto", "niño", "ojo", "pala", "palmera", "pan", "peine",
    "periodico", "pez", "piano", "pie", "piña", "pistola", "platano", "preso", "pueblo",
    "puerta", "rata", "semaforo", "silla", "sol", "tambor", "telefono", "toalla", "toro",
    "tortuga", "tren", "zapato"
]

# Diccionario de fonemas
fonemas = {
    "arbol": ["a", "r", "b", "o", "l"],
    "boca": ["b", "o", "c", "a"],
    "bruja": ["b", "r", "u", "j", "a"],
    "casa": ["c", "a", "s", "a"],
    "cabra": ["c", "a", "b", "r", "a"],
    "cafe": ["c", "a", "f", "e"],
    "campana": ["c", "a", "m", "p", "a", "n", "a"],
    "caramelos": ["c", "a", "r", "a", "m", "e", "l", "o", "s"],
    "clavo": ["c", "l", "a", "v", "o"],
    "cuchara": ["c", "u", "ch", "a", "r", "a"],
    "dedo": ["d", "e", "d", "o"],
    "ducha": ["d", "u", "ch", "a"],
    "escoba": ["e", "s", "c", "o", "b", "a"],
    "flan": ["f", "l", "a", "n"],
    "fresa": ["f", "r", "e", "s", "a"],
    "fuma": ["f", "u", "m", "a"],
    "gafas": ["g", "a", "f", "a", "s"],
    "globo": ["g", "l", "o", "b", "o"],
    "gorro": ["g", "o", "rr", "o"],
    "grifo": ["g", "r", "i", "f", "o"],
    "indio": ["i", "n", "d", "i", "o"],
    "jarra": ["j", "a", "rr", "a"],
    "jaula": ["j", "a", "u", "l", "a"],
    "lapiz": ["l", "a", "p", "i", "z"],
    "lavadora": ["l", "a", "v", "a", "d", "o", "r", "a"],
    "llaves": ["ll", "a", "v", "e", "s"],
    "luna": ["l", "u", "n", "a"],
    "mar": ["m", "a", "r"],
    "mariposa": ["m", "a", "r", "i", "p", "o", "s", "a"],
    "moto": ["m", "o", "t", "o"],
    "niño": ["n", "i", "ñ", "o"],
    "ojo": ["o", "j", "o"],
    "pala": ["p", "a", "l", "a"],
    "palmera": ["p", "a", "l", "m", "e", "r", "a"],
    "pan": ["p", "a", "n"],
    "peine": ["p", "e", "i", "n", "e"],
    "periodico": ["p", "e", "r", "i", "o", "d", "i", "c", "o"],
    "pez": ["p", "e", "z"],
    "piano": ["p", "i", "a", "n", "o"],
    "pie": ["p", "i", "e"],
    "pina": ["p", "i", "ñ", "a"],
    "pistola": ["p", "i", "s", "t", "o", "l", "a"],
    "platano": ["p", "l", "a", "t", "a", "n", "o"],
    "preso": ["p", "r", "e", "s", "o"],
    "pueblo": ["p", "u", "e", "b", "l", "o"],
    "puerta": ["p", "u", "e", "r", "t", "a"],
    "rata": ["r", "a", "t", "a"],
    "semaforo": ["s", "e", "m", "a", "f", "o", "r", "o"],
    "silla": ["s", "i", "ll", "a"],
    "sol": ["s", "o", "l"],
    "tambor": ["t", "a", "m", "b", "o", "r"],
    "telefono": ["t", "e", "l", "e", "f", "o", "n", "o"],
    "toalla": ["t", "o", "a", "ll", "a"],
    "toro": ["t", "o", "r", "o"],
    "tortuga": ["t", "o", "r", "t", "u", "g", "a"],
    "tren": ["t", "r", "e", "n"],
    "zapato": ["z", "a", "p", "a", "t", "o"]
}

def comparar_fonemas(objetivo, produccion):
    if not produccion or produccion.strip() == "":
        return {"produccion": "", "errores": ["No producido"], "correcto": False}

    objetivo_norm = unicodedata.normalize('NFKD', objetivo.lower()).encode('ASCII', 'ignore').decode('ASCII')
    produccion_norm = unicodedata.normalize('NFKD', produccion.lower()).encode('ASCII', 'ignore').decode('ASCII')

    fonemas_obj = fonemas.get(objetivo_norm, list(objetivo_norm))
    fonemas_prod = list(produccion_norm)

    errores = []
    correcto = True
    i_obj = 0  # Índice para fonemas objetivo
    i_prod = 0  # Índice para fonemas producción

    while i_obj < len(fonemas_obj) and i_prod < len(fonemas_prod):
        fonema_obj = fonemas_obj[i_obj]
        fonema_prod = fonemas_prod[i_prod]

        if fonema_obj == fonema_prod:
            # Fonemas coinciden, avanzar ambos índices
            i_obj += 1
            i_prod += 1
        else:
            # Verificar si es una omisión en el objetivo
            if i_obj + 1 < len(fonemas_obj) and fonemas_obj[i_obj + 1] == fonema_prod:
                errores.append(f"Omisión en posición {i_obj + 1}: {fonema_obj}")
                correcto = False
                i_obj += 1
            # Verificar si es una adición en la producción
            elif i_prod + 1 < len(fonemas_prod) and fonemas_prod[i_prod + 1] == fonema_obj:
                errores.append(f"Adición en posición {i_obj + 1}: {fonema_prod}")
                correcto = False
                i_prod += 1
            else:
                # Sustitución
                errores.append(f"Sustitución en posición {i_obj + 1}: {fonema_obj} → {fonema_prod}")
                correcto = False
                i_obj += 1
                i_prod += 1

    # Maneja fonemas restantes en objetivo (omisiones)
    while i_obj < len(fonemas_obj):
        errores.append(f"Omisión en posición {i_obj + 1}: {fonemas_obj[i_obj]}")
        correcto = False
        i_obj += 1

    # Maneja fonemas restantes en producción (adiciones)
    while i_prod < len(fonemas_prod):
        errores.append(f"Adición en posición {i_obj + 1}: {fonemas_prod[i_prod]}")
        correcto = False
        i_prod += 1

    if not errores:
        errores = ["Correcto"]

    return {
        "produccion": produccion,
        "errores": errores,
        "correcto": correcto
    }

@app.route('/')
def home():
       return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('register.html')

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                        (name, email, hashed_password))
            conn.commit()
            conn.close()
            flash('Registro exitoso. Ahora puedes continuar.', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('El email ya está registrado.', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html', palabras=palabras)

@app.route('/analizar', methods=['POST'])
def analizar():
    resultados = {"espontanea": {}, "repeticion": {}}
    aciertos_esp = 0
    aciertos_rep = 0
    total_palabras = len(palabras)

    for palabra in palabras:
        espontanea = request.form.get(f'espontanea_{palabra}')
        repeticion = request.form.get(f'repeticion_{palabra}')

        if espontanea:
            res_esp = comparar_fonemas(palabra, espontanea)
            resultados["espontanea"][palabra] = res_esp
            if res_esp["correcto"]:
                aciertos_esp += 1

        if repeticion:
            res_rep = comparar_fonemas(palabra, repeticion)
            resultados["repeticion"][palabra] = res_rep
            if res_rep["correcto"]:
                aciertos_rep += 1

    total_esp = len(resultados["espontanea"])
    total_rep = len(resultados["repeticion"])
    pct_esp = (aciertos_esp / total_esp * 100) if total_esp > 0 else 0
    pct_rep = (aciertos_rep / total_rep * 100) if total_rep > 0 else 0

    resumen = {
        "aciertos_esp": aciertos_esp,
        "total_esp": total_esp,
        "pct_esp": round(pct_esp, 2),
        "aciertos_rep": aciertos_rep,
        "total_rep": total_rep,
        "pct_rep": round(pct_rep, 2)
    }

    # Guardar resultados en la sesión para el PDF
    session['resultados'] = resultados
    session['resumen'] = resumen

    return render_template('results.html', resultados=resultados, resumen=resumen, palabras=palabras)

from flask import session

@app.route('/descargar_pdf')
def descargar_pdf():
    resultados = session.get('resultados', {"espontanea": {}, "repeticion": {}})
    resumen = session.get('resumen', {
        "aciertos_esp": 0, "total_esp": 0, "pct_esp": 0,
        "aciertos_rep": 0, "total_rep": 0, "pct_rep": 0
    })

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontSize = 8
    normal_style.leading = 10

    elements.append(Paragraph("Resultados del Análisis Fonológico", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Espontánea: {resumen['aciertos_esp']} / {resumen['total_esp']} correctas ({resumen['pct_esp']}%)", normal_style))
    elements.append(Paragraph(f"Repetición: {resumen['aciertos_rep']} / {resumen['total_rep']} correctas ({resumen['pct_rep']}%)", normal_style))
    elements.append(Spacer(1, 12))

    data = [["Palabra", "Espontánea", "Repetición"]]
    for palabra in palabras:
        esp = resultados["espontanea"].get(palabra, {"produccion": "No ingresado", "errores": [""]})
        rep = resultados["repeticion"].get(palabra, {"produccion": "No ingresado", "errores": [""]})
        esp_text = f"Producción: {esp['produccion']}\nErrores: {', '.join(esp['errores'])}"
        rep_text = f"Producción: {rep['produccion']}\nErrores: {', '.join(rep['errores'])}"
        data.append([
            Paragraph(palabra, normal_style),
            Paragraph(esp_text, normal_style),
            Paragraph(rep_text, normal_style)
        ])

    # Definir anchos de columna para ajustar a la página (letter: 612x792 puntos)
    col_widths = [100, 230, 230]  # Total: 560 puntos, dejando márgenes
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK')  # Ajuste de texto
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resultados_rfi.pdf'
    return response
