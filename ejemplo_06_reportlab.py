"""Ejemplo 6: librería reportlab para crear PDFs más profesionales."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
from utilidades import titulo, ruta_salida


def pdf_con_canvas():
    """Forma de bajo nivel: dibujar directamente en coordenadas."""
    salida = ruta_salida("reportlab_canvas.pdf")
    c = canvas.Canvas(str(salida), pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 700, "Hola desde ReportLab (canvas)")
    c.setFont("Helvetica", 12)
    c.drawString(100, 670, "Aquí se dibuja usando coordenadas (x, y).")
    c.setStrokeColor(colors.blue)
    c.rect(100, 600, 200, 50)          # rectángulo
    c.circle(400, 625, 25, fill=1)     # círculo
    c.save()
    print("PDF creado:", salida.name)


def pdf_con_platypus():
    """Forma de alto nivel: párrafos, tablas y estilos automáticos."""
    salida = ruta_salida("reportlab_platypus.pdf")
    estilos = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(salida), pagesize=letter)

    contenido = [
        Paragraph("Reporte de ventas", estilos["Title"]),
        Spacer(1, 12),
        Paragraph(
            "Este documento se generó con <b>Platypus</b>, el módulo de "
            "ReportLab que organiza el contenido automáticamente.",
            estilos["Normal"],
        ),
        Spacer(1, 20),
    ]

    datos = [
        ["Mes", "Ventas", "Gastos"],
        ["Enero", "1200", "800"],
        ["Febrero", "1500", "900"],
        ["Marzo", "1800", "1000"],
    ]
    tabla = Table(datos, colWidths=[120, 100, 100])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))
    contenido.append(tabla)

    doc.build(contenido)
    print("PDF creado:", salida.name)


def main():
    titulo("6. REPORTLAB")
    pdf_con_canvas()
    pdf_con_platypus()


if __name__ == "__main__":
    main()
