"""Interfaz gráfica minimalista en blanco y negro (estilo neo-brutalismo).

Diseño inspirado en estética de alto contraste, bordes sólidos de 2px
y sombras duras rectangulares (black drop shadow).
Solo utiliza tonos blanco y negro (#ffffff y #000000).
"""

import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# Activar alta definición (DPI Awareness) en Windows para nitidez absoluta
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from utilidades import CARPETA_SALIDA

# Categorías
CAT_ESTANDAR = "ESTÁNDAR"
CAT_ARCHIVOS = "ARCHIVOS & PDF"
CAT_DATOS = "DATOS & GRÁFICAS"
CAT_WEB_ML = "WEB & ML"

EJEMPLOS = [
    {
        "id": 1,
        "modulo": "ejemplo_01_math",
        "funcion": "main",
        "numero": "01",
        "nombre": "MATH",
        "categoria": CAT_ESTANDAR,
        "icono": "📐",
        "descripcion": "Constantes pi y e, raíces cuadradas, potencias, logaritmos, trigonometría, factoriales y cálculo de área.",
        "archivos": [],
    },
    {
        "id": 2,
        "modulo": "ejemplo_02_random",
        "funcion": "main",
        "numero": "02",
        "nombre": "RANDOM",
        "categoria": CAT_ESTANDAR,
        "icono": "🎲",
        "descripcion": "Generación de números aleatorios, elecciones de listas, dados y generador de contraseñas.",
        "archivos": [],
    },
    {
        "id": 3,
        "modulo": "ejemplo_03_datetime",
        "funcion": "main",
        "numero": "03",
        "nombre": "DATETIME",
        "categoria": CAT_ESTANDAR,
        "icono": "📅",
        "descripcion": "Fechas y horas actuales, formato strftime, lectura strptime, cálculos con timedelta y diferencia de días.",
        "archivos": [],
    },
    {
        "id": 4,
        "modulo": "ejemplo_04_csv",
        "funcion": "main",
        "numero": "04",
        "nombre": "CSV",
        "categoria": CAT_ARCHIVOS,
        "icono": "📑",
        "descripcion": "Escritura y lectura de archivos CSV tabulares con csv.writer, csv.reader, DictReader y DictWriter.",
        "archivos": ["alumnos.csv", "alumnos_aprobados.csv"],
    },
    {
        "id": 5,
        "modulo": "ejemplo_05_fpdf",
        "funcion": "main",
        "numero": "05",
        "nombre": "FPDF2",
        "categoria": CAT_ARCHIVOS,
        "icono": "📄",
        "descripcion": "Creación de documentos PDF con encabezado, pie de página, texto estructurado y tabla de productos.",
        "archivos": ["reporte_fpdf.pdf"],
    },
    {
        "id": 6,
        "modulo": "ejemplo_06_reportlab",
        "funcion": "main",
        "numero": "06",
        "nombre": "REPORTLAB",
        "categoria": CAT_ARCHIVOS,
        "icono": "📰",
        "descripcion": "Generación avanzada de PDFs vectoriales con Canvas (dibujo en coordenadas) y Platypus (tablas automáticas).",
        "archivos": ["reportlab_canvas.pdf", "reportlab_platypus.pdf"],
    },
    {
        "id": 7,
        "modulo": "ejemplo_07_numpy",
        "funcion": "main",
        "numero": "07",
        "nombre": "NUMPY",
        "categoria": CAT_DATOS,
        "icono": "🔢",
        "descripcion": "Arreglos multidimensionales, operaciones vectorizadas sin bucles, estadísticas, matrices y álgebra lineal.",
        "archivos": [],
    },
    {
        "id": 8,
        "modulo": "ejemplo_08_pandas",
        "funcion": "main",
        "numero": "08",
        "nombre": "PANDAS",
        "categoria": CAT_DATOS,
        "icono": "🐼",
        "descripcion": "DataFrames estructurados, cálculo de sueldos, filtrado condicional, agrupaciones groupby y exportación CSV.",
        "archivos": ["empleados_pandas.csv"],
    },
    {
        "id": 9,
        "modulo": "ejemplo_09_matplotlib",
        "funcion": "main",
        "numero": "09",
        "nombre": "MATPLOTLIB",
        "categoria": CAT_DATOS,
        "icono": "📈",
        "descripcion": "Visualización gráfica: gráficas de líneas, barras de ventas, dispersión, pastel e histograma.",
        "archivos": ["graficas_matplotlib.png", "histograma_matplotlib.png"],
    },
    {
        "id": 10,
        "modulo": "ejemplo_10_requests",
        "funcion": "main",
        "numero": "10",
        "nombre": "REQUESTS",
        "categoria": CAT_WEB_ML,
        "icono": "🌐",
        "descripcion": "Peticiones HTTP GET y POST a una API REST remota, parámetros URL y control seguro de fallos de red.",
        "archivos": [],
    },
    {
        "id": 11,
        "modulo": "ejemplo_11_flask",
        "funcion": "demo_sin_servidor",
        "numero": "11",
        "nombre": "FLASK",
        "categoria": CAT_WEB_ML,
        "icono": "🌶️",
        "descripcion": "Servidor web y endpoints de API probados mediante el cliente de pruebas interno (test_client).",
        "archivos": [],
    },
    {
        "id": 12,
        "modulo": "ejemplo_12_sklearn",
        "funcion": "main",
        "numero": "12",
        "nombre": "SCIKIT-LEARN",
        "categoria": CAT_WEB_ML,
        "icono": "🤖",
        "descripcion": "Modelos de Machine Learning: Regresión lineal, clasificación KNN (dataset Iris) y agrupamiento KMeans.",
        "archivos": [],
    },
]


