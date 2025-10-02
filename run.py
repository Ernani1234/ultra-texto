#!/usr/bin/env python3
"""
Script de execução simplificado para UltraTexto Pro v2.0
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Erro: Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        print("   Por favor, atualize o Python e tente novamente")
        return False
    return True

def check_tkinter():
    """Verifica se tkinter está disponível"""
    try:
        import tkinter
        return True
    except ImportError:
        print("❌ Erro: tkinter não está instalado")
        print("   Para instalar no Ubuntu/Debian:")
        print("   sudo apt-get install python3-tk")
        print("   ")
        print("   Para outros sistemas, tkinter geralmente vem com Python")
        return False

def check_dependencies():
    """Verifica todas as dependências"""
    print("🔍 Verificando dependências...")
    
    if not check_python_version():
        return False
    
    if not check_tkinter():
        return False
    
    print("✅ Todas as dependências estão OK!")
    return True

def run_tests():
    """Executa testes se solicitado"""
    print("🧪 Executando testes...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_modules.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            return True
        else:
            print("❌ Alguns testes falharam:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 UltraTexto Pro v2.0 - Iniciando...")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("main_integrated.py").exists():
        print("❌ Erro: Execute este script no diretório do UltraTexto Pro")
        print("   Certifique-se de que o arquivo main_integrated.py está presente")
        sys.exit(1)
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            if check_dependencies():
                success = run_tests()
                sys.exit(0 if success else 1)
            else:
                sys.exit(1)
        elif sys.argv[1] == "--help":
            print("Uso:")
            print("  python run.py          # Executar aplicação")
            print("  python run.py --test   # Executar testes")
            print("  python run.py --help   # Mostrar esta ajuda")
            sys.exit(0)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Executar aplicação
    print("🎯 Iniciando UltraTexto Pro...")
    try:
        # Importar e executar aplicação principal
        from main_integrated import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        print("   Verifique se todos os arquivos estão presentes")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

