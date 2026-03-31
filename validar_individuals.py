#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar e explorar individuals da ontologia de PLN
"""

from rdflib import Graph, Namespace, RDF, RDFS, OWL
from pathlib import Path
from collections import defaultdict

def carregar_ontologia_com_individuals():
    """Carrega a ontologia principal e os individuals"""
    print("🔄 Carregando ontologias...")
    g = Graph()
    
    # Carregar a ontologia principal
    ontologia_principal = Path(__file__).parent / "ontologia_pln_v3_melhorada.owl"
    if ontologia_principal.exists():
        g.parse(str(ontologia_principal), format='xml')
        print(f"✓ Ontologia principal carregada")
    
    # Carregar os individuals
    ontologia_individuals = Path(__file__).parent / "ontologia_pln_v3_individuals.owl"
    if ontologia_individuals.exists():
        g.parse(str(ontologia_individuals), format='xml')
        print(f"✓ Arquivo de individuals carregado")
    else:
        print(f"⚠ Arquivo de individuals não encontrado")
        return None
    
    print(f"✓ Total de triplas carregadas: {len(g)}")
    return g

def agrupar_individuals_por_tipo(g):
    """Agrupa os individuals pelas suas classes"""
    individuals_por_tipo = defaultdict(list)
    
    # Definir namespace
    pln = Namespace("http://www.ufrgs.br/ontologies/pln_v3.owl#")
    
    # Encontrar todos os subjects que são instâncias
    for subject in g.subjects():
        # Pular ontologias
        if (subject, RDF.type, OWL.Ontology) in g:
            continue
        
        # Encontrar os tipos (classes) deste individual
        tipos = list(g.objects(subject, RDF.type))
        
        for tipo in tipos:
            # Extrair o nome da classe
            tipo_str = str(tipo)
            tipo_nome = tipo_str.split('#')[-1] if '#' in tipo_str else tipo_str
            
            individuals_por_tipo[tipo_nome].append({
                'uri': subject,
                'tipo_uri': tipo,
                'labels_pt': [str(l) for l in g.objects(subject, RDFS.label) 
                             if hasattr(l, 'language') and l.language == 'pt'],
                'labels_en': [str(l) for l in g.objects(subject, RDFS.label) 
                             if hasattr(l, 'language') and l.language == 'en'],
                'comments': [str(c) for c in g.objects(subject, RDFS.comment)],
                'notations': [str(n) for n in g.objects(subject, Namespace("http://www.w3.org/2004/02/skos/core#").notation)]
            })
    
    return individuals_por_tipo

def exibir_relatorio(g, individuals_por_tipo):
    """Exibe um relatório formatado dos individuals"""
    
    total_individuals = sum(len(inds) for inds in individuals_por_tipo.values())
    
    print("\n" + "=" * 100)
    print("📊 RELATÓRIO DE INDIVIDUALS DA ONTOLOGIA PLN v3")
    print("=" * 100)
    print(f"\n✓ Total de tipos (classes) com individuals: {len(individuals_por_tipo)}")
    print(f"✓ Total de individuals: {total_individuals}")
    
    print("\n" + "=" * 100)
    print("📚 INDIVIDUALS POR TIPO")
    print("=" * 100)
    
    # Ordenar por tipo
    for tipo in sorted(individuals_por_tipo.keys()):
        individuals = individuals_por_tipo[tipo]
        print(f"\n📌 {tipo} ({len(individuals)} individual{'' if len(individuals) == 1 else 's'})")
        print("-" * 100)
        
        for idx, indiv in enumerate(individuals, 1):
            print(f"\n  {idx}. {str(indiv['uri']).split('#')[-1]}")
            
            # Labels
            if indiv['labels_pt']:
                for label in indiv['labels_pt']:
                    print(f"     🇧🇷 {label}")
            if indiv['labels_en']:
                for label in indiv['labels_en']:
                    print(f"     🇬🇧 {label}")
            
            # Comments
            if indiv['comments']:
                for comment in indiv['comments']:
                    print(f"     📝 {comment}")
            
            # Notations
            if indiv['notations']:
                for notation in indiv['notations']:
                    print(f"     🏷️ {notation}")

def gerar_relatorio_html(individuals_por_tipo):
    """Gera relatório em HTML"""
    
    total_individuals = sum(len(inds) for inds in individuals_por_tipo.values())
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Individuals da Ontologia PLN v3</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .stat-box h3 {{
            margin: 0 0 10px 0;
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
        }}
        .stat-box .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .type-group {{
            background-color: #f9f9f9;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            border-left: 4px solid #764ba2;
        }}
        .type-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #764ba2;
            margin-bottom: 10px;
        }}
        .individual-item {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 3px;
            border-left: 4px solid #27ae60;
        }}
        .individual-name {{
            font-weight: bold;
            color: #2c3e50;
            font-family: monospace;
            font-size: 0.95em;
        }}
        .label {{
            margin: 8px 0;
            color: #555;
        }}
        .label.pt {{
            color: #e74c3c;
        }}
        .label.en {{
            color: #3498db;
        }}
        .comment {{
            margin: 8px 0;
            font-style: italic;
            color: #666;
            border-left: 2px solid #f39c12;
            padding-left: 10px;
        }}
        .notation {{
            display: inline-block;
            background-color: #ecf0f1;
            padding: 3px 8px;
            border-radius: 3px;
            margin: 5px 5px 5px 0;
            font-family: monospace;
            font-size: 0.9em;
        }}
        .count {{
            background-color: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Individuals da Ontologia PLN v3</h1>
        <p>Exemplos concretos de indivíduos para as classes da ontologia</p>
    </div>

    <div class="stats">
        <div class="stat-box">
            <h3>Total de Tipos</h3>
            <div class="value">{len(individuals_por_tipo)}</div>
        </div>
        <div class="stat-box" style="border-left-color: #27ae60;">
            <h3>Total de Individuals</h3>
            <div class="value" style="color: #27ae60;">{total_individuals}</div>
        </div>
    </div>

    <div class="section">
        <h2>🔍 Individuals por Tipo</h2>
"""
    
    # Ordenar por tipo
    for tipo in sorted(individuals_por_tipo.keys()):
        individuals = individuals_por_tipo[tipo]
        
        html += f"""        <div class="type-group">
            <div class="type-name">{tipo} <span class="count">{len(individuals)}</span></div>
"""
        
        for indiv in individuals:
            individual_nome = str(indiv['uri']).split('#')[-1]
            
            html += f"""            <div class="individual-item">
                <div class="individual-name">• {individual_nome}</div>
"""
            
            # Labels
            for label in indiv['labels_pt']:
                html += f'                <div class="label pt">🇧🇷 {label}</div>\n'
            
            for label in indiv['labels_en']:
                html += f'                <div class="label en">🇬🇧 {label}</div>\n'
            
            # Comments
            for comment in indiv['comments']:
                html += f'                <div class="comment">{comment}</div>\n'
            
            # Notations
            if indiv['notations']:
                html += '                <div style="margin: 8px 0;">'
                for notation in indiv['notations']:
                    html += f'<span class="notation">{notation}</span>'
                html += '</div>\n'
            
            html += """            </div>
"""
        
        html += """        </div>
"""
    
    html += """    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente pela ferramenta de validação de individuals</p>
    </div>
</body>
</html>
"""
    return html

def main():
    """Função principal"""
    
    # Carregar
    g = carregar_ontologia_com_individuals()
    if g is None:
        return
    
    # Agrupar
    print("\n🔄 Analisando individuals...")
    individuals_por_tipo = agrupar_individuals_por_tipo(g)
    
    if not individuals_por_tipo:
        print("⚠ Nenhum individual encontrado!")
        return
    
    # Exibir relatório em console
    exibir_relatorio(g, individuals_por_tipo)
    
    # Gerar HTML
    print("\n📝 Gerando relatório HTML...")
    html = gerar_relatorio_html(individuals_por_tipo)
    
    arquivo_html = Path(__file__).parent / "relatorio_individuals.html"
    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Relatório salvo em: {arquivo_html}")
    print("\n" + "=" * 100)
    print("✓ Validação concluída com sucesso!")
    print("=" * 100)

if __name__ == "__main__":
    main()
