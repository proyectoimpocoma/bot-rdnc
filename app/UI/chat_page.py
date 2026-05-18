import streamlit as st

from app.bot.handler import BotHandler
from app.core import get_app_logger
from app.UI import components, state

logger = get_app_logger("chat_page")


@st.cache_resource
def get_bot() -> BotHandler:
    return BotHandler()


def render():
    st.set_page_config(page_title="Bot RNDC", page_icon="🚛")
    st.title("Cotizacion de Rutas RNDC")

    bot = get_bot()
    state.init_state()
    components.render_chat_history(st.session_state.message)

    text_usuario = st.chat_input("Escribe tu ruta (Ej: De Abejorral a Guarne)")

    if text_usuario:
        st.chat_message("user").markdown(text_usuario)
        state.add_message("user", text_usuario)

        with st.chat_message("assistant"), st.spinner("Consultando RNDC.."):
            try:
                resultado = bot.run(text_usuario)
                df_mostrar, texto_respuesta = components.render_result(resultado)
                state.add_message("assistant", texto_respuesta, df_mostrar)
            except Exception as e:
                logger.error(f"Error procesando la ruta: {e}")
                st.error("Hubo un error. Revisa que las ciudades sean correctas.")
