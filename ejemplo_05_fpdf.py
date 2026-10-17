"""Ejemplo 5: librería fpdf (paquete fpdf2) para crear PDFs sencillos."""
from fpdf import FPDF
from utilidades import titulo, ruta_salida


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Reporte generado con FPDF", align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def main():
    titulo("5. FPDF")

    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Ejemplo con fpdf2", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(
        0, 8,
        "Este PDF fue creado con Python. FPDF permite escribir texto, "
        "dibujar líneas y crear tablas de forma muy sencilla.",
    )
    pdf.ln(5)

    # Tabla simple
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 10, "Producto", border=1)
    pdf.cell(40, 10, "Cantidad", border=1)
    pdf.cell(40, 10, "Precio", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=12)
    productos = [("Teclado", 5, 350.00), ("Mouse", 10, 150.50), ("Monitor", 2, 2800.00)]
    for nombre, cantidad, precio in productos:
        pdf.cell(60, 10, nombre, border=1)
        pdf.cell(40, 10, str(cantidad), border=1)
        pdf.cell(40, 10, f"${precio:,.2f}", border=1, new_x="LMARGIN", new_y="NEXT")

    # Una línea decorativa
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    salida = ruta_salida("reporte_fpdf.pdf")
    pdf.output(str(salida))
    print("PDF creado:", salida.name)


if __name__ == "__main__":
    main()
