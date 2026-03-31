#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar ontologia OWL usando RDFLib
Carrega a ontologia e apresenta todas as classes
"""

from rdflib import Graph, Namespace, RDF, RDFS, OWL
from pathlib import Path

def carregar_ontologia(caminho_arquivo):
    """Carrega a ontologia do arquivo OWL"""
    print("🔄 Carregando ontologia...")
    g = Graph()
    try:
        g.parse(caminho_arquivo, format='xml')
        print(f"✓ Ontologia carregada com sucesso!")
        print(f"  Total de triplas: {len(g)}")
        return g
    except Exception as e:
        print(f"✗ Erro ao carregar ontologia: {e}")
        return None

def validar_ontologia(g):
    """Valida a estrutura básica da ontologia"""
    print("\n📋 Validação da ontologia:")
    
    # Verificar namespace OWL
    owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
    rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    
    # Verificar se há classes
    classes = list(g.subjects(RDF.type, OWL.Class))
    print(f"  ✓ Classes encontradas: {len(classes)}")
    
    # Verificar se há propriedades
    object_props = list(g.subjects(RDF.type, OWL.ObjectProperty))
    datatype_props = list(g.subjects(RDF.type, OWL.DatatypeProperty))
    print(f"  ✓ Propriedades de objeto: {len(object_props)}")
    print(f"  ✓ Propriedades de dados: {len(datatype_props)}")
    
    # Verificar se há ontologia definida
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    print(f"  ✓ Ontologias declaradas: {len(ontologies)}")
    if ontologies:
        for ont in ontologies:
            labels = list(g.objects(ont, RDFS.label))
            print(f"    - {ont}")
            if labels:
                print(f"      Label: {labels[0]}")
    
    return {
        'classes': classes,
        'object_props': object_props,
        'datatype_props': datatype_props
    }

def listar_classes(g, dados_validacao):
    """Lista todas as classes da ontologia com informações"""
    print("\n📚 Classes da Ontologia:")
    print("=" * 80)
    
    classes = dados_validacao['classes']
    
    if not classes:
        print("  Nenhuma classe encontrada!")
        return
    
    # Ordena as classes por nome
    classes_ordenadas = sorted(classes, key=lambda x: str(x))
    
    for idx, classe in enumerate(classes_ordenadas, 1):
        print(f"\n{idx}. {classe}")
        
        # Obter labels (português e inglês)
        labels_pt = list(g.objects(classe, RDFS.label))
        labels_en = list(g.objects(classe, RDFS.label))
        
        for label in labels_pt:
            lang = label.language if hasattr(label, 'language') else 'N/A'
            if lang == 'pt':
                print(f"   🔤 Label (PT): {label}")
        
        for label in labels_en:
            lang = label.language if hasattr(label, 'language') else 'N/A'
            if lang == 'en':
                print(f"   🔤 Label (EN): {label}")
        
        # Obter comentários
        comentarios = list(g.objects(classe, RDFS.comment))
        if comentarios:
            print(f"   📝 Descrição: {comentarios[0]}")
        
        # Obter superclasses
        superclasses = list(g.objects(classe, RDFS.subClassOf))
        if superclasses:
            print(f"   ↑ Subclasse de: {superclasses[0]}")
        
        # Obter subclasses
        subclasses = list(g.subjects(RDFS.subClassOf, classe))
        if subclasses:
            count = len(subclasses)
            print(f"   ↓ Superclasse de {count} classe(s)")

def listar_propriedades(g, dados_validacao):
    """Lista as propriedades de objeto da ontologia"""
    print("\n" + "=" * 80)
    print("\n🔗 Propriedades de Objeto:")
    print("=" * 80)
    
    object_props = dados_validacao['object_props']
    
    if not object_props:
        print("  Nenhuma propriedade de objeto encontrada!")
        return
    
    object_props_ordenadas = sorted(object_props, key=lambda x: str(x))
    
    for idx, prop in enumerate(object_props_ordenadas, 1):
        print(f"\n{idx}. {prop}")
        
        # Obter labels
        labels = list(g.objects(prop, RDFS.label))
        if labels:
            print(f"   🔤 Label: {labels[0]}")
        
        # Obter comentários
        comentarios = list(g.objects(prop, RDFS.comment))
        if comentarios:
            print(f"   📝 Descrição: {comentarios[0]}")
        
        # Obter domínio e range
        domains = list(g.objects(prop, RDFS.domain))
        ranges = list(g.objects(prop, RDFS.range))
        
        if domains:
            print(f"   📌 Domínio: {domains[0]}")
        if ranges:
            print(f"   🎯 Range: {ranges[0]}")

def main():
    """Função principal"""
    arquivo_ontologia = Path(__file__).parent / "ontologia_pln_v3_melhorada.owl"
    
    if not arquivo_ontologia.exists():
        print(f"✗ Arquivo não encontrado: {arquivo_ontologia}")
        return
    
    print(f"📂 Carregando: {arquivo_ontologia}\n")
    
    # Carregar ontologia
    g = carregar_ontologia(str(arquivo_ontologia))
    if g is None:
        return
    
    # Validar
    dados = validar_ontologia(g)
    
    # Listar classes
    listar_classes(g, dados)
    
    # Listar propriedades
    listar_propriedades(g, dados)
    
    print("\n" + "=" * 80)
    print("✓ Validação concluída com sucesso!")
    print("=" * 80)

if __name__ == "__main__":
    main()
