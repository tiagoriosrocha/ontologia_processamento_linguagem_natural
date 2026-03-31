# 📚 Ontologia de Processamento de Linguagem Natural (PLN)

Ontologia abrangente e formal de **Processamento de Linguagem Natural**, desenvolvida como referência estruturada baseada no livro:

> **Processamento de Linguagem Natural: Conceitos, Técnicas e Aplicações em Português** – 3ª Edição
> 
> Organizadoras: Helena de Medeiros Caseli e Maria das Graças Volpe Nunes  
> Publicação: BPLN, 2024 | ISBN: 978-65-01-20581-6  
> Website: brasileiraspln.com/livro-pln

---

## 🎯 O que é Esta Ontologia?

Esta ontologia PLN é uma **representação formal e estruturada do conhecimento em Processamento de Linguagem Natural**, codificada em **OWL 2.0** (Web Ontology Language). Ela mapeia conceitos, técnicas, modelos e aplicações da área PLN em uma hierarquia semântica que pode ser:

- 📖 **Consultada** por humanos para entender estrutura conceitual
- 🔍 **Processada** por máquinas para reasoning e inferência
- 🔗 **Integrada** em sistemas que precisam de conhecimento PLN estruturado
- 📊 **Estendida** com novos conceitos conforme evolução da área

---

## 📦 Arquivo da Ontologia

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| **`onto_pln.owl`** | OWL 2.0 | Ontologia principal: 315 classes, 9 propriedades, 2.380 linhas |

---

## 🏗️ Estrutura e Organização

### Hierarquia Conceitual

A ontologia está organizada em **11 domínios semânticos principais**:

```
Ontologia PLN (Raiz)
│
├─ 🔤 CONCEITOS FUNDAMENTAIS
│  └─ Linguagem, Token, Palavra, Frase, Sentença, Lexema, Significado
│
├─ 🎚️ NÍVEIS DE ANÁLISE LINGUÍSTICA
│  ├─ Fonologia (sons da linguagem)
│  ├─ Morfologia (estrutura das palavras)
│  ├─ Sintaxe (estrutura das frases)
│  ├─ Semântica (significado)
│  ├─ Pragmática (uso contextual)
│  └─ Discurso (organização textual)
│
├─ 📋 TAREFAS DE PLN (60+ classes)
│  ├─ Tarefas de Análise (Tokenização, POS Tagging, NER, etc.)
│  ├─ Tarefas de Geração (Sumarização, Tradução, etc.)
│  ├─ Tarefas de Classificação (Sentimentos, Spam, etc.)
│  └─ Tarefas de Recuperação (Busca, QA, etc.)
│
├─ 🧠 ARQUITETURAS NEURAIS (15 classes)
│  ├─ Redes Recorrentes (LSTM, GRU, RNN)
│  ├─ Redes Convolucionais (CNN)
│  ├─ Mecanismos de Atenção (Self-attention, Multi-head)
│  ├─ Transformer
│  └─ Componentes (Activation, Loss functions, Gates)
│
├─ 🤖 MODELOS PRÉ-TREINADOS (30+ classes)
│  ├─ Modelos de Linguagem (Word2Vec, GloVe, FastText)
│  ├─ Modelos Neurais (BERT, GPT, ELMo, T5)
│  ├─ Modelos Multimodais
│  └─ Sistemas LLM
│
├─ 📚 RECURSOS E DADOS
│  ├─ Corpora (Linguísticos, Anotados, Paralelos)
│  ├─ Datasets (Benchmarks)
│  └─ Bases de Conhecimento (WordNet, DBpedia, etc.)
│
├─ 🎨 APLICAÇÕES PRÁTICAS
│  ├─ Chatbot e Diálogo
│  ├─ Tradução Automática
│  ├─ Análise de Sentimentos
│  ├─ Sistemas QA
│  └─ Detecção de Plágio
│
├─ 📊 TÉCNICAS E PARADIGMAS
│  ├─ Aprendizado Supervisionado
│  ├─ Aprendizado Não-Supervisionado
│  ├─ Transfer Learning
│  └─ Few-shot/Zero-shot Learning
│
├─ 📈 MÉTRICAS E AVALIAÇÃO (20+ classes)
│  ├─ Métricas de Tradução (BLEU, METEOR, TER, WER)
│  ├─ Métricas de Similaridade (BERTScore, BLEURT)
│  └─ Métricas Gerais (Precision, Recall, F1)
│
├─ 🔧 PRÉ-PROCESSAMENTO E PÓS-PROCESSAMENTO
│  ├─ Normalização Textual
│  ├─ Reparação Gramatical
│  └─ Otimização de Output
│
└─ 🎓 RESPONSABILIDADE E ÉTICA EM IA
   ├─ Viés e Preconceitos
   ├─ Explicabilidade
   ├─ Privacidade
   └─ Transparência
```

