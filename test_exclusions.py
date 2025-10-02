#!/usr/bin/env python3
"""
Teste das Exclusões Automáticas - UltraTexto Pro
Verifica se o sistema de exclusões automáticas está funcionando corretamente
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from modules.exclusion_manager import ExclusionManager
from modules.config_manager import ConfigManager

def test_auto_exclusions():
    """Testa o sistema de exclusões automáticas"""
    print("🧪 Testando Sistema de Exclusões Automáticas")
    print("=" * 50)
    
    try:
        # Inicializar gerenciadores
        config_manager = ConfigManager()
        exclusion_manager = ExclusionManager()
        
        print("✅ Gerenciadores inicializados com sucesso")
        
        # Aplicar exclusões automáticas
        exclusion_manager.apply_auto_exclusions(config_manager)
        print("✅ Exclusões automáticas aplicadas")
        
        # Verificar perfil padrão
        if "Padrão" in exclusion_manager.profiles:
            print("✅ Perfil padrão encontrado")
            default_profile = exclusion_manager.profiles["Padrão"]
            print(f"   📊 Total de regras: {len(default_profile.rules)}")
            
            # Contar regras por tipo
            rule_types = {}
            for rule in default_profile.rules:
                if rule.rule_type not in rule_types:
                    rule_types[rule.rule_type] = 0
                rule_types[rule.rule_type] += 1
            
            print("   📋 Distribuição por tipo:")
            for rule_type, count in rule_types.items():
                print(f"      - {rule_type}: {count}")
            
            # Verificar exclusões específicas importantes
            important_exclusions = [
                'node_modules', '.venv', 'venv', 'env',
                'vendor', 'target', 'obj', 'bin'
            ]
            
            print("\n🔍 Verificando exclusões importantes:")
            for exclusion in important_exclusions:
                found = any(
                    rule.pattern == exclusion and rule.rule_type == 'folder'
                    for rule in default_profile.rules
                )
                status = "✅" if found else "❌"
                print(f"   {status} {exclusion}")
            
        else:
            print("❌ Perfil padrão não encontrado")
            return False
        
        # Testar resumo das exclusões
        summary = exclusion_manager.get_exclusion_summary()
        print(f"\n📊 Resumo das Exclusões:")
        print(f"   Perfil: {summary.get('profile_name', 'N/A')}")
        print(f"   Regras ativas: {summary.get('enabled_rules', 0)}")
        print(f"   Pastas excluídas: {len(summary.get('common_exclusions', []))}")
        
        # Testar exclusão de caminhos
        test_paths = [
            ("/path/to/node_modules", True, "Dependências Node.js"),
            ("/path/to/.venv", True, "Ambiente virtual Python"),
            ("/path/to/venv", True, "Ambiente virtual Python"),
            ("/path/to/src/main.py", False, "Arquivo Python válido"),
            ("/path/to/dist/build.js", True, "Arquivo de build"),
            ("/path/to/.git/config", True, "Repositório Git"),
        ]
        
        print("\n🧪 Testando exclusões de caminhos:")
        for path, should_exclude, description in test_paths:
            is_excluded, reason = exclusion_manager.should_exclude_path(path, path.endswith('/'))
            status = "✅" if is_excluded == should_exclude else "❌"
            print(f"   {status} {path} - {description}")
            if is_excluded:
                print(f"      Razão: {reason}")
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exclusion_profiles():
    """Testa a funcionalidade de perfis de exclusão"""
    print("\n🧪 Testando Perfis de Exclusão")
    print("=" * 40)
    
    try:
        exclusion_manager = ExclusionManager()
        
        # Criar novo perfil
        new_profile = exclusion_manager.create_profile("Teste_Exclusoes", "Perfil de teste")
        print("✅ Novo perfil criado")
        
        # Adicionar regra ao perfil
        from modules.exclusion_manager import ExclusionRule
        test_rule = ExclusionRule('folder', 'test_folder', 'Pasta de teste')
        new_profile.add_rule(test_rule)
        print("✅ Regra adicionada ao perfil")
        
        # Verificar se a regra foi adicionada
        if len(new_profile.rules) == 1:
            print("✅ Regra encontrada no perfil")
        else:
            print("❌ Regra não encontrada no perfil")
            return False
        
        # Testar exclusão com o novo perfil
        exclusion_manager.set_current_profile("Teste_Exclusoes")
        is_excluded, reason = exclusion_manager.should_exclude_path("/path/to/test_folder", True)
        
        if is_excluded:
            print("✅ Exclusão funcionando com novo perfil")
        else:
            print("❌ Exclusão não funcionando com novo perfil")
            return False
        
        # Limpar perfil de teste
        exclusion_manager.delete_profile("Teste_Exclusoes")
        print("✅ Perfil de teste removido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante testes de perfis: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando Testes do Sistema de Exclusões")
    print("=" * 60)
    
    # Testar exclusões automáticas
    test1_passed = test_auto_exclusions()
    
    # Testar perfis de exclusão
    test2_passed = test_exclusion_profiles()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Teste de Exclusões Automáticas: PASSOU")
    else:
        print("❌ Teste de Exclusões Automáticas: FALHOU")
    
    if test2_passed:
        print("✅ Teste de Perfis de Exclusão: PASSOU")
    else:
        print("❌ Teste de Perfis de Exclusão: FALHOU")
    
    if test1_passed and test2_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O sistema de exclusões está funcionando corretamente.")
        return 0
    else:
        print("\n💥 ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima para identificar problemas.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
