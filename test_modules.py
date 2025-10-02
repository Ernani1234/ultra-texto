#!/usr/bin/env python3
"""
Script de teste para verificar a integridade dos módulos do UltraTexto Pro
"""

import sys
import os
from pathlib import Path

# Adicionar diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Testa importação de todos os módulos"""
    print("🔍 Testando importações dos módulos...")
    
    try:
        # Testar tema
        from themes.dark_theme import DarkTheme
        print("✅ Tema escuro importado com sucesso")
        
        # Testar componentes de UI
        from modules.ui_components import (
            ProgressDialog, NotificationManager, FileTreeView, 
            SearchBox, StatusBar
        )
        print("✅ Componentes de UI importados com sucesso")
        
        # Testar gerenciador de exclusões
        from modules.exclusion_manager import ExclusionManager, ExclusionRule
        print("✅ Gerenciador de exclusões importado com sucesso")
        
        # Testar processador de arquivos
        from modules.file_processor import FileProcessor
        print("✅ Processador de arquivos importado com sucesso")
        
        # Testar scanner de diretórios
        from modules.directory_scanner import DirectoryScanner
        print("✅ Scanner de diretórios importado com sucesso")
        
        # Testar gerenciador de exportação
        from modules.export_manager import ExportManager
        print("✅ Gerenciador de exportação importado com sucesso")
        
        # Testar gerenciador de configurações
        from modules.config_manager import ConfigManager
        print("✅ Gerenciador de configurações importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_config_manager():
    """Testa o gerenciador de configurações"""
    print("\n🔧 Testando gerenciador de configurações...")
    
    try:
        from modules.config_manager import ConfigManager
        
        # Criar instância
        config = ConfigManager("test_config")
        print("✅ ConfigManager criado com sucesso")
        
        # Testar configurações básicas
        extensions = config.get_supported_extensions()
        print(f"✅ Extensões suportadas: {len(extensions)} tipos")
        
        # Testar get/set
        config.set("test.value", "teste")
        value = config.get("test.value")
        assert value == "teste", "Erro no get/set"
        print("✅ Get/Set funcionando corretamente")
        
        # Testar diretório de saída
        output_dir = config.get_output_directory()
        print(f"✅ Diretório de saída: {output_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do ConfigManager: {e}")
        return False

def test_exclusion_manager():
    """Testa o gerenciador de exclusões"""
    print("\n🚫 Testando gerenciador de exclusões...")
    
    try:
        from modules.exclusion_manager import ExclusionManager, ExclusionRule
        import time
        
        # Criar instância
        exclusion_mgr = ExclusionManager()
        print("✅ ExclusionManager criado com sucesso")
        
        # Criar perfil de teste com nome único
        test_profile_name = f"Teste_{int(time.time())}"
        exclusion_mgr.create_profile(test_profile_name, "Perfil de teste")
        print("✅ Perfil criado com sucesso")
        
        # Adicionar regra
        rule = ExclusionRule('extension', '.tmp', 'Arquivos temporários')
        exclusion_mgr.add_rule_to_current_profile(rule)
        print("✅ Regra adicionada com sucesso")
        
        # Testar exclusão
        should_exclude, reason = exclusion_mgr.should_exclude_path("test.tmp", False)
        assert should_exclude, "Regra de exclusão não funcionou"
        print("✅ Lógica de exclusão funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do ExclusionManager: {e}")
        return False

def test_directory_scanner():
    """Testa o scanner de diretórios"""
    print("\n🔍 Testando scanner de diretórios...")
    
    try:
        from modules.directory_scanner import DirectoryScanner
        
        # Criar instância
        supported_extensions = {'.py', '.txt', '.md'}
        scanner = DirectoryScanner(supported_extensions)
        print("✅ DirectoryScanner criado com sucesso")
        
        # Testar escaneamento do diretório atual
        current_dir = Path(__file__).parent
        root_node = scanner.scan_directory(str(current_dir), include_subdirectories=False)
        print(f"✅ Diretório escaneado: {len(root_node.children)} itens encontrados")
        
        # Testar geração de texto da árvore
        tree_text = scanner.generate_tree_text(root_node, max_items=10)
        assert len(tree_text) > 0, "Texto da árvore vazio"
        print("✅ Geração de texto da árvore funcionando")
        
        # Testar estatísticas
        stats = scanner.get_statistics()
        print(f"✅ Estatísticas: {stats['total_files']} arquivos, {stats['total_directories']} diretórios")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do DirectoryScanner: {e}")
        return False

def test_file_processor():
    """Testa o processador de arquivos"""
    print("\n📄 Testando processador de arquivos...")
    
    try:
        from modules.file_processor import FileProcessor
        
        # Criar instância
        supported_extensions = {'.py', '.txt', '.md'}
        processor = FileProcessor(supported_extensions)
        print("✅ FileProcessor criado com sucesso")
        
        # Testar escaneamento de diretório
        current_dir = Path(__file__).parent
        files_found = list(processor.scan_directory(str(current_dir), include_subdirectories=False))
        print(f"✅ Escaneamento funcionando: {len(files_found)} arquivos encontrados")
        
        # Testar estimativa de contagem
        file_count = processor.get_file_count_estimate(str(current_dir), include_subdirectories=False)
        print(f"✅ Estimativa de arquivos: {file_count}")
        
        # Testar formatação de tamanho
        size_str = processor._format_file_size(1024)
        assert "KB" in size_str, "Formatação de tamanho não funcionou"
        print("✅ Formatação de tamanho funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do FileProcessor: {e}")
        return False

def test_export_manager():
    """Testa o gerenciador de exportação"""
    print("\n📤 Testando gerenciador de exportação...")
    
    try:
        from modules.export_manager import ExportManager
        
        # Criar instância
        export_mgr = ExportManager()
        print("✅ ExportManager criado com sucesso")
        
        # Testar dados de exemplo
        test_data = {
            "root_path": "/test/path",
            "stats": {"total_files": 10, "total_size": 1024},
            "tree_items": [
                {"name": "test.py", "path": "/test/test.py", "is_directory": False}
            ]
        }
        
        # Testar exportação JSON
        json_output = "test_export.json"
        export_mgr.export_to_json(test_data, json_output)
        
        # Verificar se arquivo foi criado
        if Path(json_output).exists():
            print("✅ Exportação JSON funcionando")
            Path(json_output).unlink()  # Limpar
        else:
            print("❌ Arquivo JSON não foi criado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do ExportManager: {e}")
        return False

def test_file_structure():
    """Verifica a estrutura de arquivos"""
    print("\n📁 Verificando estrutura de arquivos...")
    
    required_files = [
        "themes/dark_theme.py",
        "modules/__init__.py",
        "modules/ui_components.py",
        "modules/exclusion_manager.py",
        "modules/file_processor.py",
        "modules/directory_scanner.py",
        "modules/export_manager.py",
        "modules/config_manager.py",
        "main_integrated.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {missing_files}")
        return False
    else:
        print("✅ Todos os arquivos necessários estão presentes")
        return True

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do UltraTexto Pro v2.0\n")
    
    tests = [
        ("Estrutura de arquivos", test_file_structure),
        ("Importações", test_imports),
        ("ConfigManager", test_config_manager),
        ("ExclusionManager", test_exclusion_manager),
        ("DirectoryScanner", test_directory_scanner),
        ("FileProcessor", test_file_processor),
        ("ExportManager", test_export_manager)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Executando: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
    
    print(f"\n{'='*50}")
    print(f"RESULTADO FINAL: {passed}/{total} testes passaram")
    print('='*50)
    
    if passed == total:
        print("🎉 Todos os testes passaram! O UltraTexto Pro está funcionando corretamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