### Propriedades Relacionais

As classes são conectadas por **9 propriedades semânticas**:

| Propriedade | Significado | Exemplo |
|-----------|-----------|---------|
| `pertenceAoNivel` | Conceito pertence a nível linguístico | Sintaxe ∈ Níveis |
| `usaModelo` | Tarefa utiliza um modelo pré-treinado | NER usa BERT |
| `usaRecurso` | Tarefa usa recurso (corpus, dataset) | Tradução usa Corpus Paralelo |
| `requerTarefa` | Tarefa pré-requisito para outra | POS-Tagging antes de Parsing |
| `usaArquitetura` | Tarefa implementada com arquitetura | Classificação usa Transformer |
| `usaTecnica` | Tarefa aplica técnica específica | NER usa Sequence Labeling |
| `usaParadigma` | Abordagem usa paradigma de aprendizado | Chatbot usa Deep Learning |
| `avaliaPor` | Métrica usada para avaliar tarefa | Tradução avaliada por BLEU |
| `temComponente` | Sistema contém componente | Chatbot tem NLU + NLG |

---

## 🎯 Para que Serve?

Esta ontologia PLN pode ser utilizada para:

### 1. **Referência e Educação**
- Estrutura formal para ensino de PLN
- Mapa completo do domínio da área
- Hierarquia clara de conceitos

### 2. **Integração em Sistemas**
- Base de conhecimento para sistemas de recomendação
- Markup semântico de documentos sobre PLN
- Raciocínio automatizado sobre conceitos

### 3. **Pesquisa e Documentação**
- Mapeamento de estado da arte
- Rastreabilidade entre conceitos
- Análise de tendências e gaps

### 4. **Desenvolvimento de Aplicações**
- Guia para desenvolvimento de sistemas PLN
- Mapeamento de dependências entre tarefas
- Seleção de arquiteturas apropriadas

### 5. **Interoperabilidade**
- Padrão comum de nomenclatura
- Integração com ontologias externas
- Consultas SPARQL complexas

---

## 📋 Conteúdo Quantitativo

| Elemento | Quantidade |
|----------|-----------|
| **Classes** | 315 |
| **Object Properties** | 9 |
| **Linhas OWL/XML** | 2.380 |
| **Linguagens Suportadas** | Português + Inglês |

---

## 🔍 Como Consultar

### Via Python (RDFLib)
```python
from rdflib import Graph

# Carregar ontologia
g = Graph()
g.parse("onto_pln.owl", format='xml')

# Contar classes
from rdflib.namespace import RDFS, RDF, OWL
classes = list(g.subjects(RDF.type, OWL.Class))
print(f"Total de classes: {len(classes)}")

# Encontrar subclasses de "TarefaPLN"
from rdflib import URIRef
tarefa = URIRef("http://www.ufrgs.br/ontologies/onto_pln.owl#TarefaPLN")
subclasses = list(g.subjects(RDFS.subClassOf, tarefa))
for sc in subclasses:
    print(sc)
```

### Via SPARQL
```sparql
# Todas as tarefas que usam Transformer
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.ufrgs.br/ontologies/onto_pln.owl#>

SELECT ?tarefa WHERE {
  ?tarefa ont:usaArquitetura ont:Transformer .
}
```

---

## 📐 Validação

A ontologia foi validada quanto a:
- ✅ **Bem-formação XML/RDF**: Estrutura válida
- ✅ **Conformidade OWL 2.0**: Sintaxe e semântica corretas
- ✅ **Integridade de Hierarquias**: Subclass relations válidas
- ✅ **Correção Ortográfica**: 315 classes auditadas
- ✅ **Coerência Semântica**: Relações lógicas consistentes

---

## 🔗 Recursos Adicionais

- 📖 Livro-base: https://brasileiraspln.com/livro-pln
- 🌐 Padrão OWL: https://www.w3.org/OWL/
- 🔍 SPARQL: https://www.w3.org/TR/sparql11-query/
- 📚 RDFLib: https://rdflib.readthedocs.io/
