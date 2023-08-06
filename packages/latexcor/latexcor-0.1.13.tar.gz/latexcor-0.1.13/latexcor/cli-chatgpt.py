import os
import chardet
import argparse


def clean_aux(paths: list) -> None:
    """nettoie les fichiers auxiliaires produits par le compilateur LaTeX.

    Args:
        paths (list): _description_
    """
    """
    Cette fonction se charge de nettoyer tous les fichiers auxiliaires qui se trouvent dans le dossier spécifié.

    :param paths: Liste des chemins des dossiers à nettoyer
    :type paths: list
    :return: None
    """
    for path in paths:
        try:
            for file in os.listdir(path):
                ext = os.path.splitext((file))[1]
                if ext in clean_up:
                    try:
                        os.remove(os.path.join(path, file))
                        print(f"{file} a été supprimé avec succès")
                    except OSError:
                        print(f"Erreur lors de la suppression de {file}")
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")


def predict_encoding(file_path: str, n_lines: int = 20) -> str:
    """Predict a file's encoding using chardet

    Args:
        file_path (str): Path to the file to be analyzed
        n_lines (int, optional): Number of lines to analyze. Defaults to 20.

    Returns:
        str: The detected encoding
    """

    # Open the file as binary data
    with open(file_path, "rb") as f:
        # Join binary lines for specified number of lines
        rawdata = b"".join([f.readline() for _ in range(n_lines)])

    # Check if the encoding is detected and return the result
    encoding = chardet.detect(rawdata)["encoding"]
    if encoding is not None:
        return encoding
    else:
        raise ValueError("Unable to detect encoding")


# Ajout de la possibilité de spécifier un dossier source différent à surveiller et à compiler
parser.add_argument("--src_dir", help="Specify source directory for latexcompiler")


def recompile_all(path: str, latex_engine: str) -> None:
    for file_name in os.listdir(path):
        if file_name.endswith(".tex"):
            os.system(f"{latex_engine} {file_name}")


def define_latex_engine(args: argparse.Namespace) -> str:
    if args.xelatex:
        return "xelatex"
    elif args.lualatex:
        return "lualatex"
    else:
        return "pdflatex"
