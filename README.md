# RFI Analyzer - Herramienta de Evaluación Fonológica

#### Vídeo de demostración: [Insertar URL de YouTube aquí]

#### Descripción

**RFI Analyzer** es una aplicación web diseñada para facilitar la evaluación del desarrollo fonológico en niños de habla hispana mediante el **Registro Fonológico Inducido (RFI)**.

Como exmaestro de Audición y Lenguaje, durante años realicé estas evaluaciones en papel: mostrar imágenes, anotar lo que decía el niño, transcribir, comparar con los fonemas esperados y redactar informes manualmente. Era un proceso lento, propenso a errores y difícil de archivar o compartir.

Este proyecto nace precisamente de esa necesidad no cubierta: tener una herramienta digital, rápida, accesible desde cualquier dispositivo y que genere informes automáticamente.

### Características principales

- Formulario con las 50 palabras clásicas del RFI + imágenes asociadas
- Registro de respuestas en **producción espontánea** y **repetición**
- Análisis automático de errores fonológicos (omisiones, sustituciones, adiciones)
- Detección correcta de omisiones en posición intermedia (ej: "bruja" → "buja" → Omisión en posición 2: r)
- Cálculo de porcentaje de aciertos en cada modalidad
- Generación y descarga de informe PDF profesional con tabla legible
- Registro de usuarios opcional (SQLite + bcrypt)
- Botón "Continuar sin registro" para acceso inmediato
- Diseño responsive (funciona bien en móvil y tablet)

### Tecnologías utilizadas

- Backend: **Flask** (Python)
- Base de datos: **SQLite** (ligera, sin servidor externo)
- Autenticación: contraseñas hasheadas con **bcrypt**
- Generación PDF: **ReportLab** (tablas con ajuste automático de texto)
- Frontend: HTML + Jinja2 + CSS puro (responsive)
- Imágenes: 50 archivos .png en carpeta `static/images/`

### Decisiones de diseño importantes

- **Registro opcional** → prioridad de usabilidad. Muchos logopedas quieren probar la herramienta sin crear cuenta.
- **Análisis en servidor** → más fiable y fácil de mantener que hacerlo en JavaScript.
- **Detección de omisiones** → la parte más delicada. Se utilizó comparación con dos índices para alinear correctamente secuencias cuando falta un fonema.
- **PDF legible** → muchas iteraciones hasta encontrar anchos de columna fijos + tamaño de letra 8 + márgenes 30pt + Paragraph para wrap automático.

### Limitaciones actuales y posibles mejoras

- Solo español castellano estándar (no contempla seseo/ceceo ni otros dialectos)
- No guarda historial de evaluaciones (solo las del momento)
- No hay sistema de login completo ni recuperación de contraseña

Posibles evoluciones:
- Guardar evaluaciones asociadas al usuario
- Gráficos de evolución (Chart.js)
- Sugerencias de intervención según patrones de error
- Soporte multilingüe o variantes dialectales

### Licencia

MIT License

### Autor

Gustavo Álvarez Sánchez
Exmaestro de Audición y Lenguaje  
Desarrollador web autodidacta

¡Gracias por visitar el proyecto!
