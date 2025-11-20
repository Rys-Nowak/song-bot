import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from examples import examples

TITLE = "blues_o_czwartej"

INPUT_FILE = "input/input.txt"
OUTPUT_DIR = "output"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        input_text = f.read()

    load_dotenv()
    api_key = "AIzaSyBUCYStWGdnjv1c3Mob5h8ayUSX_UN2280"
    if not api_key:
        print("No GOOGLE_API_KEY found in environment.")
        exit(1)

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.1,
            google_api_key=api_key
        )

        messages = [
            ("system", "Jesteś asystentem, który pomaga w tworzeniu śpiewnika w LaTeX na podstawie podanych tekstów piosenek.\n"
                       "Teksty są kopiowane z różnych źródeł i mogą być w różnym formacie. "
                       "Wyodrębnij autora i tytuł piosenki oraz podane chwyty gitarowe. "
                       "Chwyty gitarowe mogą być podane na końcu każdego wersu lub w tekście. "
                       "Refren powininen być za każdym razem wypisany w całości. "
                       "Zachowaj chwyty gitarowe w tych samych miejscach co w tekście wejściowym, jeśli są one podane w środku linii tekstu piosenki. "
                       "Jeśli są podane nad liniami tekstu lub obok nich -- wypisz je obok tekstu. "
                       "Zadbaj o to, żeby chwyty były podane w każdej linii tekstu, nawet jeśli w tekście wejściowym podane są tylko na początku. "
                       "Staraj się odróżnić zwrotki od refrenów.\n"
                       "Twoim zadaniem jest zwrócenie sformatowanego tekstu piosenki w LaTeX z użyciem pakietu 'songs'. "
                       "Wersy powyżej 32 znaków należy podzielić w dogodnym miejscu na 2 części za pomocą polecenia \\brk. "
                       "Zachowaj dodatkowe informacje takie jak Intro, Solo, Kapodaster itp. i umieść w tekście za pomocą \\musicnote. "
                       "Używaj komend z pakietu songs takich jak \\rep kiedy to potrzebne. "
                       "Do oznaczenia chwytów obok tekstu używaj dodatkowej komendy \\lchords (np. \\lchords{a e G}). "
                       "Do oznaczenie chwytów w intro lub solo/przygrywce zawsze używaj komendy \\nolyrics i składni \[<chwyt>].\n"
                       "Linie mają zaczynać się z dużych liter. "
                    #    "Sprawdź czy w wyjściowym tekście występują wyarażenia ' eginverse', ' eginsong' lub ' eginchorus', jeśli tak, to podmień je na odpowiednio na \\beginverse, \\beginsong i \\beginchorus. "
                       "Na koniec upewnij czy wszystkie chwyty są przepisane poprawnie i czy nie ma różnic w tekście. Popraw wszystkie błędy.\n"
                       "Odpowiadasz wyłącznie w formacie LaTeX bez dodatkowych wyjaśnień ani użycia markdown."),
            *examples,
            ("human", input_text)
        ]

        print("--- Pełna lista wiadomości wysyłana do modelu ---")
        for role, content in messages:
            print(f"{role.upper()}: {content}")
        print("-----------------------------------------------------------------------")

        response = llm.invoke(messages)
        print("\nOdpowiedź LLM:\n", response.content)
        with open(os.path.join(OUTPUT_DIR, f"{TITLE}.tex"), "w", encoding="utf-8") as f:
            f.write(response.content.
                    replace(" egin", "\\begin").
                    replace(" rk ", "\\brk ").
                    replace("	extnote", "\\textnote").
                    replace("\nolyrics", "\n\\nolyrics")
                    )

    except Exception as e:
        print("Błąd komunikacji z Gemini API:", e)

if __name__ == "__main__":
    main()