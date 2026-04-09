"""
file_organizer.py
-----------------
Organizador inteligente de arquivos de clientes.
Classifica por tipo, gera relatório e detecta duplicatas.

Autor: Pedro Paulo Rodrigues Grassel
"""

import os
import shutil
import hashlib
import re
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


# ─────────────────────────────────────────────
# CATEGORIAS E EXTENSÕES
# ─────────────────────────────────────────────

CATEGORIAS = {
    "Documentos/Word": {
        ".doc", ".docx", ".odt", ".rtf"
    },
    "Documentos/PDF": {
        ".pdf"
    },
    "Documentos/Texto": {
        ".txt", ".md", ".log"
    },
    "Dados/Excel": {
        ".xls", ".xlsx", ".xlsm", ".ods"
    },
    "Dados/CSV_TXT_DAT": {
        ".csv", ".dat", ".tsv"
    },
    "Dados/LiDAR": {
        ".laz", ".las", ".z+f", ".sta"
    },
    "Apresentacoes": {
        ".ppt", ".pptx", ".odp"
    },
    "Imagens": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".heic", ".tiff", ".tif", ".svg"
    },
    "Imagens/RAW": {
        ".nef", ".cr2", ".arw", ".dng", ".orf", ".rw2"
    },
    "Videos": {
        ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".3gp"
    },
    "Audio": {
        ".mp3", ".wav", ".opus", ".m4a", ".flac", ".aac"
    },
    "Compactados": {
        ".zip", ".rar", ".7z", ".tar", ".gz"
    },
    "Codigo": {
        ".py", ".r", ".R", ".js", ".html", ".css",
        ".sql", ".ipynb", ".sh", ".bat"
    },
}


# ─────────────────────────────────────────────
# INTERFACE GRÁFICA
# ─────────────────────────────────────────────

def selecionar_pasta(titulo: str) -> str:
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title=titulo)
    root.destroy()
    return pasta


