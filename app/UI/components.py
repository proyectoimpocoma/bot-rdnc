import streamlit as st


def render_chat_history(messages: list):
    """Dibuja todos los mensajes anteriores en pantalla."""
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "dataframe" in msg:
                st.dataframe(msg["dataframe"], use_container_width=True)


def render_result(resultado):
    """Renderiza el dataframe de resultados del bot."""
    if resultado is not None and not resultado.is_empty():
        st.markdown("Aquí están los datos encontrados:")
        df_mostrar = resultado.to_pandas()
        st.dataframe(df_mostrar, use_container_width=True)
        return df_mostrar, "Aquí están los datos encontrados:"
    else:
        msg = "No encontré resultados exactos para esa ruta."
        st.markdown(msg)
        return None, msg
