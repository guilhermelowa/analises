import glob
import json
import os
import re


def read_files():
    current_dir = os.getcwd()
    notebooks = glob.glob(f"{current_dir}/analysis/*.ipynb")
    scripts = glob.glob(f"{current_dir}/analysis/*.py")
    htmls = glob.glob(f"{current_dir}/docs/*.html")
    return notebooks, scripts, htmls


def check(notebooks, scripts, htmls):
    missing_py_files = len(notebooks) != len(scripts)
    missing_htmls = len(notebooks) != len(htmls)
    has_clean_outputs = True
    naming = []

    for notebook in notebooks:
        # checa padrão de nomes
        naming.extend(
            [True if re.search(r"\d{4}-\d{2}-\d{2}-\S+\.ipynb", notebook) else False]
        )

        # checa se os outputs estão limpos
        notebook = json.load(open(notebook))
        for cell in notebook["cells"]:
            if cell.get("outputs", None):
                has_clean_outputs = False

    has_proper_naming = all(naming)
    return missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs


def build_message(
    missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs
):
    missing_py_files = " " if missing_py_files else "x"
    missing_htmls = " " if missing_htmls else "x"
    proper_naming = "x" if has_proper_naming else " "
    clean_outputs = "x" if has_clean_outputs else " "

    return (
        "Esse checklist vai te ajudar a saber quando o seu notebook está pronto:\n"
        "\n"
        f"- [{clean_outputs}] Os _outputs_ dos _notebooks_ estão limpos\n"
        f"- [{missing_py_files}] Os arquivos `.py` foram gerados na pasta `analysis`\n"
        f"- [{missing_htmls}] Os `.html` foram gerados na pasta `docs/`\n"
        f"- [{proper_naming}] Os nomes dos _notebooks_ estão de acordo com o padrão\n"
        "\n"
        "Se tiver dúvidas, veja o nosso [guia de contribuição](https://github.com/DadosAbertosDeFeira/analises/blob/main/CONTRIBUTING.md).\n"  # noqa
        "Certifique-se que os testes estão passando e que o seu código "
        "está de acordo com as regras de qualidade."
    )


if __name__ == "__main__":
    notebooks, scripts, htmls = read_files()
    missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs = check(
        notebooks, scripts, htmls
    )
    print(
        build_message(
            missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs
        )
    )
