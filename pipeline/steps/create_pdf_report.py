from pipeline.steps.setp import BaseStep
from config.config import BETS_PDF_PATH
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from datetime import datetime

class CreatePDFReport(BaseStep):

    def _clasificar_riesgo(self, apuesta):

        apuesta = apuesta["bet_data"]
        sigma = apuesta.get("Sigma", 0) or 0
        cv = apuesta.get("CV", 0) or 0
        p_real = apuesta.get("p_real", 0) or 0  # valor entre 0 y 1

        prob_pct = p_real * 100

        """ if sigma < 1.0 and cv < 10 and prob_pct >= 80:
            return "A"  # Muy estable y buena probabilidad
        elif sigma < 1.5 and cv < 20 and prob_pct >= 65:
            return "B"  # Moderado riesgo o probabilidad media
        else:
            return "C"  # Alta variabilidad o baja probabilidad """
        prob_pct = p_real * 100 if p_real <= 1 else p_real

        if prob_pct > 84 and sigma < 0.7 and cv <= 15:
            return "A"
        elif prob_pct >= 70 and sigma <= 1.5 and cv <= 25:
            return "B"
        else:
            return "C"

    def _generar_pdf_apuestas(self, apuestas, filename="apuestas.pdf"):

        def safe_text(value):
            return str(value) if value is not None else ""

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        y = height - 3 * cm  # margen superior

        for apuesta in apuestas:
            try:
                # --- Dimensiones del recuadro 
                card_height = 6 * cm
                card_width = width - 4 * cm
                x = 2 * cm
                y_card_bottom = y - card_height

                # --- Si no hay espacio, nueva página 
                if y_card_bottom < 2.5 * cm:
                    c.showPage()
                    y = height - 3 * cm
                    y_card_bottom = y - card_height

                # --- Fondo de la tarjeta 
                c.setFillColor(HexColor("#f9f9fb"))
                c.setStrokeColor(HexColor("#cccccc"))
                c.roundRect(x, y_card_bottom, card_width, card_height, 10, fill=True, stroke=True)

                # --- Título del evento 
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(black)
                c.drawString(x + 1 * cm, y - 1 * cm, safe_text(apuesta.get('event')))
                

                 # --- Fecha y hora del evento 
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(HexColor("#333A42"))
                fecha = apuesta["start_time"]
                if fecha:
                    dt = datetime.fromisoformat(fecha)
                    fecha_formateada = dt.strftime("%Y-%m-%d | %H:%M")
                    c.drawString(x + 12 * cm, y - 1 * cm, safe_text(fecha_formateada))

                # --- Riesgo del evento 
                riesgo = self._clasificar_riesgo(apuesta)
                c.setFont("Helvetica-Bold", 12)
                if riesgo == "A":
                    c.setFillColor(HexColor("#1C6B39"))
                elif riesgo == "B":
                    c.setFillColor(HexColor("#C8BD3F"))
                else:
                    c.setFillColor(HexColor("#A62929"))
                c.drawString(x + 13.5 * cm, y - 5 * cm, f"Riesgo: {safe_text(riesgo) if hasattr(self, '_clasificar_riesgo') else ''}")

                # --- Info general ---
                c.setFont("Helvetica", 10)
                c.setFillColor(black)

                # Crear las líneas con datos seguros
                info_lines = [
                    "",
                    f"Liga: {safe_text(apuesta['league'])}",
                    f"Mercado: {safe_text(apuesta['bet_data']['mercado'])}",
                    (
                        f"Equipo: {safe_text(apuesta['bet_data']['equipo'])}"
                        if apuesta['bet_data']['equipo'] is not None
                        else "Equipo: "
                    ),
                    f"Promedio de goles: {safe_text(apuesta['predictions']['avg_goals'])}",
                    f"Cuota: {safe_text(apuesta['bet_data']['odd'])}",
                    (
                        f"Probabilidad: {(apuesta['bet_data']['p_real'] * 100):.1f}%"
                        if apuesta['bet_data']['p_real'] is not None
                        else "Probabilidad: "
                    ),
                    f"EV%: {safe_text(apuesta['bet_data']['EV%'])} | Edge%: {safe_text(apuesta['bet_data']['Edge%'])} | Kelly%: {safe_text(apuesta['bet_data']['Kelly%'])}",
                ]

                # Escribir el texto dentro del recuadro
                y_text = y - 1.5 * cm
                for line in info_lines:
                    c.drawString(x + 1 * cm, y_text, safe_text(line))
                    y_text -= 0.45 * cm

                # --- Botón de enlace ---
                btn_w, btn_h = 4.5 * cm, 0.8 * cm
                btn_x, btn_y = x + card_width - btn_w - 1 * cm, y_card_bottom + 0.8 * cm

                url = apuesta.get("fixture_path")
                if url:
                    c.setFillColor(HexColor("#2878CF"))
                    c.roundRect(btn_x, btn_y, btn_w, btn_h, 4, fill=True, stroke=False)

                    c.setFillColor(white)
                    c.setFont("Helvetica-Bold", 10)
                    c.drawCentredString(btn_x + btn_w / 2, btn_y + 0.25 * cm, "Abrir en Stake")

                    # Enlace clicable
                    try:
                        c.linkURL(str(url), (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), relative=0)
                    except Exception as e:
                        self.log.error(f"Error creando enlace para {url}: {e}")

                # Espaciado entre tarjetas
                y = y_card_bottom - 1.5 * cm

            except Exception as e:
                self.log.error(f"Ocurrió un error en una tarjeta: {e}")

        # --- Sección interpretativa al final del PDF ---
        c.showPage()

        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#1F4E79"))
        c.drawString(2 * cm, height - 3 * cm, "Interpretación de los Datos")

        c.setFont("Helvetica", 10)
        c.setFillColor(black)

        texto_interpretacion = [
            "• Liga, Fecha y Mercado: información general del evento deportivo.",
            "• Promedio de goles: valor esperado de anotaciones totales basado en estadísticas.",
            "• Cuota: multiplicador de la apuesta ofrecido por la casa.",
            "• Probabilidad: estimación porcentual de ocurrencia según el modelo.",
            "• EV% (Valor Esperado): si es positivo, la apuesta tiene valor estadístico.",
            "• Edge%: ventaja estimada respecto a la cuota del mercado.",
            "• Kelly%: fracción sugerida del bankroll a invertir.",
            "",
            "Clasificación de riesgo:",
            "  - A: Bajo riesgo → alta probabilidad y baja volatilidad (apuestas más seguras).",
            "  - B: Riesgo medio → equilibrio entre valor y estabilidad.",
            "  - C: Alto riesgo → probabilidad baja o alta variación, mayor incertidumbre."
        ]

        y_text = height - 4 * cm
        for linea in texto_interpretacion:
            c.drawString(2 * cm, y_text, linea)
            y_text -= 0.5 * cm

        # --- Guardar PDF ---
        try:
            c.save()
            self.log.success(f"PDF generado: {filename}")
        except Exception as e:
            self.log.error(f"Ocurrió un error al guardar el PDF: {e}")


    def run(self, context):
        fixture_list = context["good_bets"]

        if len(fixture_list) > 1:
            try:
                filename = f"apuestas_{datetime.now().strftime('%Y-%m-%d')}.pdf"
                self._generar_pdf_apuestas(fixture_list, f"{BETS_PDF_PATH}{filename}")
            except Exception as e:
                self.log.error(f"Ocurrio un error al generar pdf : {e}")
        else:
            self.log.info("No hay ninguna apuesta valiosa")