import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

try:
    _icon = Image.open('logo_mr.png')
except Exception:
    _icon = "🔤"
st.set_page_config(page_title="OCR · Miguel Ruiz", page_icon=_icon, layout="centered")

# ---- Estilo personalizado: paleta azul petróleo + terracota (Miguel Ruiz) ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Inter:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(135deg, #1b3a4b 0%, #14303d 100%);
        color: #e8eef0;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { right: 1rem; }
    .stApp, .stApp p, .stApp li, .stApp span, .stApp label,
    .stMarkdown, [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {
        color: #e8eef0 !important;
    }
    h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif !important; color: #e07a5f !important; }
    section[data-testid="stSidebar"] { background: #12272f; }
    section[data-testid="stSidebar"] * { color: #e8eef0 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #e07a5f !important; }
    /* Caja donde aparece el texto reconocido */
    [data-testid="stText"], .stText {
        background: #1d3f4e; color: #e8eef0 !important;
        border: 1px solid rgba(242,204,143,0.15);
        border-radius: 10px; padding: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 style=\"font-family:'Montserrat', sans-serif; font-weight:700; color:#f2cc8f; margin-bottom:0;\">Miguel Ruiz</h2>", unsafe_allow_html=True)
st.title("Reconocimiento Óptico de Caracteres 🔤")
st.caption("Toma una foto y extrae el texto que contiene. Desarrollado por Miguel Ruiz.")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    st.subheader("Opciones")
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

if img_file_buffer is not None:
    # Leer la imagen de la cámara con OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.subheader("Texto reconocido:")
    if text.strip():
        st.write(text)
    else:
        st.info("No se detectó texto en la imagen. Intenta con mejor iluminación o enfoque.")
