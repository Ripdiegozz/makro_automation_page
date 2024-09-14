import pandas as pd
import os
import datetime

def process_file(uploaded_file, user):
    # Definir las columnas requeridas para el output
    final_columns = [
        'Check Revision', 'CÓD. Código / Unidades Disponibles UND*', 'Departamento',
        'Código', 'Descripcion', 'Tipo Cliente', 'Tipo Cliente Promoción', 
        'No Oferta', 'Descripcion Brief', 'Excepciones / Comentarios', 
        'PVP Regular Sugerido', 'PVP Regular con Descuento', 'Descuento en Porcentaje %', 
        'Escala', 'Unidades Disponibles', 'Q Maxima por Cliente'
    ]

    source_columns = [
        'Pack RMS', 'Sucursal', 'Proveedor', 'Departamento', 'Código', 'Descripcion', 'Tipo Cliente', 'KVI',
        'No Oferta', 'Descripcion Brief', 'Tipo Cliente Promoción', 'Tipo de Oferta', 'Nacional o Regional',
        '1', '2', '3', '4', '5', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
        'Excepciones / Comentarios', 'Ctd Stock', 'Valor Stock', 'Mes N-3', 'Mes N-2', 'Mes N-1', 'Prom Ctd',
        'Promedio Dias MM', 'Unidades a Vender', 'Evacuacion de Inventario (SI/NO)', '% Incremento Venta',
        'PVP Moda', 'PVP Regular Sugerido', 'PVP Regular con Descuento', 'Descuento en Porcentaje %', 'Escala',
        'Precio con Escala', 'PVP Oferta', 'Descuento', 'Ahorro', 'Estimado Venta', 'Unidades Disponibles',
        'Q Maxima por Cliente'
    ]
    
    filter = [
        'Departamento', 'Código', 'Descripcion', 'Tipo Cliente', 'Tipo Cliente Promoción',
        'No Oferta', 'Descripcion Brief', 'Excepciones / Comentarios', 'PVP Regular Sugerido',
        'PVP Regular con Descuento', 'Descuento\nen Porcentaje %', 'Escala', 'Unidades Disponibles',
        'Q Maxima por Cliente'
    ]

    try:
        all_sheets = pd.read_excel(uploaded_file, sheet_name=None, skiprows=6)
        # "./"
        app_dir = os.path.dirname(__file__)
        output_dir = os.path.join(app_dir, 'processed_files')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{user.username}-processed-file.xlsx"
        processed_file_path = os.path.join(output_dir, filename)

        with pd.ExcelWriter(processed_file_path) as writer:
            for sheet_name, sheet_df in all_sheets.items():
                # Verificar tiene columnas
                if len(sheet_df.columns) > 1:
                    # Eliminar la primera columna si siempre está vacía
                    sheet_df = sheet_df.drop(sheet_df.columns[0], axis=1)
                    
                    if len(sheet_df.columns) != len(source_columns):
                        print(f"Error: La hoja {sheet_name} tiene un número inesperado de columnas: {len(sheet_df.columns)}")
                        continue
                    
                    df = sheet_df[filter]

                    # Asegurarse de que el DataFrame tenga las columnas finales
                    df_final = pd.DataFrame(columns=final_columns)
                    
                    # Rellenar el DataFrame final con los datos procesados
                    df_final[filter] = df
                    df_final = df_final[final_columns]

                    # Guardar el DataFrame en una hoja del archivo Excel
                    df_final.to_excel(writer, sheet_name=sheet_name, index=False)

        return processed_file_path

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None
