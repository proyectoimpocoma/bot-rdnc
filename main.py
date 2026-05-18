import streamlit as st

from app.bot.handler import BotHandler
from app.core.logging import get_app_logger

logger = get_app_logger("")


def interface():
    st.set_page_config(page_title="Bot RNDC", page_icon="🚛")
    st.title("Consulta de Rutas RNDC 🚛")

    @st.cache_resource
    def get_bot():
        return BotHandler()

    bot = get_bot()

    # 2. Inicializar el historial del chat en la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 3. Dibujar los mensajes anteriores en pantalla
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "dataframe" in msg:
                st.dataframe(msg["dataframe"], use_container_width=True)

    texto_usuario = st.chat_input("Escribe tu ruta (Ej: De Abejorral a Guarne)")
    logger.info(texto_usuario)

    if texto_usuario:
        # A. Mostrar el mensaje del usuario inmediatamente
        st.chat_message("user").markdown(texto_usuario)
        st.session_state.messages.append({"role": "user", "content": texto_usuario})

        # B. Procesar la respuesta del bot
        with (
            st.chat_message("assistant"),
            st.spinner("Consultando base de datos RNDC..."),
        ):
            try:
                # Pasar el texto al handler
                resultado = bot.run(texto_usuario)
                logger.info(resultado)

                # Validar si el dataframe está vacío
                if resultado is not None and not resultado.is_empty():
                    st.markdown("Aqui estan los datos encontrados")

                    # Polars a Pandas para mejor compatibilidad con Streamlit
                    df_mostrar = resultado.to_pandas()
                    st.dataframe(df_mostrar, use_container_width=True)

                    # Guardar en historial
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "Aquí están los datos encontrados:",
                            "dataframe": df_mostrar,
                        }
                    )
                else:
                    msg = "No encontré resultados exactos para esa ruta."
                    st.markdown(msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": msg}
                    )

            except Exception as e:
                logger.error(f"Error procesando la ruta: {e}")
                msg_error = "Hubo un error intentando buscar la ruta. Revisa que las ciudades sean correctas."
                st.error(msg_error)
                st.session_state.messages.append(
                    {"role": "assistant", "content": msg_error}
                )


def main():
    interface()


if __name__ == "__main__":
    main()
