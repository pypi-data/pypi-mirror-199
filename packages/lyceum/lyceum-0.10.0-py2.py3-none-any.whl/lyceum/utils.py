"""Module d'utilitaires

Pas sûr de la garder"""

import os
from pathlib import Path
from functools import partial

PRINT_NORMAL = print


def make_print_compact():
    return partial(PRINT_NORMAL, end="|")


def make_print_normal():
    return partial(PRINT_NORMAL)


def rep2dot(racine, only_dirs=False, include_files_patterns=[]) -> str:
    """Renvoie un fichier dot d'une structure d'une hiérarchie de répértoire"""
    # numérote les noeuds n0 n1...
    # en stockant le nom du noeud dans un
    racine = Path(racine)
    i = 0
    nodes = {racine.as_posix(): f"n{i}"}
    dot = "digraph tree {\n"
    dot += f'n{i} [shape="folder", label="{racine.name}"];\n'
    for root, dirs, files in os.walk(racine):
        # dossiers
        for dir in dirs:
            dir = Path(f"{root}/{dir}")
            i += 1
            posix = dir.as_posix()
            nodes[posix] = f"n{i}"
            dot += f'{nodes[posix]} [shape="folder", label="{dir.name}"];\n'
            dot += f'{nodes[root]}-> {nodes[posix]};\n'
        # fichiers
        if not only_dirs:
            for file in files:
                file = Path(f"{root}/{file}")
                if sum([file.match(pattern) for pattern in include_files_patterns]) == 0:
                    continue
                i += 1
                posix = file.as_posix()
                nodes[posix] = f"n{i}"
                dot += f'{nodes[posix]} [shape="note", label="{file.name}"];\n'
                dot += f'{nodes[root]}-> {nodes[posix]};\n'

    dot += "}"
        
    print(dot)

    return dot
