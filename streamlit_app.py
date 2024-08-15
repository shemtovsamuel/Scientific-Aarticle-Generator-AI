import os
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
PASSWORD = st.secrets["PASSWORD"]

title_default = "Analyse technique de la déflectométrie en réflexion pour l'évaluation de la qualité des lentilles intraoculaires courbées"
data_default = """L’objectif de ce projet de recherche est d’étudier une solution concernant l’analyse de lentilles intraoculaires partiellement courbées directement après un processus d’usinage et de développer un dispositif de contrôle de la qualité utilisant la technologie PMD. En outre, nous sommes contraints pas le procédé de fabrication des lentilles, lesquelles disposent d’un support de fabrication dont nous ne pouvons pas la séparer pour l’opération de contrôle. Ceci implique que la lentille IOL doit rester fixée sur le porte-pièce, à son support de fabrication. L'inspection doit être effectuée sans contact physique avec la pièce, à sec, sans contact avec de l'eau, de la vapeur ou d'autres liquides et la mesure non destructive. Le contrôle doit également :
•	Avoir une résolution d’image attendue de 5 µm ;
•	Avoir un champ de vision max (FoV ) de l’ordre de 15 mm ;
•	Avoir un temps d’inspection et de traitement inférieur à 2 minutes.

L’élément à inspecter est fabriqué en acrylique hydrophile, acrylique hydrophobe, silicone ou PMMA, donc transparent mais opaque en face d’usinage. Il est important de respecter la géométrie de la lentille IOL, beaucoup moins réfléchissante qu’une lentille standard :
•	Sur sa face arrière, la surface est concave avec des rayons de courbure compris entre 5 et 8 mm ;
•	Sur sa face avant, la surface est convexe avec des rayons de courbure compris entre 0 et 11 mm ;
•	A l’extérieur de la zone optique se trouve une zone de voute inclinée à 27 degrés avec un diamètre à 8 mm ;
•	A l’extérieur de la zone voutée, se trouve la zone haptique d’un diamètre égal à 11,3 mm ;
•	La zone optique d’intérêt mesure environ 5 mm de diamètre.

La difficulté émanant de cet objet, visible sur la figure 2, provient de sa géométrie complexe et est directement corrélée à sa non spécularité induisant des phénomènes potentiels de double réflexion qui devront être considérés du point de vue des chemins optiques lors des mesures.
"""

def read_article(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter the password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter the password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    else:
        return True

if check_password():
    bibliography = read_article("bibliography.txt")

    model = ChatAnthropic(
        temperature=0,
        api_key=ANTHROPIC_API_KEY,
        model_name="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        streaming=True
    )

    prompt = ChatPromptTemplate.from_template("""
Tu es un expert en rédaction d'articles techniques. Ta tâche est de générer un article scientifique sur le sujet donné, en utilisant les données fournies et en vous inspirant de la bibliographie fournie. Voici les directives à suivre :

1. Titre de l'article : {title}

2. Données pertinentes à utiliser :
{data}

3. Bibliographie pour référence :
{bibliography}

Instructions spécifiques :
- Rédige un article scientifique, structuré sur le sujet donné.
- Utilise les données fournies pour étayer ton argumentation et tes explications.
- Inspire-toi des concepts et idées mentionnés dans la bibliographie, mais ne copie pas directement le contenu.
- Cite les sources appropriées de la bibliographie lorsque tu fais référence à des idées spécifiques.
- Assure-toi que l'article soit cohérent, bien organisé et adapté à un public technique.
- Utilise un style d'écriture clair et professionnel.
- L'article doit comporter une introduction, un développement avec plusieurs sous-parties, et une conclusion.
- Longueur approximative : 800-1000 mots.

Génère maintenant l'article en respectant ces directives, en commencant directemement par l'introduction.
""")

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    st.title("Générateur d'Article Technique")

    use_test_values = st.checkbox("Utiliser les valeurs de test")

    if use_test_values:
        title = st.text_input("Entrez le titre de l'article:", value=title_default)
        data = st.text_area("Entrez les données pertinentes:", value=data_default, height=200)
    else:
        title = st.text_input("Entrez le titre de l'article:")
        data = st.text_area("Entrez les données pertinentes:", height=200)

    if st.button("Générer l'Article"):
        if title and data:
            st.subheader("Article Généré:")
            output_container = st.empty()
            full_response = ""

            with st.spinner("Génération de l'article en cours..."):
                for chunk in chain.stream({"title": title, "data": data, "bibliography": bibliography}):
                    full_response += chunk
                    output_container.markdown(full_response)

            st.success("Génération de l'article terminée!")
        else:
            st.error("Veuillez remplir tous les champs avant de générer l'article.")