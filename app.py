import streamlit as st
import json
import random
import os

# Archivo donde se guardarán las palabras
DATA_FILE = "words.json"

# Cargar palabras desde el archivo JSON
def load_words():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar palabras en el archivo JSON
def save_words(words):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=4, ensure_ascii=False)

# Agregar una nueva palabra
def add_word(english, spanish):
    words = load_words()
    words.append({"english": english, "spanish": spanish, "learned": False})
    save_words(words)

# Marcar palabra como aprendida
def mark_learned(index):
    words = load_words()
    words[index]["learned"] = True
    save_words(words)

# Obtener palabras para repasar (nuevas y aprendidas)
def get_words_for_review():
    words = load_words()
    new_words = [w for w in words if not w["learned"]]
    learned_words = [w for w in words if w["learned"]]
    return new_words + learned_words

# Función para buscar palabras específicas
def search_words(query):
    words = load_words()
    return [word for word in words if query.lower() in word['english'].lower()]

# ----------------- INTERFAZ STREAMLIT -----------------
st.title("📚 My English Trainer 📝")

# Modo: Agregar palabra
st.sidebar.header("➕ Agregar Nueva Palabra")
new_english = st.sidebar.text_input("Palabra en inglés:")
new_spanish = st.sidebar.text_input("Traducción en español:")
if st.sidebar.button("Agregar"):
    if new_english and new_spanish:
        if any(word['english'].lower() == new_english.lower() for word in load_words()):
            st.sidebar.warning("⚠️ La palabra ya existe en la lista.")
        else:
            add_word(new_english, new_spanish)
            st.sidebar.success("✅ Palabra agregada!")
    else:
        st.sidebar.warning("⚠️ Completa ambos campos.")

# 📌 Modo: Repaso de palabras
st.header("🧠 Modo Repaso")

# Controlar la palabra actual en sesión
if 'current_word' not in st.session_state:
    words_for_review = get_words_for_review()
    if words_for_review:
        st.session_state.current_word = random.choice(words_for_review)
    else:
        st.session_state.current_word = None

word = st.session_state.current_word

if word:
    # Mostrar palabra en inglés más grande
    st.markdown(f"🔹 <h1 style='font-size: 40px; text-align:center;'>{word['english']}</h1>", unsafe_allow_html=True)

    # Alternar traducción
    if 'show_translation_state' not in st.session_state:
        st.session_state.show_translation_state = False

    show_translation_button = st.button("Mostrar/Ocultar Traducción")
    if show_translation_button:
        st.session_state.show_translation_state = not st.session_state.show_translation_state

    if st.session_state.show_translation_state:
        st.write(f"📖 Traducción: **{word['spanish']}**")
    
    # Botón para marcar como aprendida
    if st.button("✔️ Marcar como aprendida"):
        words = load_words()
        index = words.index(word)
        mark_learned(index)
        words_for_review = get_words_for_review()
        st.session_state.current_word = random.choice(words_for_review) if words_for_review else None
        st.success("¡Bien hecho! 🎉")
        st.rerun()  # Recargar la página para mostrar una nueva palabra

else:
    st.info("🏆 ¡Has aprendido todas las palabras!")

# 📌 Panel de palabras con scroll vertical y soporte para tema oscuro
st.header("📖 Lista de Palabras")

with st.expander("📜 Ver todas las palabras (clic para expandir)"):
    search_query = st.text_input("🔍 Buscar palabra en inglés")

    # Filtrar palabras según búsqueda
    filtered_words = search_words(search_query) if search_query else load_words()

    # Estilos para el contenedor de scroll con tema oscuro
    st.markdown(
        """
        <style>
        .scroll-container {
            height: 300px; /* Altura máxima del panel */
            overflow-y: auto; /* Habilitar scroll vertical */
            border: 1px solid #444;
            padding: 10px;
            background-color: #222; /* Fondo oscuro */
            border-radius: 5px;
            color: #ddd; /* Texto claro para contrastar */
        }
        .scroll-container p {
            color: #fff; /* Color blanco para texto */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenedor con scroll y palabras dentro
    palabras_html = "<div class='scroll-container'>"
    for word in filtered_words:
        palabras_html += f"<p>🔹 <b>{word['english']}</b> - {word['spanish']} {'✅' if word['learned'] else '❌'}</p>"
    palabras_html += "</div>"

    st.markdown(palabras_html, unsafe_allow_html=True)
