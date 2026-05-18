import streamlit as st


def render_chat_history(messages: list):
    """Dibuja todos los mensajes anteriores en pantalla."""
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "dataframe" in msg:
                render_result(msg["dataframe"])


def render_result(resultado):
    """Renderiza el dataframe de resultados del bot."""
    if resultado is None or resultado.is_empty():
        msg = "No encontre resultados exactos para esa ruta."
        st.markdown(msg)
        return None, msg

    # Agrupar por tipo de vehiculo por polars
    grupos = resultado.partition_by("CONFIG_VEHICULO", as_dict=True)

    lineas = ["### 🚛 Resultados por tipo de vehículo\n"]

    for tipo_vehiculo, df_group in grupos.items():
        # Calcular metricas
        total_viajes = df_group["VIAJESTOTALES"].sum()
        costo_promedio_unitario = df_group["VALOR_PROMEDIO_UNITARIO"].mean()

        # Mostrar en 3 columnas con números formateados

        lineas.append(
            f"**🚚 {tipo_vehiculo}**  \n"
            f"- 📦 Viajes totales: `{total_viajes:,.0f}`  \n"
            f"- 💰 Flete promedio: `${costo_promedio_unitario:,.0f}`  \n"
        )
    texto = st.markdown("\n".join(lineas))
    return resultado.to_pandas(), texto
