#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar o match entre termos extraídos do dataset e a ontologia PLN

Uso:
    python3 verificar_match_termos.py
    
Descrição:
    - Lê termos do arquivo entidades_nomeadas_extraidas_dataset.txt
    - Normaliza os termos (remove camelCase, espaços, underscores)
    - Verifica match com labels e altLabels da ontologia
    - Gera relatório detalhado de matches (exatos e parciais)
    - Exporta resultados em JSON
"""

import re
import json
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple
from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.namespace import SKOS, OWL

# Configurações
ONTOLOGIA_PATH = "onto_pln.owl"
ENTRADA_TERMOS_PATH = "entidades_nomeadas_extraidas_dataset.txt"
SAIDA_MATCHES_PATH = "matches_ontologia.json"
SAIDA_RELATORIO_PATH = "relatorio_matches.txt"


def normalizar_termo(termo: str) -> str:
    """
    Normaliza um termo para facilitar comparação
    
    Operações:
    1. Remove acentos
    2. Converte para minúsculas
    3. Remove underscores e hífens
    4. Remove espaços extras
    5. Remove pontuação
    6. Separa camelCase
    
    Args:
        termo: Termo a normalizar
        
    Returns:
        Termo normalizado
    """
    # Remover acentos (decomposição NFD + remoção de diacríticos)
    termo = unicodedata.normalize('NFD', termo)
    termo = ''.join(char for char in termo if unicodedata.category(char) != 'Mn')
    
    # Converter para minúsculas
    termo = termo.lower()
    
    # Separar camelCase (inserir espaço antes de maiúsculas)
    termo = re.sub(r'([a-z])([A-Z])', r'\1 \2', termo)
    termo = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', termo)
    
    # Substituir underscores e hífens por espaços
    termo = termo.replace('_', ' ').replace('-', ' ')
    
    # Remover pontuação (exceto espaços)
    termo = re.sub(r'[^\w\s]', '', termo)
    
    # Normalizar espaços (múltiplos espaços para um)
    termo = re.sub(r'\s+', ' ', termo).strip()
    
    return termo


def carregar_ontologia(caminho: str) -> Graph:
    """
    Carrega a ontologia RDF
    
    Args:
        caminho: Caminho para o arquivo OWL
        
    Returns:
        Graph RDFLib com a ontologia carregada
    """
    print(f"📚 Carregando ontologia de: {caminho}")
    g = Graph()
    g.parse(caminho, format="xml")
    print(f"✓ Ontologia carregada com sucesso ({len(g)} triplas)")
    return g


def extrair_termos_ontologia(g: Graph) -> Dict[str, Dict]:
    """
    Extrai todos os termos (labels e altLabels) da ontologia
    
    Args:
        g: Graph RDFLib
        
    Returns:
        Dict com estrutura:
        {
            'termo_normalizado': {
                'labels': [lista de labels originais],
                'altlabels': [lista de altlabels originais],
                'classes': [lista de URIs das classes],
                'tipo_match': ['label' | 'altlabel' | 'ambos']
            }
        }
    """
    termos_ontologia = defaultdict(lambda: {
        'labels': [],
        'altlabels': [],
        'classes': [],
        'tipo_match': set()
    })
    
    print("\n🔍 Extraindo termos da ontologia...")
    
    # Iterar sobre todas as classes
    for classe in g.subjects(RDF.type, OWL.Class):
        # Extrair labels (RDFS)
        for label in g.objects(classe, RDFS.label):
            label_text = str(label)
            label_norm = normalizar_termo(label_text)
            
            if label_norm:
                termos_ontologia[label_norm]['labels'].append(label_text)
                termos_ontologia[label_norm]['classes'].append(str(classe))
                termos_ontologia[label_norm]['tipo_match'].add('label')
        
        # Extrair altLabels (SKOS)
        for altlabel in g.objects(classe, SKOS.altLabel):
            altlabel_text = str(altlabel)
            altlabel_norm = normalizar_termo(altlabel_text)
            
            if altlabel_norm:
                termos_ontologia[altlabel_norm]['altlabels'].append(altlabel_text)
                termos_ontologia[altlabel_norm]['classes'].append(str(classe))
                termos_ontologia[altlabel_norm]['tipo_match'].add('altlabel')
    
    # Converter sets em listas para serialização JSON
    for termo_norm in termos_ontologia:
        termos_ontologia[termo_norm]['tipo_match'] = list(
            termos_ontologia[termo_norm]['tipo_match']
        )
        # Remover duplicatas mantendo ordem
        termos_ontologia[termo_norm]['classes'] = list(
            dict.fromkeys(termos_ontologia[termo_norm]['classes'])
        )
    
    print(f"✓ {len(termos_ontologia)} termos únicos extraídos da ontologia")
    return dict(termos_ontologia)


def carregar_termos_dataset(caminho: str) -> List[str]:
    """
    Carrega os termos do arquivo de input
    
    Args:
        caminho: Caminho para o arquivo com termos
        
    Returns:
        Lista de termos únicos
    """
    print(f"\n📄 Carregando termos do dataset: {caminho}")
    
    termos = set()
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            termo = linha.strip()
            if termo and not termo.startswith('#'):  # Ignorar linhas vazias e comentários
                termos.add(termo)
    
    termos = sorted(list(termos))
    print(f"✓ {len(termos)} termos únicos carregados do dataset")
    return termos


def buscar_matches(
    termos_dataset: List[str],
    termos_ontologia: Dict[str, Dict],
    threshold_parcial: float = 0.8
) -> Dict:
    """
    Busca matches entre termos do dataset e da ontologia
    
    Args:
        termos_dataset: Lista de termos do dataset
        termos_ontologia: Dicionário com termos normalizados da ontologia
        threshold_parcial: Threshold de similaridade para matches parciais
        
    Returns:
        Dict com resultados de matches
    """
    matches_exatos = []
    matches_parciais = []
    nao_encontrados = []
    
    print(f"\n🔎 Verificando matches ({len(termos_dataset)} termos)...")
    
    for termo_original in termos_dataset:
        termo_norm = normalizar_termo(termo_original)
        
        # Skip termos vazios após normalização
        if not termo_norm:
            nao_encontrados.append({
                'termo': termo_original,
                'motivo': 'termo vazio após normalização'
            })
            continue
        
        # Buscar match exato
        if termo_norm in termos_ontologia:
            match_info = termos_ontologia[termo_norm]
            matches_exatos.append({
                'termo_original': termo_original,
                'termo_normalizado': termo_norm,
                'labels': match_info['labels'],
                'altlabels': match_info['altlabels'],
                'classes': match_info['classes'],
                'tipo_match': match_info['tipo_match'],
                'confianca': 1.0
            })
        else:
            # Buscar matches parciais (palavras em comum)
            palavras_dataset = set(termo_norm.split())
            melhor_score = 0
            melhor_termo = None
            
            for termo_onto_norm, info_onto in termos_ontologia.items():
                palavras_onto = set(termo_onto_norm.split())
                
                # Calcular Jaccard similarity
                if palavras_dataset and palavras_onto:
                    intersecao = len(palavras_dataset & palavras_onto)
                    uniao = len(palavras_dataset | palavras_onto)
                    score = intersecao / uniao if uniao > 0 else 0
                    
                    if score > melhor_score:
                        melhor_score = score
                        melhor_termo = termo_onto_norm
            
            if melhor_score >= threshold_parcial:
                match_info = termos_ontologia[melhor_termo]
                matches_parciais.append({
                    'termo_original': termo_original,
                    'termo_normalizado': termo_norm,
                    'termo_ontologia': melhor_termo,
                    'labels': match_info['labels'],
                    'altlabels': match_info['altlabels'],
                    'classes': match_info['classes'],
                    'tipo_match': match_info['tipo_match'],
                    'confianca': melhor_score
                })
            else:
                nao_encontrados.append({
                    'termo': termo_original,
                    'termo_normalizado': termo_norm
                })
    
    return {
        'exatos': matches_exatos,
        'parciais': matches_parciais,
        'nao_encontrados': nao_encontrados,
        'total_termos': len(termos_dataset),
        'total_matches_exatos': len(matches_exatos),
        'total_matches_parciais': len(matches_parciais),
        'taxa_cobertura': (len(matches_exatos) + len(matches_parciais)) / len(termos_dataset) * 100
    }


def gerar_relatorio(resultados: Dict, caminho_saida: str):
    """
    Gera relatório em formato texto
    
    Args:
        resultados: Dicionário com resultados dos matches
        caminho_saida: Caminho para salvar o relatório
    """
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("=" * 100 + "\n")
        f.write("RELATÓRIO DE VERIFICAÇÃO DE MATCH - TERMOS vs ONTOLOGIA PLN\n")
        f.write("=" * 100 + "\n\n")
        
        # Estatísticas
        f.write("📊 ESTATÍSTICAS GERAIS\n")
        f.write("-" * 100 + "\n")
        f.write(f"Total de termos no dataset:     {resultados['total_termos']}\n")
        f.write(f"Matches exatos encontrados:     {resultados['total_matches_exatos']}\n")
        f.write(f"Matches parciais encontrados:   {resultados['total_matches_parciais']}\n")
        f.write(f"Termos não encontrados:         {len(resultados['nao_encontrados'])}\n")
        f.write(f"Taxa de cobertura:              {resultados['taxa_cobertura']:.2f}%\n")
        f.write("\n")
        
        # Matches Exatos
        f.write("\n" + "=" * 100 + "\n")
        f.write("✅ MATCHES EXATOS ({} termos)\n".format(len(resultados['exatos'])))
        f.write("=" * 100 + "\n\n")
        
        for i, match in enumerate(resultados['exatos'], 1):
            f.write(f"{i}. TERMO ORIGINAL: {match['termo_original']}\n")
            f.write(f"   Termo normalizado: {match['termo_normalizado']}\n")
            
            if match['labels']:
                f.write(f"   Labels: {', '.join(match['labels'])}\n")
            
            if match['altlabels']:
                f.write(f"   Alt Labels: {', '.join(match['altlabels'])}\n")
            
            f.write(f"   Tipo de match: {', '.join(match['tipo_match'])}\n")
            f.write(f"   Confiança: {match['confianca']:.1%}\n")
            f.write(f"   Classes: {len(match['classes'])} classe(s)\n")
            
            if match['classes']:
                for cls in match['classes'][:1]:  # Mostrar primeira classe
                    f.write(f"     - {cls}\n")
            
            f.write("\n")
        
        # Matches Parciais
        f.write("\n" + "=" * 100 + "\n")
        f.write("⚠️  MATCHES PARCIAIS ({} termos)\n".format(len(resultados['parciais'])))
        f.write("=" * 100 + "\n\n")
        
        for i, match in enumerate(resultados['parciais'], 1):
            f.write(f"{i}. TERMO ORIGINAL: {match['termo_original']}\n")
            f.write(f"   Termo normalizado: {match['termo_normalizado']}\n")
            f.write(f"   Correspondeu com: {match['termo_ontologia']}\n")
            
            if match['labels']:
                f.write(f"   Labels: {', '.join(match['labels'])}\n")
            
            if match['altlabels']:
                f.write(f"   Alt Labels: {', '.join(match['altlabels'])}\n")
            
            f.write(f"   Confiança: {match['confianca']:.1%}\n")
            f.write("\n")
        
        # Termos não encontrados
        f.write("\n" + "=" * 100 + "\n")
        f.write("❌ TERMOS NÃO ENCONTRADOS ({} termos)\n".format(len(resultados['nao_encontrados'])))
        f.write("=" * 100 + "\n\n")
        
        for i, item in enumerate(resultados['nao_encontrados'][:50], 1):  # Mostrar primeiros 50
            f.write(f"{i}. {item['termo']}\n")
            if 'termo_normalizado' in item:
                f.write(f"   Normalizado: {item['termo_normalizado']}\n")
        
        if len(resultados['nao_encontrados']) > 50:
            f.write(f"\n... e mais {len(resultados['nao_encontrados']) - 50} termos não encontrados\n")
        
        # Resumo
        f.write("\n" + "=" * 100 + "\n")
        f.write("RESUMO\n")
        f.write("=" * 100 + "\n")
        f.write(f"✓ {resultados['total_matches_exatos']} ({resultados['total_matches_exatos']/resultados['total_termos']*100:.1f}%) termos encontrados exatamente\n")
        f.write(f"⚠ {len(resultados['parciais'])} ({len(resultados['parciais'])/resultados['total_termos']*100:.1f}%) termos encontrados parcialmente\n")
        f.write(f"✗ {len(resultados['nao_encontrados'])} ({len(resultados['nao_encontrados'])/resultados['total_termos']*100:.1f}%) termos não encontrados\n")
        f.write(f"\n📈 Taxa de cobertura total: {resultados['taxa_cobertura']:.2f}%\n")


def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("VERIFICADOR DE MATCH - TERMOS vs ONTOLOGIA PLN".center(80))
    print("=" * 80 + "\n")
    
    # Verificar arquivos de entrada
    if not Path(ONTOLOGIA_PATH).exists():
        print(f"❌ Erro: Arquivo de ontologia não encontrado: {ONTOLOGIA_PATH}")
        return
    
    if not Path(ENTRADA_TERMOS_PATH).exists():
        print(f"❌ Erro: Arquivo de termos não encontrado: {ENTRADA_TERMOS_PATH}")
        return
    
    # Carregar dados
    g = carregar_ontologia(ONTOLOGIA_PATH)
    termos_dataset = carregar_termos_dataset(ENTRADA_TERMOS_PATH)
    termos_ontologia = extrair_termos_ontologia(g)
    
    # Buscar matches
    resultados = buscar_matches(termos_dataset, termos_ontologia)
    
    # Salvar resultados em JSON
    #print(f"\n💾 Salvando resultados em JSON: {SAIDA_MATCHES_PATH}")
    #with open(SAIDA_MATCHES_PATH, 'w', encoding='utf-8') as f:
    #    json.dump(resultados, f, ensure_ascii=False, indent=2)
    #print("✓ Arquivo JSON gerado com sucesso")
    
    # Gerar relatório
    print(f"📋 Gerando relatório: {SAIDA_RELATORIO_PATH}")
    gerar_relatorio(resultados, SAIDA_RELATORIO_PATH)
    print("✓ Relatório gerado com sucesso")
    
    # Resumo na tela
    print("\n" + "=" * 80)
    print("RESUMO DOS RESULTADOS".center(80))
    print("=" * 80)
    print(f"\n✅ Matches Exatos:      {resultados['total_matches_exatos']:4d} ({resultados['total_matches_exatos']/resultados['total_termos']*100:5.1f}%)")
    print(f"⚠️  Matches Parciais:    {len(resultados['parciais']):4d} ({len(resultados['parciais'])/resultados['total_termos']*100:5.1f}%)")
    print(f"❌ Não Encontrados:     {len(resultados['nao_encontrados']):4d} ({len(resultados['nao_encontrados'])/resultados['total_termos']*100:5.1f}%)")
    print(f"\n📈 Taxa de Cobertura: {resultados['taxa_cobertura']:.2f}%")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