def mostrar_conclusao(msg: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Organização Concluída!", msg)
    root.destroy()


# ─────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────

def get_categoria(extensao: str) -> str:
    """Retorna a categoria do arquivo pela extensão."""
    ext = extensao.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if ext in extensoes:
            return categoria
    return "Nao_Identificados"


def hash_arquivo(caminho: Path, chunk_size: int = 8192) -> str:
    """Calcula MD5 do arquivo para detecção de duplicatas exatas."""
    h = hashlib.md5()
    try:
        with open(caminho, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
    except Exception:
        return ""
    return h.hexdigest()


def nome_unico(pasta: Path, nome: str) -> Path:
    """Evita sobrescrever arquivos: gera nome_1, nome_2, etc."""
    destino = pasta / nome
    stem = Path(nome).stem
    suffix = Path(nome).suffix
    contador = 1
    while destino.exists():
        destino = pasta / f"{stem}_{contador}{suffix}"
        contador += 1
    return destino


# ─────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────

def organizar(dir_origem: str, dir_destino: str) -> None:
    path_origem = Path(dir_origem).resolve()
    path_destino = Path(dir_destino).resolve()

    print(f"\n{'='*60}")
    print(f"  ORGANIZADOR DE ARQUIVOS DE CLIENTES")
    print(f"{'='*60}")
    print(f"  Origem  : {path_origem}")
    print(f"  Destino : {path_destino}")
    print(f"{'='*60}\n")

    # Contadores para relatório
    contagem = {}           # {categoria: count}
    duplicatas = 0
    erros = 0
    total = 0
    hashes_vistos = {}      # {hash: caminho_destino}

    inicio = datetime.now()

    for root, dirs, files in os.walk(path_origem):
        path_root = Path(root).resolve()

        # Segurança: não processar a própria pasta de destino
        if path_destino == path_root or path_destino in path_root.parents:
            continue

        for arquivo in files:
            caminho = path_root / arquivo
            extensao = caminho.suffix
            categoria = get_categoria(extensao)
            total += 1

            # Pasta de destino
            pasta_destino = path_destino / categoria
            pasta_destino.mkdir(parents=True, exist_ok=True)

            # Verifica duplicata por hash
            h = hash_arquivo(caminho)
            if h and h in hashes_vistos:
                pasta_dup = path_destino / "_Duplicatas"
                pasta_dup.mkdir(parents=True, exist_ok=True)
                destino_final = nome_unico(pasta_dup, arquivo)
                print(f"  [DUPLICATA] {arquivo}")
                duplicatas += 1
            else:
                destino_final = nome_unico(pasta_destino, arquivo)
                if h:
                    hashes_vistos[h] = destino_final
                print(f"  [OK] {arquivo:45s} → {categoria}")

            try:
                shutil.copy2(str(caminho), str(destino_final))
                contagem[categoria] = contagem.get(categoria, 0) + 1
            except Exception as e:
                print(f"  [ERRO] {arquivo}: {e}")
                erros += 1

    fim = datetime.now()
    duracao = (fim - inicio).seconds

    gerar_relatorio(
        path_destino, path_origem, contagem,
        total, duplicatas, erros, duracao
    )


# ─────────────────────────────────────────────
# RELATÓRIO
# ─────────────────────────────────────────────

def gerar_relatorio(
    path_destino: Path,
    path_origem: Path,
    contagem: dict,
    total: int,
    duplicatas: int,
    erros: int,
    duracao: int
) -> None:

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    organizados = sum(contagem.values())

    linhas = [
        "=" * 60,
        "      RELATÓRIO DE ORGANIZAÇÃO DE ARQUIVOS",
        "=" * 60,
        f"  Origem         : {path_origem}",
        f"  Processado em  : {agora}",
        f"  Duração        : {duracao}s",
        f"  Status         : {'✅ CONCLUÍDO' if erros == 0 else '⚠️  CONCLUÍDO COM ERROS'}",
        "=" * 60,
        "",
        "── RESUMO GERAL ─────────────────────────────────────────",
        f"  Total de arquivos encontrados : {total}",
        f"  Arquivos organizados          : {organizados}",
        f"  Duplicatas detectadas         : {duplicatas}",
        f"  Erros                         : {erros}",
        "",
        "── DISTRIBUIÇÃO POR CATEGORIA ───────────────────────────",
    ]

    for categoria, qtd in sorted(contagem.items(), key=lambda x: -x[1]):
        barra = "█" * min(qtd, 40)
        linhas.append(f"  {categoria:<30s}: {qtd:>4} arquivo(s)  {barra}")

    linhas += [
        "",
        "── ESTRUTURA GERADA ─────────────────────────────────────",
        f"  {path_destino}",
        "",
        "=" * 60,
    ]

    # Salva relatório
    relatorio_path = path_destino / f"_relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print("\n" + "\n".join(linhas))
    print(f"\n  Relatório salvo em: {relatorio_path}")

    # Popup de conclusão
    msg = (
        f"Organização concluída!\n\n"
        f"Total de arquivos : {total}\n"
        f"Organizados       : {organizados}\n"
        f"Duplicatas        : {duplicatas}\n"
        f"Erros             : {erros}\n\n"
        f"Relatório salvo em:\n{relatorio_path}"
    )
    mostrar_conclusao(msg)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("\n  ORGANIZADOR DE ARQUIVOS DE CLIENTES")
    print("  Selecione as pastas nas janelas que vão abrir...\n")

    dir_origem = selecionar_pasta("ORIGEM — Pasta com arquivos do cliente")
    if not dir_origem:
        print("Operação cancelada.")
        return

    dir_destino = selecionar_pasta("DESTINO — Onde salvar os arquivos organizados")
    if not dir_destino:
        print("Operação cancelada.")
        return

    organizar(dir_origem, dir_destino)


if __name__ == "__main__":
    main()
