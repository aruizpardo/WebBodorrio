from datetime import datetime
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO

import mysql.connector
import os
import pandas as pd

app = FastAPI()

# Habilitar CORS para que la web pueda hacer llamadas a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.post("/invitados")
def crear_invitado(
    nome: str = Form(...),
    contacto: str = Form(...),
    asistencia: str = Form(...),
    usuario_bus: str = Form(...),
    neno: str = Form(...),
    vegano: str = Form(...),
    alerxias: str = Form(""),
    intolerancias: str = Form("")
):
    """Crear un nuevo invitado"""
    try:
        db = get_db()
        cursor = db.cursor()

        query = """
            INSERT INTO invitados 
            (nome, contacto, asistencia, usuario_bus, neno, vegano, alerxias, intolerancias)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            nome,
            contacto,
            True if asistencia == 'si' else False,
            True if usuario_bus == 'si' else False,
            True if neno == 'si' else False,
            True if vegano == 'si' else False,
            alerxias,
            intolerancias
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()

        return {"message": "Invitado creado exitosamente", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
def exportar_csv():
    """Exportar invitados a CSV"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT nome, contacto, asistencia, usuario_bus, neno, vegano, alerxias, intolerancias FROM invitados ORDER BY data_rexistro DESC")
        invitados = cursor.fetchall()
        cursor.close()
        db.close()

        if not invitados:
            raise HTTPException(status_code=404, detail="No hay invitados para exportar")
        
        # Crear DataFrame a partir de datos
        df = pd.DataFrame(invitados)

        # Crear resumo
        total_invitados = len(df)
        confirmados = len(df[df['asistencia'] == True])
        usuarios_bus = len(df[df['usuario_bus'] == True])
        ninos = len(df[df['neno'] == True])
        vegans = len(df[df['vegano'] == True])
        alerxias = len(df[df['alerxias'] != ""])
        intolerancias = len(df[df['intolerancias'] != ""])

        # Crear DataFrame de resumo
        df_resumo = pd.DataFrame({
            'Concepto': ['Total invitados', 'Confirmados', 'Usuarios bus', 'Nenos', 'Vegans', 'Alerxias', 'Intolerancias'],
            'Cantidade': [total_invitados, confirmados, usuarios_bus, ninos, vegans, alerxias, intolerancias]
        })

        # Crear DataFrame a partir de datos
        df = pd.DataFrame(invitados)

        # Crear Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Escribir páxina de resumo primeiro
            df_resumo.to_excel(writer, index=False, sheet_name="Resumo")

            # Escribir datos dos invitados
            df.to_excel(writer, index=False, sheet_name="Invitados")

            # Axustar ancho das columnas
            for sheet_name in ["Resumo", "Invitados"]:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    # Engadir un pouco de marxe
                    adjusted_width = min(max_length + 5, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        filename = f"invitados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "API de Boda funcionando"}