class TextRedirector:
    """Redirige stdout y stderr a una cola thread-safe para la consola."""

    def __init__(self, cola, tag="stdout"):
        self.cola = cola
        self.tag = tag

    def write(self, texto):
        if texto:
            self.cola.put((texto, self.tag))

    def flush(self):
        pass


class NeoCard(tk.Frame):
    """Contenedor de tarjeta neo-brutalista con sombra negra dura y borde sólido."""

    def __init__(self, parent, shadow_size=4, bg_card="#ffffff", **kwargs):
        super().__init__(parent, bg="#000000", **kwargs)
        self.shadow_size = shadow_size
        self.inner = tk.Frame(
            self,
            bg=bg_card,
            highlightthickness=2,
            highlightbackground="#000000",
            highlightcolor="#000000",
        )
        self.inner.pack(
            fill="both",
            expand=True,
            padx=(0, shadow_size),
            pady=(0, shadow_size),
        )


class NeoButton(tk.Frame):
    """Botón estilo neo-brutalista blanco y negro con sombra dura y animación de pulsado."""

    def __init__(
        self,
        parent,
        text="",
        command=None,
        font=("Segoe UI", 9, "bold"),
        padx=12,
        pady=5,
        shadow_size=3,
        inverted=False,
        cursor="hand2",
        **kwargs
    ):
        super().__init__(parent, bg="#000000", **kwargs)
        self.command = command
        self.shadow_size = shadow_size
        self.inverted = inverted
        self.is_disabled = False

        self.bg_normal = "#000000" if inverted else "#ffffff"
        self.fg_normal = "#ffffff" if inverted else "#000000"
        self.bg_hover = "#222222" if inverted else "#000000"
        self.fg_hover = "#ffffff" if inverted else "#ffffff"

        self.inner = tk.Frame(
            self,
            bg=self.bg_normal,
            highlightthickness=2,
            highlightbackground="#000000",
            highlightcolor="#000000",
            cursor=cursor,
        )
        self.inner.pack(
            fill="both",
            expand=True,
            padx=(0, self.shadow_size),
            pady=(0, self.shadow_size),
        )

        self.label = tk.Label(
            self.inner,
            text=text,
            font=font,
            bg=self.bg_normal,
            fg=self.fg_normal,
            padx=padx,
            pady=pady,
            cursor=cursor,
        )
        self.label.pack(fill="both", expand=True)

        for w in (self.inner, self.label):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._on_press)
            w.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, e=None):
        if self.is_disabled:
            return
        self.inner.configure(bg=self.bg_hover)
        self.label.configure(bg=self.bg_hover, fg=self.fg_hover)

    def _on_leave(self, e=None):
        if self.is_disabled:
            return
        self.inner.pack_configure(
            padx=(0, self.shadow_size), pady=(0, self.shadow_size)
        )
        self.inner.configure(bg=self.bg_normal)
        self.label.configure(bg=self.bg_normal, fg=self.fg_normal)

    def _on_press(self, e=None):
        if self.is_disabled:
            return
        offset = max(1, self.shadow_size - 1)
        self.inner.pack_configure(
            padx=(offset, max(0, self.shadow_size - offset)),
            pady=(offset, max(0, self.shadow_size - offset)),
        )

    def _on_release(self, e=None):
        if self.is_disabled:
            return
        self.inner.pack_configure(
            padx=(0, self.shadow_size), pady=(0, self.shadow_size)
        )
        if self.command:
            self.command()

    def set_text(self, text):
        self.label.configure(text=text)

    def set_state(self, state):
        self.is_disabled = state == "disabled"
        if self.is_disabled:
            self.inner.configure(bg="#e5e5e5")
            self.label.configure(bg="#e5e5e5", fg="#888888", cursor="arrow")
            self.inner.configure(cursor="arrow")
        else:
            self.inner.configure(bg=self.bg_normal)
            self.label.configure(bg=self.bg_normal, fg=self.fg_normal, cursor="hand2")
            self.inner.configure(cursor="hand2")

    def set_inverted(self, inverted):
        self.inverted = inverted
        self.bg_normal = "#000000" if inverted else "#ffffff"
        self.fg_normal = "#ffffff" if inverted else "#000000"
        self.bg_hover = "#222222" if inverted else "#000000"
        self.fg_hover = "#ffffff" if inverted else "#ffffff"
        self.inner.configure(bg=self.bg_normal)
        self.label.configure(bg=self.bg_normal, fg=self.fg_normal)


