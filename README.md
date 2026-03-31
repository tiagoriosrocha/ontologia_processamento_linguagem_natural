# 📚 Ontologia de PLN

Ontologia abrangente de Processamento de Linguagem Natural baseada no livro:

Processamento de Linguagem Natural: Conceitos, Técnicas e Aplicações em Português – 3a. Edição / organizadoras:
Helena de Medeiros Caseli e Maria das Graças Volpe Nunes. ── São Carlos : BPLN, 2024. Internet: brasileiraspln.com/livro-pln ISBN: 978-65-01-20581-6

---

## 📁 Arquivos Principais

| Arquivo | Descrição | Tamanho |
|---------|-----------|--------|
| **`onto_pln.owl`** | Ontologia principal em OWL 2.0 com 177 classes e 9 propriedades | 57 KB |
| **`onto_pln_individuals.owl`** | 62 exemplos concretos (instâncias) para as classes | 15 KB |

---

## 🚀 Começar Rapidamente


### 1. Validar com Python
```bash
python3 validar_ontologia.py                # Validar arquitetura
python3 validar_individuals.py              # Validar instâncias
```

### 2. Usar em Código (Python)
```python
from rdflib import Graph

g = Graph()
g.parse("onto_pln.owl", format='xml')

# Consultar classes
print(f"Total de triplas: {len(g)}")

# Buscar específico
for s in g.subjects():
    print(s)
```

---

## 📊 Conteúdo da Ontologia

**177 Classes** organizadas em 7 categorias principais:

- 🔤 **Conceitos Fundamentais** (8): Linguagem, Token, Lexema, Significado, etc.
- 🎯 **Níveis Linguísticos** (7): Fonética, Fonologia, Morfologia, Sintaxe, Semântica, Pragmática, Discurso
- 📋 **Tarefas PLN** (50+): Análise, Geração, Classificação, Recuperação
- 🧠 **Arquiteturas Neurais** (7): DNN, RNN, LSTM, GRU, CNN, Transformer, Seq2Seq
- 🤖 **Modelos Pré-Treinados** (15): Word2Vec, BERT, GPT, ELMo, etc.
- 📚 **Recursos** (40+): Corpus, Datasets, WordNet, DBpedia, FrameNet
- 🎨 **Aplicações** (15): Chatbot, Tradutor, Analisador de Sentimentos, etc.

**9 Object Properties** conectando conceitos:
- `pertenceAoNivel` | `usaModelo` | `usaRecurso` | `requerTarefa` | `usaArquitetura` | `usaTecnica` | `usaParadigma` | `avaliaBorPor` | `temComponente`
