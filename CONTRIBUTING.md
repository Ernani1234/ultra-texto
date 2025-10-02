# 🤝 Guia de Contribuição - UltraTexto Pro

<div align="center">

![Contributing Banner](https://via.placeholder.com/800x200/2b2b2b/ffffff?text=Contribua+com+o+UltraTexto+Pro)

**Obrigado por considerar contribuir com o UltraTexto Pro!**

[![Contributors](https://img.shields.io/github/contributors/seu-usuario/ultra-texto-pro)](https://github.com/seu-usuario/ultra-texto-pro/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/seu-usuario/ultra-texto-pro)](https://github.com/seu-usuario/ultra-texto-pro/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/seu-usuario/ultra-texto-pro)](https://github.com/seu-usuario/ultra-texto-pro/pulls)

</div>

---

## 📋 Índice

- [🎯 Como Contribuir](#-como-contribuir)
- [🏗️ Configuração do Ambiente](#️-configuração-do-ambiente)
- [📝 Padrões de Código](#-padrões-de-código)
- [🧪 Testes](#-testes)
- [📖 Documentação](#-documentação)
- [🐛 Reportando Bugs](#-reportando-bugs)
- [💡 Sugerindo Melhorias](#-sugerindo-melhorias)
- [🔄 Processo de Pull Request](#-processo-de-pull-request)
- [👥 Comunidade](#-comunidade)

---

## 🎯 Como Contribuir

Existem várias maneiras de contribuir com o UltraTexto Pro:

### 🔧 **Desenvolvimento**
- Implementar novas funcionalidades
- Corrigir bugs existentes
- Melhorar performance
- Refatorar código

### 📝 **Documentação**
- Melhorar documentação existente
- Criar tutoriais e guias
- Traduzir documentação
- Corrigir erros de escrita

### 🧪 **Testes**
- Reportar bugs
- Testar novas funcionalidades
- Criar casos de teste
- Melhorar cobertura de testes

### 🎨 **Design**
- Melhorar interface do usuário
- Criar ícones e assets
- Sugerir melhorias de UX
- Criar mockups

---

## 🏗️ Configuração do Ambiente

### 📋 **Pré-requisitos**

- 🐍 **Python 3.8+** (recomendado 3.9+)
- 🔧 **Git** para controle de versão
- 📝 **Editor de código** (VS Code, PyCharm, etc.)

### ⚡ **Configuração Rápida**

```bash
# 1️⃣ Fork o repositório no GitHub
# Clique em "Fork" na página do projeto

# 2️⃣ Clone seu fork
git clone https://github.com/SEU-USUARIO/ultra-texto-pro.git
cd ultra-texto-pro/ultra-texto

# 3️⃣ Configure o repositório upstream
git remote add upstream https://github.com/USUARIO-ORIGINAL/ultra-texto-pro.git

# 4️⃣ Crie um ambiente virtual
python -m venv .venv

# 5️⃣ Ative o ambiente virtual
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 6️⃣ Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# 7️⃣ Execute os testes para verificar se tudo está funcionando
python -m pytest tests/
```

### 🔧 **Dependências de Desenvolvimento**

Crie um arquivo `requirements-dev.txt`:

```txt
# Testes
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Qualidade de código
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0

# Documentação
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0

# Utilitários
pre-commit>=3.0.0
tox>=4.0.0
```

### 🎣 **Configuração de Pre-commit Hooks**

```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
pre-commit install
```

Crie `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
```

---

## 📝 Padrões de Código

### 🐍 **Estilo Python**

Seguimos o **PEP 8** com algumas adaptações:

```python
# ✅ Bom
class FileProcessor:
    """Processa arquivos de acordo com as configurações."""
    
    def __init__(self, config: ConfigManager) -> None:
        self.config = config
        self._processed_files: List[FileInfo] = []
    
    def process_file(self, file_path: Path) -> Optional[FileInfo]:
        """Processa um arquivo individual."""
        try:
            return self._do_process_file(file_path)
        except Exception as e:
            logger.error(f"Erro ao processar {file_path}: {e}")
            return None

# ❌ Ruim
class fileprocessor:
    def __init__(self,config):
        self.config=config
        self.processed_files=[]
    
    def processFile(self,filePath):
        return self.doProcessFile(filePath)
```

### 📏 **Convenções de Nomenclatura**

| Tipo | Convenção | Exemplo |
|---|---|---|
| **Classes** | PascalCase | `FileProcessor`, `ConfigManager` |
| **Funções/Métodos** | snake_case | `process_file()`, `get_config()` |
| **Variáveis** | snake_case | `file_path`, `processed_count` |
| **Constantes** | UPPER_SNAKE_CASE | `MAX_FILE_SIZE`, `DEFAULT_ENCODING` |
| **Módulos** | snake_case | `file_processor.py`, `config_manager.py` |

### 🏗️ **Estrutura de Arquivos**

```python
"""
Módulo para processamento de arquivos.

Este módulo contém classes e funções para processar diferentes
tipos de arquivo de acordo com as configurações do usuário.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

from core.interfaces import IFileProcessor
from core.exceptions import FileProcessingError
from utils.file_utils import is_text_file

logger = logging.getLogger(__name__)


class FileProcessor(IFileProcessor):
    """Implementação do processador de arquivos."""
    
    def __init__(self, config: 'ConfigManager') -> None:
        """
        Inicializa o processador de arquivos.
        
        Args:
            config: Gerenciador de configurações
        """
        self.config = config
        self._stats = ProcessingStats()
    
    # Resto da implementação...
```

### 🔍 **Type Hints**

Use type hints em todas as funções e métodos:

```python
from typing import List, Dict, Optional, Union, Callable
from pathlib import Path

def process_directory(
    directory: Path,
    extensions: List[str],
    progress_callback: Optional[Callable[[int], None]] = None
) -> Dict[str, Any]:
    """Processa um diretório e retorna estatísticas."""
    pass
```

---

## 🧪 Testes

### 🎯 **Filosofia de Testes**

- **Cobertura mínima**: 80%
- **Testes unitários** para lógica de negócio
- **Testes de integração** para fluxos completos
- **Testes de interface** para componentes UI

### 📁 **Estrutura de Testes**

```
tests/
├── unit/                    # Testes unitários
│   ├── test_file_processor.py
│   ├── test_config_manager.py
│   └── test_exclusion_manager.py
├── integration/             # Testes de integração
│   ├── test_full_workflow.py
│   └── test_export_pipeline.py
├── ui/                      # Testes de interface
│   ├── test_main_window.py
│   └── test_components.py
├── fixtures/                # Dados de teste
│   ├── sample_files/
│   └── test_configs/
└── conftest.py             # Configurações pytest
```

### ✍️ **Escrevendo Testes**

```python
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from modules.file_processor import FileProcessor
from modules.config_manager import ConfigManager


class TestFileProcessor:
    """Testes para o processador de arquivos."""
    
    @pytest.fixture
    def config_manager(self):
        """Fixture para o gerenciador de configurações."""
        config = ConfigManager()
        config.load_default_config()
        return config
    
    @pytest.fixture
    def file_processor(self, config_manager):
        """Fixture para o processador de arquivos."""
        return FileProcessor(config_manager)
    
    def test_process_python_file(self, file_processor, tmp_path):
        """Testa processamento de arquivo Python."""
        # Arrange
        test_file = tmp_path / "test.py"
        test_file.write_text("print('Hello, World!')")
        
        # Act
        result = file_processor.process_file(test_file)
        
        # Assert
        assert result is not None
        assert result.extension == ".py"
        assert "Hello, World!" in result.content
    
    def test_process_nonexistent_file(self, file_processor):
        """Testa processamento de arquivo inexistente."""
        # Arrange
        nonexistent_file = Path("does_not_exist.py")
        
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            file_processor.process_file(nonexistent_file)
    
    @patch('modules.file_processor.logger')
    def test_process_file_with_error(self, mock_logger, file_processor):
        """Testa tratamento de erro durante processamento."""
        # Arrange
        with patch.object(file_processor, '_read_file_content', 
                         side_effect=Exception("Test error")):
            test_file = Path("test.py")
            
            # Act
            result = file_processor.process_file(test_file)
            
            # Assert
            assert result is None
            mock_logger.error.assert_called_once()
```

### 🏃 **Executando Testes**

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/unit/test_file_processor.py

# Com cobertura
pytest --cov=modules --cov-report=html

# Testes em modo verbose
pytest -v

# Testes com saída detalhada
pytest -s

# Executar apenas testes que falharam na última execução
pytest --lf
```

---

## 📖 Documentação

### 📝 **Docstrings**

Use o formato **Google Style**:

```python
def process_directory(
    directory: Path,
    include_subdirs: bool = True,
    progress_callback: Optional[Callable[[int], None]] = None
) -> ProcessingResult:
    """
    Processa todos os arquivos em um diretório.
    
    Args:
        directory: Caminho para o diretório a ser processado
        include_subdirs: Se deve incluir subdiretórios
        progress_callback: Função chamada para reportar progresso (0-100)
    
    Returns:
        Resultado do processamento com estatísticas e arquivos processados
    
    Raises:
        DirectoryNotFoundError: Se o diretório não existir
        PermissionError: Se não houver permissão para acessar o diretório
    
    Example:
        >>> processor = FileProcessor(config)
        >>> result = processor.process_directory(Path("./src"))
        >>> print(f"Processados {result.file_count} arquivos")
    """
    pass
```

### 📚 **Documentação de Módulos**

```python
"""
Módulo de processamento de arquivos.

Este módulo fornece funcionalidades para processar diferentes tipos
de arquivo, extrair conteúdo e gerar estatísticas.

Classes:
    FileProcessor: Processador principal de arquivos
    FileInfo: Informações sobre um arquivo processado
    ProcessingStats: Estatísticas de processamento

Funções:
    is_supported_file: Verifica se um arquivo é suportado
    get_file_encoding: Detecta a codificação de um arquivo

Example:
    >>> from modules.file_processor import FileProcessor
    >>> processor = FileProcessor(config_manager)
    >>> result = processor.process_directory(Path("./src"))
"""
```

---

## 🐛 Reportando Bugs

### 📝 **Template de Bug Report**

Ao reportar um bug, use o seguinte template:

```markdown
## 🐛 Descrição do Bug
Uma descrição clara e concisa do bug.

## 🔄 Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role para baixo até '...'
4. Veja o erro

## ✅ Comportamento Esperado
Uma descrição clara do que você esperava que acontecesse.

## ❌ Comportamento Atual
Uma descrição clara do que realmente aconteceu.

## 📸 Screenshots
Se aplicável, adicione screenshots para ajudar a explicar o problema.

## 💻 Ambiente
- OS: [ex: Windows 10]
- Python: [ex: 3.9.7]
- Versão do UltraTexto Pro: [ex: 2.0.0]

## 📋 Informações Adicionais
Qualquer outra informação sobre o problema.

## 🔍 Logs
```
Cole aqui os logs relevantes
```
```

### 🔍 **Coletando Informações de Debug**

```python
# Para coletar informações de debug, execute:
from utils.logging_utils import create_debug_report

debug_info = create_debug_report()
print(debug_info)
```

---

## 💡 Sugerindo Melhorias

### 📝 **Template de Feature Request**

```markdown
## 🎯 Resumo da Funcionalidade
Uma descrição clara e concisa da funcionalidade desejada.

## 🤔 Problema que Resolve
Qual problema esta funcionalidade resolveria?

## 💡 Solução Proposta
Uma descrição clara da solução que você gostaria de ver.

## 🔄 Alternativas Consideradas
Outras soluções que você considerou.

## 📊 Casos de Uso
- Caso de uso 1: ...
- Caso de uso 2: ...

## 🎨 Mockups/Exemplos
Se aplicável, adicione mockups ou exemplos.

## 📈 Impacto
Como esta funcionalidade beneficiaria os usuários?

## 🔧 Implementação
Ideias sobre como implementar (opcional).
```

---

## 🔄 Processo de Pull Request

### 📋 **Checklist Antes do PR**

- [ ] ✅ Código segue os padrões estabelecidos
- [ ] 🧪 Testes foram adicionados/atualizados
- [ ] 📝 Documentação foi atualizada
- [ ] 🔍 Código foi revisado por você mesmo
- [ ] ⚡ Testes passam localmente
- [ ] 📊 Cobertura de testes mantida/melhorada

### 🏷️ **Convenções de Commit**

Use **Conventional Commits**:

```bash
# Tipos de commit
feat: nova funcionalidade
fix: correção de bug
docs: mudanças na documentação
style: formatação, ponto e vírgula, etc
refactor: refatoração de código
test: adição ou correção de testes
chore: mudanças em ferramentas, configurações, etc

# Exemplos
git commit -m "feat: adicionar suporte a arquivos .tsx"
git commit -m "fix: corrigir erro de encoding em arquivos grandes"
git commit -m "docs: atualizar guia de instalação"
git commit -m "test: adicionar testes para ExclusionManager"
```

### 📝 **Template de Pull Request**

```markdown
## 📋 Descrição
Breve descrição das mudanças realizadas.

## 🎯 Tipo de Mudança
- [ ] 🐛 Bug fix (mudança que corrige um problema)
- [ ] ✨ Nova funcionalidade (mudança que adiciona funcionalidade)
- [ ] 💥 Breaking change (mudança que quebra compatibilidade)
- [ ] 📝 Documentação (mudança apenas na documentação)

## 🧪 Como Foi Testado?
Descreva os testes realizados para verificar suas mudanças.

## 📋 Checklist
- [ ] Meu código segue os padrões do projeto
- [ ] Realizei uma auto-revisão do código
- [ ] Comentei partes complexas do código
- [ ] Atualizei a documentação correspondente
- [ ] Minhas mudanças não geram novos warnings
- [ ] Adicionei testes que provam que minha correção/funcionalidade funciona
- [ ] Testes novos e existentes passam localmente

## 📸 Screenshots (se aplicável)
Adicione screenshots das mudanças visuais.

## 🔗 Issues Relacionadas
Fixes #123
Closes #456
```

### 🔄 **Fluxo de Trabalho**

```bash
# 1️⃣ Sincronize com upstream
git checkout main
git pull upstream main

# 2️⃣ Crie uma branch para sua feature
git checkout -b feature/nome-da-feature

# 3️⃣ Faça suas mudanças e commits
git add .
git commit -m "feat: adicionar nova funcionalidade"

# 4️⃣ Execute testes
pytest

# 5️⃣ Push para seu fork
git push origin feature/nome-da-feature

# 6️⃣ Abra um Pull Request no GitHub
```

---

## 👥 Comunidade

### 💬 **Canais de Comunicação**

- 🐛 **Issues**: Para bugs e feature requests
- 💬 **Discussions**: Para perguntas e discussões gerais
- 📧 **Email**: contato@ultratexto.com

### 🎯 **Código de Conduta**

Seguimos o [Contributor Covenant](https://www.contributor-covenant.org/):

- **Seja respeitoso** com outros contribuidores
- **Seja inclusivo** e acolhedor
- **Seja construtivo** em feedback e críticas
- **Seja paciente** com iniciantes

### 🏆 **Reconhecimento**

Contribuidores são reconhecidos:

- 📝 **README**: Lista de contribuidores
- 🎉 **Releases**: Menção em notas de lançamento
- 🏅 **Badges**: Badges especiais para grandes contribuições

---

## 🚀 Primeiros Passos

### 🎯 **Issues para Iniciantes**

Procure por issues marcadas com:
- `good first issue` - Bom para iniciantes
- `help wanted` - Ajuda necessária
- `documentation` - Melhorias na documentação

### 📚 **Recursos Úteis**

- 📖 [Documentação do Python](https://docs.python.org/3/)
- 🧪 [Pytest Documentation](https://docs.pytest.org/)
- 🎨 [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- 🔧 [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

<div align="center">

## 🙏 Obrigado por Contribuir!

**Sua contribuição faz a diferença!**

[![Contributors](https://contrib.rocks/image?repo=seu-usuario/ultra-texto-pro)](https://github.com/seu-usuario/ultra-texto-pro/graphs/contributors)

---

**UltraTexto Pro** - *Construído pela comunidade, para a comunidade*

[⬆️ Voltar ao topo](#-guia-de-contribuição---ultratexto-pro)

</div>