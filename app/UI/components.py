import streamlit as st


def render_chat_history(messages: list):
    """Dibuja todos los mensajes anteriores en pantalla."""
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def render_result(resultado: dict | None):
    """Renderiza el dataframe de resultados del bot."""
    if (
        resultado["ruta_db"] is None
        or resultado["ruta_db"].is_empty()
        or resultado["costo_sicetac"] is None
    ):
        msg = "No encontre resultados exactos para esa ruta."
        st.markdown(msg)
        return None, msg

    # Agrupar por tipo de vehiculo por polars
    # grupos = resultado.partition_by("COD_CONFIG_VEHICULO", as_dict=True)

    sicetac = resultado["costo_sicetac"]
    lineas = [
        f"### 🚛 Resultados para {resultado['origen']} - {resultado['destino']}\n"
    ]

    df_group = resultado["ruta_db"]

    tipo_vehiculo = df_group["COD_CONFIG_VEHICULO"][0]
    # Calcular metricas
    total_viajes = df_group["VIAJESTOTALES"].sum()
    costo_promedio_unitario = df_group["VALOR_PROMEDIO_UNITARIO"].mean()

    # Mostrar en 3 columnas con números formateados

    lineas.append(
        f"**🚚 {tipo_vehiculo}**  \n"
        f"- 📦 Viajes totales: `{total_viajes:,.0f}`  \n"
        f"- 💰 Flete promedio: `${costo_promedio_unitario:,.0f}`  \n"
        f"- 🧾 Costo SICETAC: `{sicetac}`"
    )
    texto = "\n".join(lineas)
    st.markdown(texto)
    return texto
