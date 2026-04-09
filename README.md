# 📁 File Organizer — Organizador Inteligente de Arquivos de Clientes

Ferramenta em Python para organizar automaticamente pastas desorganizadas de clientes, classificando arquivos por tipo, detectando duplicatas e gerando relatório completo.

Desenvolvida para uso em consultoria e gestão de projetos, onde clientes frequentemente enviam documentos, dados e imagens sem estrutura definida.

---

## ⚙️ O que faz

- **Classificação automática** por categoria (Documentos, Dados, Imagens, Código, etc.)
- **Detecção de duplicatas** via hash MD5 — arquivos idênticos vão para pasta `_Duplicatas`
- **Nomes únicos** — nunca sobrescreve arquivos existentes
- **Interface gráfica** — seleção de pastas via janela (sem linha de comando)
- **Relatório completo** `.txt` com distribuição por categoria e estatísticas
- **Popup de conclusão** com resumo do processamento

---

## 📂 Estrutura gerada

```
📁 Destino/
├── 📁 Documentos/
│   ├── 📁 Word/          (.doc, .docx, .odt)
│   ├── 📁 PDF/           (.pdf)
│   └── 📁 Texto/         (.txt, .md, .log)
├── 📁 Dados/
│   ├── 📁 Excel/         (.xls, .xlsx, .xlsm)
│   ├── 📁 CSV_TXT_DAT/   (.csv, .dat, .tsv)
│   └── 📁 LiDAR/         (.laz, .las, .sta)
├── 📁 Apresentacoes/     (.ppt, .pptx)
├── 📁 Imagens/           (.jpg, .png, .tiff...)
├── 📁 Imagens/RAW/       (.nef, .cr2, .arw...)
├── 📁 Videos/            (.mp4, .mov, .avi...)
├── 📁 Audio/             (.mp3, .wav...)
├── 📁 Compactados/       (.zip, .rar, .7z...)
├── 📁 Codigo/            (.py, .r, .sql, .ipynb...)
├── 📁 Nao_Identificados/ (extensões desconhecidas)
├── 📁 _Duplicatas/       (arquivos idênticos detectados)
└── 📄 _relatorio_YYYYMMDD_HHMMSS.txt
```

---

## 🚀 Como usar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute

```bash
python file_organizer.py
```

Duas janelas vão abrir:
1. Selecione a **pasta de origem** (arquivos do cliente)
2. Selecione a **pasta de destino** (onde organizar)

O script processa tudo automaticamente e exibe um relatório ao final.

---

## 📊 Exemplo de relatório gerado

```
============================================================
      RELATÓRIO DE ORGANIZAÇÃO DE ARQUIVOS
============================================================
  Origem         : C:/Clientes/Projeto_XYZ
  Processado em  : 08/04/2026 14:32:10
  Duração        : 12s
  Status         : ✅ CONCLUÍDO
============================================================

── RESUMO GERAL ─────────────────────────────────────────
  Total de arquivos encontrados : 347
  Arquivos organizados          : 331
  Duplicatas detectadas         : 16
  Erros                         : 0

── DISTRIBUIÇÃO POR CATEGORIA ───────────────────────────
  Documentos/PDF          :  142 arquivo(s)  ██████████████████████████
  Dados/Excel             :   87 arquivo(s)  ████████████████
  Imagens                 :   62 arquivo(s)  ███████████
  Documentos/Word         :   28 arquivo(s)  █████
  Dados/CSV_TXT_DAT       :   12 arquivo(s)  ██
```

---

## 🔧 Configuração

No topo do `file_organizer.py`, adicione ou remova categorias conforme sua necessidade:

```python
CATEGORIAS = {
    "Documentos/Word": {".doc", ".docx"},
    "Dados/LiDAR":     {".laz", ".las"},   # específico para energia eólica
    # adicione suas categorias aqui
}
```

---

## 📦 Dependências

```
Pillow
```
> `os`, `shutil`, `hashlib`, `pathlib` e `tkinter` são bibliotecas nativas do Python.

---

## 🌱 Casos de uso

| Contexto | Aplicação |
|---|---|
| Consultoria técnica | Organizar entregas de clientes de projetos |
| Energia renovável | Separar dados de campo, relatórios e imagens |
| Gestão documental | Estruturar arquivos de múltiplos fornecedores |
| Uso pessoal | Organizar downloads, backups e arquivos antigos |

---

## 👤 Autor

**Pedro Paulo Rodrigues Grassel**  
Electrical Engineering Undergraduate | Data Analysis & Automation  
[LinkedIn](https://linkedin.com/in/pedrograssel)