class AppVentana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EJEMPLOS DE LIBRERÍAS PYTHON")
        self.geometry("1180x760")
        self.minsize(980, 620)
        self.configure(bg="#ffffff")

        # Variables de estado
        self.cola_salida = queue.Queue()
        self.ejecutando = False
        self.filtro_categoria = "TODOS"
        self.filtro_texto = tk.StringVar()
        self.filtro_texto.trace_add("write", lambda *args: self.actualizar_lista_ejemplos())
        self.cards_buttons = []

        # Redirigir stdout y stderr
        self.stdout_orig = sys.stdout
        self.stderr_orig = sys.stderr
        sys.stdout = TextRedirector(self.cola_salida, "stdout")
        sys.stderr = TextRedirector(self.cola_salida, "stderr")

        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self._crear_interfaz()
        self._iniciar_escucha_cola()
        self.log_bienvenida()

    def al_cerrar(self):
        sys.stdout = self.stdout_orig
        sys.stderr = self.stderr_orig
        self.destroy()

    def _crear_interfaz(self):
        # 1. ENCABEZADO MINIMALISTA (Blanco, texto negro, borde inferior de 2px)
        header = tk.Frame(self, bg="#ffffff", padx=24, pady=16)
        header.pack(fill="x", side="top")

        header_content = tk.Frame(header, bg="#ffffff")
        header_content.pack(fill="x")

        # Título y subtítulo
        title_box = tk.Frame(header_content, bg="#ffffff")
        title_box.pack(side="left")

        lbl_titulo = tk.Label(
            title_box,
            text="EJEMPLOS DE LIBRERÍAS",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#000000",
        )
        lbl_titulo.pack(anchor="w")

        lbl_subtitulo = tk.Label(
            title_box,
            text="12 MÓDULOS INTERACTIVOS • PYTHON • ESTILO MINIMALISTA B&W",
            font=("Segoe UI", 8, "bold"),
            bg="#ffffff",
            fg="#666666",
        )
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))

        # Botones de acción del encabezado (con sombra dura neo-brutalista)
        actions_box = tk.Frame(header_content, bg="#ffffff")
        actions_box.pack(side="right")

        self.btn_ejecutar_todo = NeoButton(
            actions_box,
            text="▶ EJECUTAR TODO",
            font=("Segoe UI", 9, "bold"),
            shadow_size=4,
            inverted=True,  # Fondo negro con letras blancas para destacar
            padx=14,
            pady=7,
            command=self.ejecutar_todos,
        )
        self.btn_ejecutar_todo.pack(side="left", padx=6)

        self.btn_abrir_salida = NeoButton(
            actions_box,
            text="📂 CARPETA 'SALIDA'",
            font=("Segoe UI", 9, "bold"),
            shadow_size=4,
            inverted=False,
            padx=14,
            pady=7,
            command=self.abrir_carpeta_salida,
        )
        self.btn_abrir_salida.pack(side="left", padx=6)

        # Línea divisoria negra inferior del encabezado
        linea_divisoria = tk.Frame(self, bg="#000000", height=2)
        linea_divisoria.pack(fill="x", side="top")

        # 2. CUERPO PRINCIPAL (2 columnas)
        cuerpo = tk.Frame(self, bg="#ffffff", padx=20, pady=16)
        cuerpo.pack(fill="both", expand=True)

        # PANEL IZQUIERDO: Tarjetas de opciones
        panel_izq = tk.Frame(cuerpo, bg="#ffffff", width=540)
        panel_izq.pack(side="left", fill="both", expand=False, padx=(0, 14))
        panel_izq.pack_propagate(False)

        # Barra de búsqueda
        bar_filtro = tk.Frame(panel_izq, bg="#ffffff")
        bar_filtro.pack(fill="x", pady=(0, 10))

        # Contenedor con sombra para la búsqueda
        search_card = NeoCard(bar_filtro, shadow_size=3, bg_card="#ffffff")
        search_card.pack(fill="x")

        search_inner = tk.Frame(search_card.inner, bg="#ffffff", padx=8, pady=4)
        search_inner.pack(fill="x")

        lbl_lupa = tk.Label(
            search_inner,
            text="🔍",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#000000",
        )
        lbl_lupa.pack(side="left", padx=(0, 6))

        ent_buscar = tk.Entry(
            search_inner,
            textvariable=self.filtro_texto,
            font=("Segoe UI", 10),
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        ent_buscar.pack(side="left", fill="x", expand=True)

        # Chips de categorías (Botones minimalistas B&W)
        chips_frame = tk.Frame(panel_izq, bg="#ffffff")
        chips_frame.pack(fill="x", pady=(0, 12))

        self.categorias = ["TODOS", CAT_ESTANDAR, CAT_ARCHIVOS, CAT_DATOS, CAT_WEB_ML]
        self.botones_categoria = {}
        for cat in self.categorias:
            btn_cat = NeoButton(
                chips_frame,
                text=cat,
                font=("Segoe UI", 7, "bold"),
                shadow_size=2,
                inverted=(cat == self.filtro_categoria),
                padx=8,
                pady=3,
                command=lambda c=cat: self.cambiar_categoria(c),
            )
            btn_cat.pack(side="left", padx=(0, 6), pady=2)
            self.botones_categoria[cat] = btn_cat

        # Canvas con scrollbar para la lista de tarjetas
        canvas_container = tk.Frame(panel_izq, bg="#ffffff")
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_container,
            bg="#ffffff",
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = ttk.Scrollbar(
            canvas_container, orient="vertical", command=self.canvas.yview
        )
        self.scroll_content = tk.Frame(self.canvas, bg="#ffffff")

        self.scroll_content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scroll_content, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        self.actualizar_lista_ejemplos()

        # PANEL DERECHO: Consola y Archivos generados
        panel_der = tk.Frame(cuerpo, bg="#ffffff")
        panel_der.pack(side="right", fill="both", expand=True)

        # Consola contenida en un NeoCard con sombra dura de 4px
        console_card = NeoCard(panel_der, shadow_size=4, bg_card="#000000")
        console_card.pack(fill="both", expand=True)

        # Barra superior de la consola
        cons_top = tk.Frame(console_card.inner, bg="#000000", padx=12, pady=8)
        cons_top.pack(fill="x")

        # Indicador de estado minimalista
        self.lbl_status_led = tk.Label(
            cons_top,
            text="●",
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg="#000000",
        )
        self.lbl_status_led.pack(side="left", padx=(0, 6))

        self.lbl_status_text = tk.Label(
            cons_top,
            text="LISTO PARA EJECUTAR",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#000000",
        )
        self.lbl_status_text.pack(side="left")

        # Botones de consola: Limpiar y Copiar (estilo B&W)
        btn_copiar = NeoButton(
            cons_top,
            text="📋 COPIAR",
            font=("Segoe UI", 7, "bold"),
            shadow_size=2,
            inverted=False,
            padx=8,
            pady=2,
            command=self.copiar_consola,
        )
        btn_copiar.pack(side="right", padx=(4, 0))

        btn_limpiar = NeoButton(
            cons_top,
            text="🧹 LIMPIAR",
            font=("Segoe UI", 7, "bold"),
            shadow_size=2,
            inverted=False,
            padx=8,
            pady=2,
            command=self.limpiar_consola,
        )
        btn_limpiar.pack(side="right", padx=(4, 0))

        # Línea divisoria en la consola
        tk.Frame(console_card.inner, bg="#333333", height=1).pack(fill="x")

        # Área de texto de la consola
        text_frame = tk.Frame(console_card.inner, bg="#000000")
        text_frame.pack(fill="both", expand=True)

        self.txt_consola = tk.Text(
            text_frame,
            bg="#000000",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Consolas", 10),
            wrap="word",
            relief="flat",
            padx=12,
            pady=10,
            bd=0,
        )
        scroll_consola = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.txt_consola.yview
        )
        self.txt_consola.configure(yscrollcommand=scroll_consola.set)

        self.txt_consola.pack(side="left", fill="both", expand=True)
        scroll_consola.pack(side="right", fill="y")

        # Configuración de tags de texto en consola (estricto B&W)
        self.txt_consola.tag_config("titulo", foreground="#ffffff", font=("Consolas", 10, "bold"))
        self.txt_consola.tag_config("destacado", foreground="#ffffff", font=("Consolas", 10, "bold"))
        self.txt_consola.tag_config("dim", foreground="#aaaaaa")
        self.txt_consola.tag_config("sep", foreground="#555555")
        self.txt_consola.tag_config("error", foreground="#ffffff", background="#333333", font=("Consolas", 10, "bold"))

        # Barra inferior: Acceso rápido a archivos generados
        self.frame_archivos_card = NeoCard(panel_der, shadow_size=3, bg_card="#ffffff")
        self.frame_archivos_card.pack(fill="x", pady=(12, 0))

        bar_archivos = tk.Frame(self.frame_archivos_card.inner, bg="#ffffff", padx=10, pady=8)
        bar_archivos.pack(fill="x")

        lbl_archivos_titulo = tk.Label(
            bar_archivos,
            text="📁 ARCHIVOS:",
            font=("Segoe UI", 8, "bold"),
            bg="#ffffff",
            fg="#000000",
        )
        lbl_archivos_titulo.pack(side="left", padx=(0, 8))

        self.chips_archivos_frame = tk.Frame(bar_archivos, bg="#ffffff")
        self.chips_archivos_frame.pack(side="left", fill="x", expand=True)

        self.actualizar_chips_archivos()

    def cambiar_categoria(self, cat):
        self.filtro_categoria = cat
        for c, btn in self.botones_categoria.items():
            btn.set_inverted(c == self.filtro_categoria)
        self.actualizar_lista_ejemplos()

    def actualizar_lista_ejemplos(self):
        for w in self.scroll_content.winfo_children():
            w.destroy()
        self.cards_buttons.clear()

        query = self.filtro_texto.get().strip().lower()

        visibles = []
        for ej in EJEMPLOS:
            if self.filtro_categoria != "TODOS" and ej["categoria"] != self.filtro_categoria:
                continue
            if query:
                match = (
                    query in ej["nombre"].lower()
                    or query in ej["descripcion"].lower()
                    or query in ej["categoria"].lower()
                    or query in ej["numero"].lower()
                    or any(query in arc.lower() for arc in ej["archivos"])
                )
                if not match:
                    continue
            visibles.append(ej)

        if not visibles:
            lbl_vacio = tk.Label(
                self.scroll_content,
                text="No hay ejemplos que coincidan con la búsqueda.",
                font=("Segoe UI", 9, "italic"),
                bg="#ffffff",
                fg="#666666",
                pady=30,
            )
            lbl_vacio.pack(fill="x")
            return

        for ej in visibles:
            # Tarjeta con borde sólido de 2px y sombra negra dura de 3px
            card = NeoCard(self.scroll_content, shadow_size=3, bg_card="#ffffff")
            card.pack(fill="x", pady=5, padx=2)

            inner_box = tk.Frame(card.inner, bg="#ffffff", padx=12, pady=10)
            inner_box.pack(fill="x")

            # Fila superior: Número, Icono, Nombre, Badge de categoría y Botón Ejecutar
            top_row = tk.Frame(inner_box, bg="#ffffff")
            top_row.pack(fill="x")

            # Badge con número
            lbl_num = tk.Label(
                top_row,
                text=f"[{ej['numero']}]",
                font=("Segoe UI", 9, "bold"),
                bg="#ffffff",
                fg="#000000",
            )
            lbl_num.pack(side="left", padx=(0, 6))

            lbl_ico = tk.Label(
                top_row,
                text=ej["icono"],
                font=("Segoe UI", 11),
                bg="#ffffff",
            )
            lbl_ico.pack(side="left", padx=(0, 6))

            lbl_nom = tk.Label(
                top_row,
                text=ej["nombre"],
                font=("Segoe UI", 10, "bold"),
                bg="#ffffff",
                fg="#000000",
            )
            lbl_nom.pack(side="left")

            # Badge categoría en contorno negro
            cat_badge_frame = tk.Frame(top_row, bg="#000000")
            cat_badge_frame.pack(side="left", padx=8)
            cat_badge_inner = tk.Frame(
                cat_badge_frame,
                bg="#ffffff",
                highlightthickness=1,
                highlightbackground="#000000",
                padx=5,
                pady=1,
            )
            cat_badge_inner.pack()
            lbl_cat = tk.Label(
                cat_badge_inner,
                text=ej["categoria"],
                font=("Segoe UI", 7, "bold"),
                bg="#ffffff",
                fg="#000000",
            )
            lbl_cat.pack()

            # Botón neo-brutalista idéntico a la imagen de referencia del usuario
            btn_run = NeoButton(
                top_row,
                text="▶ EJECUTAR",
                font=("Segoe UI", 8, "bold"),
                shadow_size=3,
                inverted=False,
                padx=10,
                pady=3,
                command=lambda e=ej: self.ejecutar_un_ejemplo(e),
            )
            btn_run.pack(side="right")
            self.cards_buttons.append(btn_run)

            # Descripción en negro
            lbl_desc = tk.Label(
                inner_box,
                text=ej["descripcion"],
                font=("Segoe UI", 8),
                bg="#ffffff",
                fg="#333333",
                justify="left",
                wraplength=490,
            )
            lbl_desc.pack(anchor="w", pady=(6, 0))

            # Si genera archivos, mostrar chip
            if ej["archivos"]:
                files_row = tk.Frame(inner_box, bg="#ffffff")
                files_row.pack(anchor="w", pady=(4, 0))
                lbl_tag_arc = tk.Label(
                    files_row,
                    text="Archivo generado: " + ", ".join(ej["archivos"]),
                    font=("Segoe UI", 7, "bold"),
                    bg="#ffffff",
                    fg="#000000",
                )
                lbl_tag_arc.pack(side="left")

    def actualizar_chips_archivos(self):
        for w in self.chips_archivos_frame.winfo_children():
            w.destroy()

        if not CARPETA_SALIDA.exists():
            lbl = tk.Label(
                self.chips_archivos_frame,
                text="Sin archivos generados aún.",
                font=("Segoe UI", 8, "italic"),
                bg="#ffffff",
                fg="#666666",
            )
            lbl.pack(side="left")
            return

        archivos = [f for f in CARPETA_SALIDA.iterdir() if f.is_file()]
        if not archivos:
            lbl = tk.Label(
                self.chips_archivos_frame,
                text="Carpeta vacía. Ejecuta los ejemplos para generarlos.",
                font=("Segoe UI", 8, "italic"),
                bg="#ffffff",
                fg="#666666",
            )
            lbl.pack(side="left")
            return

        for arc in sorted(archivos, key=lambda f: f.stat().st_mtime, reverse=True)[:5]:
            ext = arc.suffix.lower()
            icono = "📄"
            if ext == ".pdf":
                icono = "📕"
            elif ext == ".png":
                icono = "🖼️"
            elif ext == ".csv":
                icono = "📊"

            btn_arc = NeoButton(
                self.chips_archivos_frame,
                text=f"{icono} {arc.name}",
                font=("Segoe UI", 7, "bold"),
                shadow_size=2,
                inverted=False,
                padx=6,
                pady=1,
                command=lambda p=arc: self.abrir_archivo(p),
            )
            btn_arc.pack(side="left", padx=3)

    def log_bienvenida(self):
        self.escribir_consola("============================================================\n", "sep")
        self.escribir_consola("⚡ PANEL DE CONTROL - EJEMPLOS DE LIBRERÍAS PYTHON\n", "titulo")
        self.escribir_consola("============================================================\n", "sep")
        self.escribir_consola("• Pulsa '▶ EJECUTAR' en cualquier tarjeta para probar esa librería.\n", "dim")
        self.escribir_consola("• O pulsa '▶ EJECUTAR TODO' arriba para ejecutar las 12 demostraciones.\n", "dim")
        self.escribir_consola("• La salida se mostrará aquí en tiempo real.\n", "dim")
        self.escribir_consola("• Los archivos generados se guardan en la carpeta 'salida'.\n\n", "dim")

    def _iniciar_escucha_cola(self):
        try:
            while True:
                texto, tag = self.cola_salida.get_nowait()
                self._procesar_linea_consola(texto, tag)
        except queue.Empty:
            pass
        self.after(50, self._iniciar_escucha_cola)

    def _procesar_linea_consola(self, texto, tag_origen):
        tag_final = tag_origen
        if "====" in texto:
            tag_final = "sep"
        elif any(f"{i}. " in texto for i in range(1, 13)) and ("=" not in texto):
            tag_final = "titulo"
        elif "PDF creado:" in texto or "Imagen guardada:" in texto or "Archivo creado:" in texto or "[OK]" in texto:
            tag_final = "destacado"
        elif "Error" in texto or "Traceback" in texto or "Exception" in texto:
            tag_final = "error"

        self.txt_consola.insert(tk.END, texto, tag_final)
        self.txt_consola.see(tk.END)

    def escribir_consola(self, texto, tag="stdout"):
        self.txt_consola.insert(tk.END, texto, tag)
        self.txt_consola.see(tk.END)

    def limpiar_consola(self):
        self.txt_consola.delete("1.0", tk.END)

    def copiar_consola(self):
        texto = self.txt_consola.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Salida de consola copiada al portapapeles.")

    def abrir_carpeta_salida(self):
        CARPETA_SALIDA.mkdir(exist_ok=True)
        try:
            if sys.platform == "win32":
                os.startfile(str(CARPETA_SALIDA))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(CARPETA_SALIDA)])
            else:
                subprocess.Popen(["xdg-open", str(CARPETA_SALIDA)])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{e}")

    def abrir_archivo(self, ruta: Path):
        try:
            if not ruta.exists():
                messagebox.showwarning("No encontrado", f"El archivo '{ruta.name}' no existe.")
                return
            if sys.platform == "win32":
                os.startfile(str(ruta))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(ruta)])
            else:
                subprocess.Popen(["xdg-open", str(ruta)])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def set_estado(self, ejecutando: bool, mensaje: str = ""):
        self.ejecutando = ejecutando
        if ejecutando:
            self.lbl_status_led.configure(text="⏳")
            self.lbl_status_text.configure(text=mensaje or "EJECUTANDO...")
            self.btn_ejecutar_todo.set_state("disabled")
            for btn in self.cards_buttons:
                try:
                    btn.set_state("disabled")
                except Exception:
                    pass
        else:
            self.lbl_status_led.configure(text="●")
            self.lbl_status_text.configure(text=mensaje or "LISTO")
            self.btn_ejecutar_todo.set_state("normal")
            for btn in self.cards_buttons:
                try:
                    btn.set_state("normal")
                except Exception:
                    pass
            self.actualizar_chips_archivos()

    def ejecutar_un_ejemplo(self, ej):
        if self.ejecutando:
            return

        def tarea():
            nombre = ej["nombre"]
            self.set_estado(True, f"EJECUTANDO {nombre}...")
            t0 = time.time()
            try:
                mod = __import__(ej["modulo"])
                fn = getattr(mod, ej["funcion"])
                fn()
                duracion = time.time() - t0
                print(f"\n[OK] {nombre} finalizado con éxito en {duracion:.2f}s.\n")
                self.set_estado(False, f"COMPLETADO: {nombre} ({duracion:.2f}s)")
            except Exception as e:
                import traceback
                print(f"\n[ERROR] Falló en {nombre}: {e}\n")
                traceback.print_exc()
                self.set_estado(False, f"ERROR EN {nombre}")

        threading.Thread(target=tarea, daemon=True).start()

    def ejecutar_todos(self):
        if self.ejecutando:
            return

        def tarea():
            self.set_estado(True, "EJECUTANDO TODOS LOS EJEMPLOS...")
            t_inicio_total = time.time()

            for i, ej in enumerate(EJEMPLOS, 1):
                nombre = ej["nombre"]
                self.set_estado(True, f"EJECUTANDO ({i}/12): {nombre}...")
                try:
                    mod = __import__(ej["modulo"])
                    fn = getattr(mod, ej["funcion"])
                    fn()
                except Exception as e:
                    import traceback
                    print(f"\n[ERROR] Falló en {nombre}: {e}\n")
                    traceback.print_exc()

            t_total = time.time() - t_inicio_total
            print("\n" + "=" * 60)
            print(f" Listo. Todos los ejemplos terminaron en {t_total:.2f}s.")
            print(f" Revisa la carpeta '{CARPETA_SALIDA.name}' para ver los archivos generados.")
            print("=" * 60 + "\n")
            self.set_estado(False, f"TODOS LOS EJEMPLOS COMPLETADOS ({t_total:.2f}s)")

        threading.Thread(target=tarea, daemon=True).start()


def iniciar_interfaz():
    app = AppVentana()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()
