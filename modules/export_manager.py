"""
Módulo de exportação em múltiplos formatos para UltraTexto Pro
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import base64

class ExportManager:
    """Gerenciador de exportação em múltiplos formatos"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        self.create_default_templates()
    
    def create_default_templates(self):
        """Cria templates padrão se não existirem"""
        
        # Template HTML para estrutura de diretórios
        html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estrutura de Diretórios - UltraTexto Pro</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(45, 45, 45, 0.8);
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        
        .header h1 {
            color: #14a085;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #b0b0b0;
            font-size: 1.1em;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(45, 45, 45, 0.8);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #555;
        }
        
        .stat-card .number {
            font-size: 2em;
            font-weight: bold;
            color: #14a085;
            display: block;
        }
        
        .stat-card .label {
            color: #b0b0b0;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .tree-container {
            background: rgba(45, 45, 45, 0.8);
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #555;
        }
        
        .tree {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .tree-item {
            margin: 2px 0;
            white-space: pre;
        }
        
        .tree-item.directory {
            color: #14a085;
            font-weight: bold;
        }
        
        .tree-item.file {
            color: #ffffff;
        }
        
        .tree-item.excluded {
            color: #f44336;
            text-decoration: line-through;
        }
        
        .tree-item.supported {
            color: #4caf50;
        }
        
        .icon {
            margin-right: 5px;
        }
        
        .search-box {
            margin-bottom: 20px;
            text-align: center;
        }
        
        .search-box input {
            background: rgba(61, 61, 61, 0.8);
            border: 1px solid #777;
            border-radius: 25px;
            padding: 12px 20px;
            color: #ffffff;
            font-size: 16px;
            width: 300px;
            outline: none;
        }
        
        .search-box input:focus {
            border-color: #14a085;
            box-shadow: 0 0 10px rgba(20, 160, 133, 0.3);
        }
        
        .controls {
            margin-bottom: 20px;
            text-align: center;
        }
        
        .btn {
            background: #14a085;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            margin: 0 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #0d7377;
        }
        
        .btn.secondary {
            background: #3d3d3d;
        }
        
        .btn.secondary:hover {
            background: #555;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #b0b0b0;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .search-box input {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 Estrutura de Diretórios</h1>
            <div class="subtitle">Gerado pelo UltraTexto Pro em {{timestamp}}</div>
            <div class="subtitle">Diretório: {{root_path}}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <span class="number">{{total_directories}}</span>
                <div class="label">Diretórios</div>
            </div>
            <div class="stat-card">
                <span class="number">{{total_files}}</span>
                <div class="label">Arquivos</div>
            </div>
            <div class="stat-card">
                <span class="number">{{total_size}}</span>
                <div class="label">Tamanho Total</div>
            </div>
            <div class="stat-card">
                <span class="number">{{excluded_items}}</span>
                <div class="label">Itens Excluídos</div>
            </div>
        </div>
        
        <div class="tree-container">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Buscar arquivos e pastas..." onkeyup="filterTree()">
            </div>
            
            <div class="controls">
                <button class="btn" onclick="expandAll()">Expandir Tudo</button>
                <button class="btn secondary" onclick="collapseAll()">Recolher Tudo</button>
                <button class="btn secondary" onclick="toggleExcluded()">Mostrar/Ocultar Excluídos</button>
            </div>
            
            <div class="tree" id="treeContent">
{{tree_content}}
            </div>
        </div>
        
        <div class="footer">
            <p>Gerado por UltraTexto Pro v2.0 | {{generation_time}}</p>
        </div>
    </div>
    
    <script>
        function filterTree() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const treeItems = document.querySelectorAll('.tree-item');
            
            treeItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
        
        function expandAll() {
            // Implementar expansão de diretórios
            console.log('Expandir todos os diretórios');
        }
        
        function collapseAll() {
            // Implementar recolhimento de diretórios
            console.log('Recolher todos os diretórios');
        }
        
        function toggleExcluded() {
            const excludedItems = document.querySelectorAll('.tree-item.excluded');
            excludedItems.forEach(item => {
                if (item.style.display === 'none') {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>"""
        
        html_template_path = self.templates_dir / "directory_structure.html"
        if not html_template_path.exists():
            with open(html_template_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
        
        # Template HTML para relatório de processamento
        report_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Processamento - UltraTexto Pro</title>
    <style>
        /* Mesmo CSS do template anterior */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%); color: #ffffff; line-height: 1.6; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: rgba(45, 45, 45, 0.8); border-radius: 10px; padding: 30px; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); }
        .header h1 { color: #14a085; font-size: 2.5em; margin-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: rgba(45, 45, 45, 0.8); border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); border: 1px solid #555; }
        .stat-card .number { font-size: 2em; font-weight: bold; color: #14a085; display: block; }
        .stat-card .label { color: #b0b0b0; font-size: 0.9em; margin-top: 5px; }
        .section { background: rgba(45, 45, 45, 0.8); border-radius: 10px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); border: 1px solid #555; }
        .section h2 { color: #14a085; margin-bottom: 20px; }
        .chart-container { height: 300px; margin: 20px 0; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Processamento</h1>
            <div class="subtitle">{{timestamp}}</div>
        </div>
        
        <div class="stats">
            {{stats_cards}}
        </div>
        
        <div class="section">
            <h2>Distribuição por Extensão</h2>
            <div class="chart-container">
                <canvas id="extensionChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>Detalhes do Processamento</h2>
            {{processing_details}}
        </div>
    </div>
    
    <script>
        // Gráfico de distribuição por extensão
        const ctx = document.getElementById('extensionChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {{chart_data}},
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>"""
        
        report_template_path = self.templates_dir / "processing_report.html"
        if not report_template_path.exists():
            with open(report_template_path, 'w', encoding='utf-8') as f:
                f.write(report_template)
    
    def export_to_json(self, data: Dict, output_path: str, pretty: bool = True) -> str:
        """Exporta dados para formato JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Preparar dados para JSON
        json_data = {
            "metadata": {
                "generated_by": "UltraTexto Pro v2.0",
                "timestamp": datetime.now().isoformat(),
                "format_version": "1.0"
            },
            "data": data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            else:
                json.dump(json_data, f, ensure_ascii=False, default=str)
        
        return str(output_path)
    
    def export_to_xml(self, data: Dict, output_path: str, root_name: str = "UltraTextoData") -> str:
        """Exporta dados para formato XML"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Criar elemento raiz
        root = ET.Element(root_name)
        
        # Adicionar metadados
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "generated_by").text = "UltraTexto Pro v2.0"
        ET.SubElement(metadata, "timestamp").text = datetime.now().isoformat()
        ET.SubElement(metadata, "format_version").text = "1.0"
        
        # Adicionar dados
        data_element = ET.SubElement(root, "data")
        self._dict_to_xml(data, data_element)
        
        # Formatar XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        return str(output_path)
    
    def _dict_to_xml(self, data: Any, parent: ET.Element):
        """Converte dicionário para elementos XML recursivamente"""
        if isinstance(data, dict):
            for key, value in data.items():
                # Sanitizar nome do elemento
                element_name = str(key).replace(' ', '_').replace('-', '_')
                element = ET.SubElement(parent, element_name)
                self._dict_to_xml(value, element)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                item_element = ET.SubElement(parent, f"item_{i}")
                self._dict_to_xml(item, item_element)
        
        else:
            parent.text = str(data) if data is not None else ""
    
    def export_directory_structure_to_html(self, structure_data: Dict, output_path: str) -> str:
        """Exporta estrutura de diretórios para HTML interativo"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Carregar template
        template_path = self.templates_dir / "directory_structure.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Preparar dados
        stats = structure_data.get('stats', {})
        tree_items = structure_data.get('tree_items', [])
        
        # Gerar conteúdo da árvore
        tree_content = self._generate_html_tree_content(tree_items)
        
        # Substituir placeholders
        html_content = template.replace('{{timestamp}}', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        html_content = html_content.replace('{{root_path}}', structure_data.get('root_path', ''))
        html_content = html_content.replace('{{total_directories}}', str(stats.get('total_directories', 0)))
        html_content = html_content.replace('{{total_files}}', str(stats.get('total_files', 0)))
        html_content = html_content.replace('{{total_size}}', self._format_file_size(stats.get('total_size', 0)))
        html_content = html_content.replace('{{excluded_items}}', str(stats.get('excluded_files', 0) + stats.get('excluded_directories', 0)))
        html_content = html_content.replace('{{tree_content}}', tree_content)
        html_content = html_content.replace('{{generation_time}}', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_html_tree_content(self, tree_items: List[Dict]) -> str:
        """Gera conteúdo HTML da árvore de arquivos"""
        html_lines = []
        
        for item in tree_items:
            name = item.get('name', '')
            path = item.get('path', '')
            is_directory = item.get('is_directory', False)
            is_excluded = item.get('is_excluded', False)
            is_supported = item.get('is_supported', False)
            size = item.get('size', 0)
            prefix = item.get('prefix', '')
            
            # Determinar classes CSS
            classes = ['tree-item']
            if is_directory:
                classes.append('directory')
            else:
                classes.append('file')
            
            if is_excluded:
                classes.append('excluded')
            elif is_supported:
                classes.append('supported')
            
            # Determinar ícone
            if is_directory:
                icon = "📁" if not is_excluded else "📁❌"
            else:
                if is_excluded:
                    icon = "📄❌"
                elif is_supported:
                    icon = "📄✅"
                else:
                    icon = "📄"
            
            # Formatear linha
            size_str = f" ({self._format_file_size(size)})" if not is_directory and size > 0 else ""
            line = f'{prefix}<span class="icon">{icon}</span>{name}{size_str}'
            
            html_lines.append(f'<div class="{" ".join(classes)}" data-path="{path}">{line}</div>')
        
        return '\n'.join(html_lines)
    
    def export_processing_report_to_html(self, report_data: Dict, output_path: str) -> str:
        """Exporta relatório de processamento para HTML"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Carregar template
        template_path = self.templates_dir / "processing_report.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Preparar dados
        stats = report_data.get('stats', {})
        
        # Gerar cards de estatísticas
        stats_cards = self._generate_stats_cards(stats)
        
        # Gerar dados do gráfico
        chart_data = self._generate_chart_data(stats)
        
        # Gerar detalhes do processamento
        processing_details = self._generate_processing_details(report_data)
        
        # Substituir placeholders
        html_content = template.replace('{{timestamp}}', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        html_content = html_content.replace('{{stats_cards}}', stats_cards)
        html_content = html_content.replace('{{chart_data}}', json.dumps(chart_data))
        html_content = html_content.replace('{{processing_details}}', processing_details)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_stats_cards(self, stats: Dict) -> str:
        """Gera cards de estatísticas"""
        cards = []
        
        stats_items = [
            ('processed_files', 'Arquivos Processados'),
            ('excluded_files', 'Arquivos Excluídos'),
            ('total_directories', 'Diretórios'),
            ('processing_speed', 'Arquivos/seg', lambda x: f"{x:.1f}"),
            ('duration', 'Duração (s)', lambda x: f"{x:.1f}"),
            ('total_size', 'Tamanho Total', self._format_file_size)
        ]
        
        for key, label, *formatter in stats_items:
            value = stats.get(key, 0)
            if formatter:
                formatted_value = formatter[0](value)
            else:
                formatted_value = str(value)
            
            cards.append(f'''
            <div class="stat-card">
                <span class="number">{formatted_value}</span>
                <div class="label">{label}</div>
            </div>
            ''')
        
        return ''.join(cards)
    
    def _generate_chart_data(self, stats: Dict) -> Dict:
        """Gera dados para gráfico de distribuição por extensão"""
        found_extensions = stats.get('found_extensions', [])
        
        # Contar arquivos por extensão (simulado)
        extension_counts = {}
        for ext in found_extensions:
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
        
        # Cores para o gráfico
        colors = [
            '#14a085', '#f44336', '#ff9800', '#4caf50', '#2196f3',
            '#9c27b0', '#ff5722', '#795548', '#607d8b', '#e91e63'
        ]
        
        labels = list(extension_counts.keys())
        data = list(extension_counts.values())
        background_colors = colors[:len(labels)]
        
        return {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': background_colors,
                'borderColor': '#ffffff',
                'borderWidth': 2
            }]
        }
    
    def _generate_processing_details(self, report_data: Dict) -> str:
        """Gera detalhes do processamento"""
        details = []
        
        # Informações básicas
        details.append('<h3>Informações Básicas</h3>')
        details.append('<ul>')
        details.append(f'<li><strong>Diretório processado:</strong> {report_data.get("root_path", "N/A")}</li>')
        details.append(f'<li><strong>Modo de processamento:</strong> {report_data.get("processing_mode", "N/A")}</li>')
        details.append(f'<li><strong>Incluir subdiretórios:</strong> {"Sim" if report_data.get("include_subdirectories") else "Não"}</li>')
        details.append('</ul>')
        
        # Erros (se houver)
        errors = report_data.get('stats', {}).get('errors', [])
        if errors:
            details.append('<h3>Erros Encontrados</h3>')
            details.append('<ul>')
            for error in errors[:10]:  # Limitar a 10 erros
                details.append(f'<li>{error}</li>')
            if len(errors) > 10:
                details.append(f'<li>... e mais {len(errors) - 10} erros</li>')
            details.append('</ul>')
        
        # Extensões encontradas
        found_extensions = report_data.get('stats', {}).get('found_extensions', [])
        if found_extensions:
            details.append('<h3>Extensões Encontradas</h3>')
            details.append('<p>' + ', '.join(sorted(found_extensions)) + '</p>')
        
        return ''.join(details)
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Formata tamanho do arquivo"""
        if size_bytes == 0:
            return "0 B"
        
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
    
    def export_to_markdown(self, data: Dict, output_path: str) -> str:
        """Exporta dados para formato Markdown"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("# Relatório UltraTexto Pro\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            # Estatísticas
            if 'stats' in data:
                stats = data['stats']
                f.write("## 📊 Estatísticas\n\n")
                f.write("| Métrica | Valor |\n")
                f.write("|---------|-------|\n")
                
                for key, value in stats.items():
                    if isinstance(value, (int, float)):
                        if key == 'total_size' or key == 'processed_size':
                            value = self._format_file_size(value)
                        elif key == 'duration':
                            value = f"{value:.1f}s"
                        elif key == 'processing_speed':
                            value = f"{value:.1f} arquivos/s"
                    
                    f.write(f"| {key.replace('_', ' ').title()} | {value} |\n")
                
                f.write("\n")
            
            # Estrutura de arquivos
            if 'tree_items' in data:
                f.write("## 📁 Estrutura de Arquivos\n\n")
                f.write("```\n")
                for item in data['tree_items']:
                    prefix = item.get('prefix', '')
                    name = item.get('name', '')
                    is_directory = item.get('is_directory', False)
                    is_excluded = item.get('is_excluded', False)
                    
                    icon = "📁" if is_directory else "📄"
                    if is_excluded:
                        icon += "❌"
                    
                    f.write(f"{prefix}{icon} {name}\n")
                f.write("```\n\n")
            
            # Detalhes adicionais
            if 'details' in data:
                f.write("## 📋 Detalhes\n\n")
                for detail in data['details']:
                    f.write(f"- {detail}\n")
                f.write("\n")
        
        return str(output_path)
    
    def create_archive(self, files: List[str], output_path: str, format_type: str = 'zip') -> str:
        """Cria arquivo compactado com os resultados"""
        import zipfile
        import tarfile
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format_type == 'zip':
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    file_path = Path(file_path)
                    if file_path.exists():
                        zipf.write(file_path, file_path.name)
        
        elif format_type == 'tar.gz':
            with tarfile.open(output_path, 'w:gz') as tarf:
                for file_path in files:
                    file_path = Path(file_path)
                    if file_path.exists():
                        tarf.add(file_path, file_path.name)
        
        else:
            raise ValueError(f"Formato de arquivo não suportado: {format_type}")
        
        return str(output_path)

