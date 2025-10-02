"""
UltraTexto Pro - Ferramenta Avançada de Processamento de Arquivos
Versão 2.0 - Versão Completa Integrada
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import sys
import threading
import time
from pathlib import Path
from datetime import datetime

# Adicionar o diretório atual ao path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Imports dos módulos
from themes.dark_theme import DarkTheme
from modules.ui_components import (
    ProgressDialog, NotificationManager, FileTreeView, 
    SearchBox, StatusBar
)
from modules.exclusion_manager import ExclusionManager, ExclusionRule
from modules.file_processor import FileProcessor
from modules.directory_scanner import DirectoryScanner
from modules.export_manager import ExportManager
from modules.config_manager import ConfigManager

class UltraTextoPro:
    """Classe principal da aplicação UltraTexto Pro - Versão Completa"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_theme()
        
        # Inicializar gerenciadores
        self.config_manager = ConfigManager()
        self.exclusion_manager = ExclusionManager()
        self.export_manager = ExportManager()
        
        # Configurar variáveis
        self.setup_variables()
        self.setup_ui()
        self.setup_notifications()
        
        # Dados da aplicação
        self.current_directory = None
        self.current_directory_tree = None
        self.last_processing_stats = None
        
        # Carregar configurações
        self.load_settings()
        
        # Aplicar exclusões automáticas baseadas na configuração
        self.exclusion_manager.apply_auto_exclusions(self.config_manager)
        
        # Atualizar resumo das exclusões na interface
        self.root.after(100, self.update_exclusions_summary)
    
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("UltraTexto Pro - Processador Avançado de Arquivos v2.0")
        
        # Carregar tamanho da janela das configurações
        window_size = self.config_manager.get("ui.window_size", [1200, 800]) if hasattr(self, 'config_manager') else [1200, 800]
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.root.minsize(1000, 600)
        
        # Centralizar na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (window_size[0] // 2)
        y = (self.root.winfo_screenheight() // 2) - (window_size[1] // 2)
        self.root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")
        
        # Protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_theme(self):
        """Aplica o tema escuro"""
        self.style = DarkTheme.apply_theme(self.root)
    
    def setup_variables(self):
        """Inicializa as variáveis da aplicação"""
        self.selected_directory = tk.StringVar()
        self.include_subdirectories = tk.BooleanVar(value=True)
        self.include_files_in_structure = tk.BooleanVar(value=True)
        self.processing_mode = tk.StringVar(value="content")
        
        # Configurações de saída
        self.auto_open_results = tk.BooleanVar(value=True)
        self.create_backup = tk.BooleanVar(value=False)
        self.compress_output = tk.BooleanVar(value=False)
    
    def setup_notifications(self):
        """Configura o sistema de notificações"""
        self.notifications = NotificationManager(self.root)
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = DarkTheme.create_title_label(title_frame, "UltraTexto Pro")
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = DarkTheme.create_subtitle_label(
            title_frame, "Processador Avançado de Arquivos v2.0"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Menu superior
        self.create_menu_bar(title_frame)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Criar abas
        self.create_main_tab()
        self.create_exclusions_tab()
        self.create_results_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
        # Barra de status
        self.status_bar = StatusBar(main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_menu_bar(self, parent):
        """Cria barra de menu superior"""
        menu_frame = ttk.Frame(parent, style='Dark.TFrame')
        menu_frame.pack(side=tk.RIGHT)
        
        # Botões de menu
        recent_button = ttk.Button(menu_frame, text="📁 Recentes", 
                                  style='Dark.TButton', command=self.show_recent_directories)
        recent_button.pack(side=tk.LEFT, padx=(0, 5))
        
        help_button = ttk.Button(menu_frame, text="❓ Ajuda", 
                                style='Dark.TButton', command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=(0, 5))
        
        about_button = ttk.Button(menu_frame, text="ℹ Sobre", 
                                 style='Dark.TButton', command=self.show_about)
        about_button.pack(side=tk.LEFT)
    
    def create_main_tab(self):
        """Cria a aba principal"""
        main_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(main_tab, text="  🏠 Principal  ")
        
        # Frame de seleção de diretório
        dir_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        dir_label = ttk.Label(dir_frame, text="Diretório Selecionado:", style='Dark.TLabel')
        dir_label.pack(anchor='w', pady=(0, 5))
        
        dir_input_frame = ttk.Frame(dir_frame, style='Dark.TFrame')
        dir_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_input_frame, textvariable=self.selected_directory, 
                                  style='Dark.TEntry', font=('Segoe UI', 10))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(dir_input_frame, text="📂 Procurar", 
                                  style='Accent.TButton', command=self.browse_directory)
        browse_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        recent_button = ttk.Button(dir_input_frame, text="📋 Recentes", 
                                  style='Dark.TButton', command=self.show_recent_directories)
        recent_button.pack(side=tk.RIGHT)
        
        # Extensões suportadas
        ext_label = ttk.Label(dir_frame, 
                             text=f"Extensões suportadas: {', '.join(sorted(self.get_supported_extensions()))}", 
                             style='Subtitle.TLabel', wraplength=800)
        ext_label.pack(anchor='w')
        
        # Frame de opções
        options_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        options_label = ttk.Label(options_frame, text="Opções de Processamento:", style='Dark.TLabel')
        options_label.pack(anchor='w', pady=(0, 10))
        
        # Checkboxes
        checkbox_frame = ttk.Frame(options_frame, style='Dark.TFrame')
        checkbox_frame.pack(fill=tk.X)
        
        subdir_check = ttk.Checkbutton(checkbox_frame, text="Incluir subdiretórios", 
                                      variable=self.include_subdirectories, style='Dark.TCheckbutton')
        subdir_check.pack(side=tk.LEFT, padx=(0, 20))
        
        files_check = ttk.Checkbutton(checkbox_frame, text="Incluir arquivos na estrutura", 
                                     variable=self.include_files_in_structure, style='Dark.TCheckbutton')
        files_check.pack(side=tk.LEFT)
        
        # Frame de modo de processamento
        mode_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        mode_label = ttk.Label(mode_frame, text="Modo de Processamento:", style='Dark.TLabel')
        mode_label.pack(anchor='w', pady=(0, 10))
        
        radio_frame = ttk.Frame(mode_frame, style='Dark.TFrame')
        radio_frame.pack(fill=tk.X)
        
        content_radio = ttk.Radiobutton(radio_frame, text="📄 Extrair conteúdo dos arquivos", 
                                       variable=self.processing_mode, value="content", 
                                       style='Dark.TRadiobutton')
        content_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        structure_radio = ttk.Radiobutton(radio_frame, text="🌳 Gerar estrutura de diretórios", 
                                         variable=self.processing_mode, value="structure", 
                                         style='Dark.TRadiobutton')
        structure_radio.pack(side=tk.LEFT)
        
        # Frame de ações
        actions_frame = ttk.Frame(main_tab, style='Dark.TFrame')
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botões principais
        process_button = ttk.Button(actions_frame, text="🚀 Processar", 
                                   style='Accent.TButton', command=self.start_processing)
        process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        preview_button = ttk.Button(actions_frame, text="👁 Preview", 
                                   style='Dark.TButton', command=self.preview_processing)
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clone_button = ttk.Button(actions_frame, text="📋 Clonar Pasta (com exclusões)",
                                 style='Dark.TButton', command=self.clone_directory_action)
        clone_button.pack(side=tk.LEFT, padx=(0, 10))
        
        scan_button = ttk.Button(actions_frame, text="🔍 Escanear", 
                                style='Dark.TButton', command=self.scan_directory)
        scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(actions_frame, text="🗑 Limpar", 
                                 style='Dark.TButton', command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        # Informações do diretório
        info_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_label = ttk.Label(info_frame, text="Informações do Diretório:", style='Dark.TLabel')
        info_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para preview
        self.preview_tree = FileTreeView(info_frame, height=10)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_exclusions_tab(self):
        """Cria a aba de exclusões avançadas"""
        exclusions_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(exclusions_tab, text="  🚫 Exclusões  ")
        
        # Frame de resumo das exclusões
        summary_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        summary_label = ttk.Label(summary_frame, text="📊 Resumo das Exclusões Ativas:", style='Dark.TLabel')
        summary_label.pack(anchor='w', pady=(0, 10))
        
        # Frame para informações do resumo
        summary_info_frame = ttk.Frame(summary_frame, style='Dark.TFrame')
        summary_info_frame.pack(fill=tk.X)
        
        # Labels para mostrar informações
        self.profile_info_label = ttk.Label(summary_info_frame, text="Perfil: Padrão", style='Dark.TLabel')
        self.profile_info_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.rules_info_label = ttk.Label(summary_info_frame, text="Regras: 0 ativas", style='Dark.TLabel')
        self.rules_info_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.common_exclusions_label = ttk.Label(summary_info_frame, text="Pastas excluídas: node_modules, .venv, venv...", style='Dark.TLabel')
        self.common_exclusions_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botão para atualizar resumo
        refresh_summary_button = ttk.Button(summary_info_frame, text="🔄 Atualizar", 
                                          style='Dark.TButton', command=self.update_exclusions_summary)
        refresh_summary_button.pack(side=tk.RIGHT)
        
        # Frame de perfis
        profiles_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        profiles_frame.pack(fill=tk.X, pady=(0, 15))
        
        profiles_label = ttk.Label(profiles_frame, text="Perfis de Exclusão:", style='Dark.TLabel')
        profiles_label.pack(anchor='w', pady=(0, 10))
        
        profile_control_frame = ttk.Frame(profiles_frame, style='Dark.TFrame')
        profile_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Combobox de perfis
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_control_frame, textvariable=self.profile_var,
                                         style='Dark.TCombobox', state='readonly')
        self.profile_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_changed)
        
        # Botões de perfil
        new_profile_button = ttk.Button(profile_control_frame, text="➕ Novo", 
                                       style='Dark.TButton', command=self.create_new_profile)
        new_profile_button.pack(side=tk.LEFT, padx=(0, 5))
        
        save_profile_button = ttk.Button(profile_control_frame, text="💾 Salvar", 
                                        style='Dark.TButton', command=self.save_current_profile)
        save_profile_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_profile_button = ttk.Button(profile_control_frame, text="🗑 Excluir", 
                                          style='Dark.TButton', command=self.delete_current_profile)
        delete_profile_button.pack(side=tk.LEFT)
        
        # Frame de filtros
        filters_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        filters_frame.pack(fill=tk.X, pady=(0, 15))
        
        filters_label = ttk.Label(filters_frame, text="Adicionar Filtros:", style='Dark.TLabel')
        filters_label.pack(anchor='w', pady=(0, 10))
        
        # Botões de filtro
        filter_buttons_frame = ttk.Frame(filters_frame, style='Dark.TFrame')
        filter_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_file_button = ttk.Button(filter_buttons_frame, text="📄 Arquivo", 
                                    style='Dark.TButton', command=self.add_file_exclusion)
        add_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_folder_button = ttk.Button(filter_buttons_frame, text="📁 Pasta", 
                                      style='Dark.TButton', command=self.add_folder_exclusion)
        add_folder_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_extension_button = ttk.Button(filter_buttons_frame, text="🏷 Extensão", 
                                         style='Dark.TButton', command=self.add_extension_exclusion)
        add_extension_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_regex_button = ttk.Button(filter_buttons_frame, text="🔍 Regex", 
                                     style='Dark.TButton', command=self.add_regex_exclusion)
        add_regex_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_size_button = ttk.Button(filter_buttons_frame, text="📏 Tamanho", 
                                    style='Dark.TButton', command=self.add_size_exclusion)
        add_size_button.pack(side=tk.LEFT, padx=(0, 10))
        
        preview_button = ttk.Button(filter_buttons_frame, text="👁 Preview", 
                                   style='Accent.TButton', command=self.preview_exclusions)
        preview_button.pack(side=tk.RIGHT)
        
        # Lista de exclusões
        exclusions_list_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        exclusions_list_frame.pack(fill=tk.BOTH, expand=True)
        
        exclusions_label = ttk.Label(exclusions_list_frame, text="Regras de Exclusão:", style='Dark.TLabel')
        exclusions_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para exclusões
        self.exclusions_tree = FileTreeView(exclusions_list_frame, 
                                           columns=('type', 'pattern', 'enabled'), height=15)
        self.exclusions_tree.tree.heading('#0', text='Descrição')
        self.exclusions_tree.tree.heading('type', text='Tipo')
        self.exclusions_tree.tree.heading('pattern', text='Padrão')
        self.exclusions_tree.tree.heading('enabled', text='Ativo')

        # Configurar larguras das colunas
        self.exclusions_tree.tree.column('#0', width=250, minwidth=200)
        self.exclusions_tree.tree.column('type', width=100, minwidth=80)
        self.exclusions_tree.tree.column('pattern', width=200, minwidth=150)
        self.exclusions_tree.tree.column('enabled', width=80, minwidth=60)
                
        self.exclusions_tree.pack(fill=tk.BOTH, expand=True)
                
        # Bind para ações
        self.exclusions_tree.tree.bind('<Delete>', self.remove_selected_exclusion)
        self.exclusions_tree.tree.bind('<Double-1>', self.edit_exclusion)
        
        # Atualizar lista de perfis
        self.update_profiles_list()
    
    def create_results_tab(self):
        """Cria a aba de resultados"""
        results_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(results_tab, text="  📊 Resultados  ")
        
        # Busca
        search_frame = ttk.Frame(results_tab, style='Dark.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.search_box = SearchBox(search_frame, on_search=self.search_results, 
                                   on_clear=self.clear_search)
        self.search_box.pack(fill=tk.X)
        
        # Lista de arquivos gerados
        files_frame = DarkTheme.create_card_frame(results_tab, padding=15)
        files_frame.pack(fill=tk.BOTH, expand=True)
        
        files_label = ttk.Label(files_frame, text="Arquivos Gerados:", style='Dark.TLabel')
        files_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para arquivos
        self.results_tree = FileTreeView(files_frame, height=15)
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões de ação
        results_buttons_frame = ttk.Frame(files_frame, style='Dark.TFrame')
        results_buttons_frame.pack(fill=tk.X)
        
        open_button = ttk.Button(results_buttons_frame, text="📂 Abrir", 
                                style='Accent.TButton', command=self.open_selected_file)
        open_button.pack(side=tk.LEFT, padx=(0, 10))
        
        view_button = ttk.Button(results_buttons_frame, text="👁 Visualizar", 
                                style='Dark.TButton', command=self.view_selected_file)
        view_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_button = ttk.Button(results_buttons_frame, text="📤 Exportar", 
                                  style='Dark.TButton', command=self.export_results)
        export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_button = ttk.Button(results_buttons_frame, text="🗑 Excluir", 
                                  style='Dark.TButton', command=self.delete_selected_file)
        delete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        folder_button = ttk.Button(results_buttons_frame, text="📁 Pasta", 
                                  style='Dark.TButton', command=self.open_output_folder)
        folder_button.pack(side=tk.RIGHT)
        
        refresh_button = ttk.Button(results_buttons_frame, text="🔄 Atualizar", 
                                   style='Dark.TButton', command=self.refresh_results)
        refresh_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_analytics_tab(self):
        """Cria a aba de análises"""
        analytics_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analytics_tab, text="  📈 Análises  ")
        
        # Estatísticas gerais
        stats_frame = DarkTheme.create_card_frame(analytics_tab, padding=15)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        stats_label = ttk.Label(stats_frame, text="Estatísticas do Último Processamento:", style='Dark.TLabel')
        stats_label.pack(anchor='w', pady=(0, 10))
        
        # Grid de estatísticas
        self.stats_frame = ttk.Frame(stats_frame, style='Dark.TFrame')
        self.stats_frame.pack(fill=tk.X)
        
        # Análises avançadas
        analysis_frame = DarkTheme.create_card_frame(analytics_tab, padding=15)
        analysis_frame.pack(fill=tk.BOTH, expand=True)
        
        analysis_label = ttk.Label(analysis_frame, text="Análises Avançadas:", style='Dark.TLabel')
        analysis_label.pack(anchor='w', pady=(0, 10))
        
        # Botões de análise
        analysis_buttons_frame = ttk.Frame(analysis_frame, style='Dark.TFrame')
        analysis_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        largest_files_button = ttk.Button(analysis_buttons_frame, text="📊 Maiores Arquivos", 
                                         style='Dark.TButton', command=self.show_largest_files)
        largest_files_button.pack(side=tk.LEFT, padx=(0, 10))
        
        extension_dist_button = ttk.Button(analysis_buttons_frame, text="📈 Distribuição de Extensões", 
                                          style='Dark.TButton', command=self.show_extension_distribution)
        extension_dist_button.pack(side=tk.LEFT, padx=(0, 10))
        
        duplicates_button = ttk.Button(analysis_buttons_frame, text="🔍 Nomes Duplicados", 
                                      style='Dark.TButton', command=self.show_duplicate_names)
        duplicates_button.pack(side=tk.LEFT, padx=(0, 10))
        
        empty_dirs_button = ttk.Button(analysis_buttons_frame, text="📁 Pastas Vazias", 
                                      style='Dark.TButton', command=self.show_empty_directories)
        empty_dirs_button.pack(side=tk.LEFT)
        
        # Área de resultados de análise
        self.analysis_tree = FileTreeView(analysis_frame, height=15)
        self.analysis_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_settings_tab(self):
        """Cria a aba de configurações"""
        settings_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(settings_tab, text="  ⚙ Configurações  ")
        
        # Notebook interno para configurações
        settings_notebook = ttk.Notebook(settings_tab, style='Dark.TNotebook')
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de processamento
        processing_tab = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(processing_tab, text="Processamento")
        
        self.create_processing_settings(processing_tab)
        
        # Aba de interface
        ui_tab = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(ui_tab, text="Interface")
        
        self.create_ui_settings(ui_tab)
        
        # Aba de saída
        output_tab = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(output_tab, text="Saída")
        
        self.create_output_settings(output_tab)
        
        # Aba avançada
        advanced_tab = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(advanced_tab, text="Avançado")
        
        self.create_advanced_settings(advanced_tab)
    
    def create_processing_settings(self, parent):
        """Cria configurações de processamento"""
        # Extensões
        ext_frame = DarkTheme.create_card_frame(parent, padding=15)
        ext_frame.pack(fill=tk.X, pady=(0, 15))
        
        ext_label = ttk.Label(ext_frame, text="Extensões Suportadas:", style='Dark.TLabel')
        ext_label.pack(anchor='w', pady=(0, 10))
        
        ext_list_frame = ttk.Frame(ext_frame, style='Dark.TFrame')
        ext_list_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.extensions_var = tk.StringVar()
        ext_entry = ttk.Entry(ext_list_frame, textvariable=self.extensions_var, 
                             style='Dark.TEntry', font=('Segoe UI', 10))
        ext_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        update_ext_button = ttk.Button(ext_list_frame, text="Atualizar", 
                                      style='Accent.TButton', command=self.update_extensions)
        update_ext_button.pack(side=tk.RIGHT)
        
        # Configurações de performance
        perf_frame = DarkTheme.create_card_frame(parent, padding=15)
        perf_frame.pack(fill=tk.X, pady=(0, 15))
        
        perf_label = ttk.Label(perf_frame, text="Performance:", style='Dark.TLabel')
        perf_label.pack(anchor='w', pady=(0, 10))
        
        # Max workers
        workers_frame = ttk.Frame(perf_frame, style='Dark.TFrame')
        workers_frame.pack(fill=tk.X, pady=(0, 5))
        
        workers_label = ttk.Label(workers_frame, text="Threads de processamento:", style='Dark.TLabel')
        workers_label.pack(side=tk.LEFT)
        
        self.max_workers_var = tk.IntVar()
        workers_spinbox = ttk.Spinbox(workers_frame, from_=1, to=16, textvariable=self.max_workers_var,
                                     style='Dark.TEntry', width=10)
        workers_spinbox.pack(side=tk.RIGHT)
        
        # Max file size
        size_frame = ttk.Frame(perf_frame, style='Dark.TFrame')
        size_frame.pack(fill=tk.X, pady=(0, 5))
        
        size_label = ttk.Label(size_frame, text="Tamanho máximo de arquivo (MB):", style='Dark.TLabel')
        size_label.pack(side=tk.LEFT)
        
        self.max_file_size_var = tk.IntVar()
        size_spinbox = ttk.Spinbox(size_frame, from_=1, to=1000, textvariable=self.max_file_size_var,
                                  style='Dark.TEntry', width=10)
        size_spinbox.pack(side=tk.RIGHT)
    
    def create_ui_settings(self, parent):
        """Cria configurações de interface"""
        # Aparência
        appearance_frame = DarkTheme.create_card_frame(parent, padding=15)
        appearance_frame.pack(fill=tk.X, pady=(0, 15))
        
        appearance_label = ttk.Label(appearance_frame, text="Aparência:", style='Dark.TLabel')
        appearance_label.pack(anchor='w', pady=(0, 10))
        
        # Checkboxes de interface
        self.show_tooltips_var = tk.BooleanVar()
        tooltips_check = ttk.Checkbutton(appearance_frame, text="Mostrar tooltips", 
                                        variable=self.show_tooltips_var, style='Dark.TCheckbutton')
        tooltips_check.pack(anchor='w', pady=2)
        
        self.animation_enabled_var = tk.BooleanVar()
        animation_check = ttk.Checkbutton(appearance_frame, text="Habilitar animações", 
                                         variable=self.animation_enabled_var, style='Dark.TCheckbutton')
        animation_check.pack(anchor='w', pady=2)
        
        self.auto_save_layout_var = tk.BooleanVar()
        layout_check = ttk.Checkbutton(appearance_frame, text="Salvar layout automaticamente", 
                                      variable=self.auto_save_layout_var, style='Dark.TCheckbutton')
        layout_check.pack(anchor='w', pady=2)
    
    def create_output_settings(self, parent):
        """Cria configurações de saída"""
        # Configurações de saída
        output_frame = DarkTheme.create_card_frame(parent, padding=15)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_label = ttk.Label(output_frame, text="Configurações de Saída:", style='Dark.TLabel')
        output_label.pack(anchor='w', pady=(0, 10))
        
        # Diretório de saída
        dir_frame = ttk.Frame(output_frame, style='Dark.TFrame')
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        dir_label = ttk.Label(dir_frame, text="Diretório de saída:", style='Dark.TLabel')
        dir_label.pack(anchor='w', pady=(0, 5))
        
        dir_input_frame = ttk.Frame(dir_frame, style='Dark.TFrame')
        dir_input_frame.pack(fill=tk.X)
        
        self.output_dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_input_frame, textvariable=self.output_dir_var, 
                             style='Dark.TEntry')
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_output_button = ttk.Button(dir_input_frame, text="Procurar", 
                                         style='Dark.TButton', command=self.browse_output_directory)
        browse_output_button.pack(side=tk.RIGHT)
        
        # Opções de saída
        auto_open_check = ttk.Checkbutton(output_frame, text="Abrir resultados automaticamente", 
                                         variable=self.auto_open_results, style='Dark.TCheckbutton')
        auto_open_check.pack(anchor='w', pady=2)
        
        backup_check = ttk.Checkbutton(output_frame, text="Criar backup dos arquivos existentes", 
                                      variable=self.create_backup, style='Dark.TCheckbutton')
        backup_check.pack(anchor='w', pady=2)
        
        compress_check = ttk.Checkbutton(output_frame, text="Comprimir arquivos de saída", 
                                        variable=self.compress_output, style='Dark.TCheckbutton')
        compress_check.pack(anchor='w', pady=2)
    
    def create_advanced_settings(self, parent):
        """Cria configurações avançadas"""
        # Configurações avançadas
        advanced_frame = DarkTheme.create_card_frame(parent, padding=15)
        advanced_frame.pack(fill=tk.X, pady=(0, 15))
        
        advanced_label = ttk.Label(advanced_frame, text="Configurações Avançadas:", style='Dark.TLabel')
        advanced_label.pack(anchor='w', pady=(0, 10))
        
        # Botões de ação
        buttons_frame = ttk.Frame(advanced_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        export_config_button = ttk.Button(buttons_frame, text="📤 Exportar Configurações", 
                                         style='Dark.TButton', command=self.export_config)
        export_config_button.pack(side=tk.LEFT, padx=(0, 10))
        
        import_config_button = ttk.Button(buttons_frame, text="📥 Importar Configurações", 
                                         style='Dark.TButton', command=self.import_config)
        import_config_button.pack(side=tk.LEFT, padx=(0, 10))
        
        reset_button = ttk.Button(buttons_frame, text="🔄 Restaurar Padrões", 
                                 style='Dark.TButton', command=self.reset_to_defaults)
        reset_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cleanup_button = ttk.Button(buttons_frame, text="🧹 Limpar Cache", 
                                   style='Dark.TButton', command=self.cleanup_cache)
        cleanup_button.pack(side=tk.RIGHT)
        
        # Informações do sistema
        info_frame = DarkTheme.create_card_frame(parent, padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_label = ttk.Label(info_frame, text="Informações do Sistema:", style='Dark.TLabel')
        info_label.pack(anchor='w', pady=(0, 10))
        
        # Texto de informações
        info_text = f"""UltraTexto Pro v2.0

Desenvolvido com Python e tkinter
Tema escuro moderno integrado

Funcionalidades:
• Processamento avançado de arquivos
• Sistema de exclusões com perfis
• Exportação em múltiplos formatos
• Análises estatísticas detalhadas
• Interface moderna e intuitiva

Configurações salvas em: {self.config_manager.config_dir}
Diretório de saída: {self.config_manager.get_output_directory()}"""
        
        info_content = ttk.Label(info_frame, text=info_text, style='Subtitle.TLabel', 
                                justify=tk.LEFT, wraplength=800)
        info_content.pack(anchor='w')
    
    # Métodos de funcionalidade principal
    def load_settings(self):
        """Carrega configurações salvas"""
        # Carregar extensões suportadas
        extensions = self.config_manager.get_supported_extensions()
        self.extensions_var.set(' '.join(extensions))
        
        # Carregar outras configurações
        self.include_subdirectories.set(self.config_manager.get("processing.include_subdirectories", True))
        self.include_files_in_structure.set(self.config_manager.get("processing.include_files_in_structure", True))
        self.processing_mode.set(self.config_manager.get("processing.processing_mode", "content"))
        
        # Configurações de saída
        self.auto_open_results.set(self.config_manager.get("output.auto_open_results", True))
        self.create_backup.set(self.config_manager.get("output.create_backup", False))
        self.compress_output.set(self.config_manager.get("output.compress_output", False))
        self.output_dir_var.set(str(self.config_manager.get_output_directory()))
        
        # Configurações de performance
        self.max_workers_var.set(self.config_manager.get("processing.max_workers", 4))
        self.max_file_size_var.set(self.config_manager.get("processing.max_file_size_mb", 10))
        
        # Configurações de interface
        self.show_tooltips_var.set(self.config_manager.get("ui.show_tooltips", True))
        self.animation_enabled_var.set(self.config_manager.get("ui.animation_enabled", True))
        self.auto_save_layout_var.set(self.config_manager.get("ui.auto_save_layout", True))
        
        # Carregar último diretório se configurado
        if self.config_manager.get("history.auto_load_last_directory", False):
            recent_dirs = self.config_manager.get_recent_directories()
            if recent_dirs:
                self.selected_directory.set(recent_dirs[0])
                self.current_directory = recent_dirs[0]
    
    def save_settings(self):
        """Salva configurações atuais"""
        # Salvar extensões
        extensions_text = self.extensions_var.get()
        extensions = [ext.strip() for ext in extensions_text.split() if ext.strip()]
        self.config_manager.set_supported_extensions(extensions)
        
        # Salvar outras configurações
        self.config_manager.set("processing.include_subdirectories", self.include_subdirectories.get())
        self.config_manager.set("processing.include_files_in_structure", self.include_files_in_structure.get())
        self.config_manager.set("processing.processing_mode", self.processing_mode.get())
        
        # Configurações de saída
        self.config_manager.set("output.auto_open_results", self.auto_open_results.get())
        self.config_manager.set("output.create_backup", self.create_backup.get())
        self.config_manager.set("output.compress_output", self.compress_output.get())
        self.config_manager.set("output.output_directory", self.output_dir_var.get())
        
        # Configurações de performance
        self.config_manager.set("processing.max_workers", self.max_workers_var.get())
        self.config_manager.set("processing.max_file_size_mb", self.max_file_size_var.get())
        
        # Configurações de interface
        self.config_manager.set("ui.show_tooltips", self.show_tooltips_var.get())
        self.config_manager.set("ui.animation_enabled", self.animation_enabled_var.get())
        self.config_manager.set("ui.auto_save_layout", self.auto_save_layout_var.get())
        
        # Salvar tamanho da janela
        geometry = self.root.geometry()
        size_part = geometry.split('+')[0]
        width, height = map(int, size_part.split('x'))
        self.config_manager.set("ui.window_size", [width, height])
        
        self.config_manager.save_config()
    
    def get_supported_extensions(self):
        """Retorna extensões suportadas"""
        return self.config_manager.get_supported_extensions()
    
    def browse_directory(self):
        """Abre dialog para selecionar diretório"""
        initial_dir = self.current_directory or os.path.expanduser("~")
        directory = filedialog.askdirectory(title="Selecione o diretório para processar",
                                           initialdir=initial_dir)
        if directory:
            self.selected_directory.set(directory)
            self.current_directory = directory
            self.config_manager.add_recent_directory(directory)
            self.update_directory_info()
            self.status_bar.set_status(f"Diretório selecionado: {os.path.basename(directory)}")
    
    def browse_output_directory(self):
        """Abre dialog para selecionar diretório de saída"""
        directory = filedialog.askdirectory(title="Selecione o diretório de saída")
        if directory:
            self.output_dir_var.set(directory)
    
    def show_recent_directories(self):
        """Mostra lista de diretórios recentes"""
        recent_dirs = self.config_manager.get_recent_directories()
        if not recent_dirs:
            self.notifications.show_info("Nenhum diretório recente encontrado")
            return
        
        # Criar janela de seleção
        dialog = tk.Toplevel(self.root)
        dialog.title("Diretórios Recentes")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")
        
        # Lista de diretórios
        frame = ttk.Frame(dialog, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = ttk.Label(frame, text="Selecione um diretório recente:", style='Dark.TLabel')
        label.pack(anchor='w', pady=(0, 10))
        
        # Listbox
        listbox = tk.Listbox(frame, bg=DarkTheme.COLORS['bg_secondary'], 
                            fg=DarkTheme.COLORS['text_primary'],
                            selectbackground=DarkTheme.COLORS['bg_selected'],
                            font=('Segoe UI', 10))
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        for directory in recent_dirs:
            listbox.insert(tk.END, directory)
        
        # Botões
        buttons_frame = ttk.Frame(frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X)
        
        def select_directory():
            selection = listbox.curselection()
            if selection:
                selected_dir = recent_dirs[selection[0]]
                self.selected_directory.set(selected_dir)
                self.current_directory = selected_dir
                self.update_directory_info()
                dialog.destroy()
        
        select_button = ttk.Button(buttons_frame, text="Selecionar", 
                                  style='Accent.TButton', command=select_directory)
        select_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(buttons_frame, text="Cancelar", 
                                  style='Dark.TButton', command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT)
        
        # Bind duplo clique
        listbox.bind('<Double-1>', lambda e: select_directory())
    
    def update_directory_info(self):
        """Atualiza as informações do diretório selecionado"""
        if not self.current_directory:
            return
        
        # Limpar árvore
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        try:
            # Usar scanner para obter informações
            scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
            
            # Escanear apenas o primeiro nível para preview rápido
            root_node = scanner.scan_directory(self.current_directory, include_subdirectories=False)
            
            # Adicionar itens à árvore
            for child in root_node.children[:20]:  # Limitar a 20 itens
                icon = "📁" if child.is_directory else ("📄✅" if child.is_supported else "📄")
                if child.is_excluded:
                    icon += "❌"
                
                size_str = self._format_file_size(child.size) if not child.is_directory else ""
                item_type = "Pasta" if child.is_directory else "Arquivo"
                
                self.preview_tree.insert('', 'end', text=f"{icon} {child.name}", 
                                       values=(size_str, item_type, ''))
            
            if len(root_node.children) > 20:
                self.preview_tree.insert('', 'end', text="... (mais itens)", 
                                       values=('', '', ''))
            
            # Atualizar estatísticas
            stats = scanner.get_statistics()
            info_text = (f"Pastas: {stats['total_directories']} | "
                        f"Arquivos: {stats['total_files']} | "
                        f"Suportados: {len([c for c in root_node.children if not c.is_directory and c.is_supported])}")
            self.status_bar.set_info(info_text)
            
        except Exception as e:
            self.notifications.show_error(f"Erro ao analisar diretório: {str(e)}")
    
    def scan_directory(self):
        """Escaneia diretório completo"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        # Executar escaneamento em thread
        def scan_thread():
            progress = ProgressDialog(self.root, "Escaneando Diretório", 
                                     "Analisando estrutura completa...")
            
            try:
                scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
                scanner.set_progress_callback(lambda c, t, m: progress.update_status(m))
                
                self.current_directory_tree = scanner.scan_directory(
                    self.current_directory, 
                    self.include_subdirectories.get()
                )
                
                progress.close()
                self.root.after(0, lambda: self.notifications.show_success("Escaneamento concluído!"))
                self.root.after(0, self.update_scan_results)
                
            except Exception as e:
                progress.close()
                self.root.after(0, lambda: self.notifications.show_error(f"Erro no escaneamento: {str(e)}"))
        
        thread = threading.Thread(target=scan_thread, daemon=True)
        thread.start()
    
    def update_scan_results(self):
        """Atualiza resultados do escaneamento"""
        if not self.current_directory_tree:
            return
        
        # Limpar árvore
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        # Gerar texto da árvore
        scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
        tree_text = scanner.generate_tree_text(self.current_directory_tree, max_items=100)
        
        # Adicionar linhas à árvore
        for line in tree_text.split('\n')[:100]:
            if line.strip():
                self.preview_tree.insert('', 'end', text=line, values=('', '', ''))
    
    def start_processing(self):
        """Inicia o processamento em thread separada"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        # Salvar configurações antes de processar
        self.save_settings()
        
        # Iniciar processamento em thread
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()
    
    def process_files(self):
        """Processa os arquivos (executado em thread separada)"""
        progress = ProgressDialog(self.root, "Processando Arquivos", 
                                 "Preparando processamento...")
        
        try:
            # Criar processador
            processor = FileProcessor(set(self.get_supported_extensions()), self.exclusion_manager)
            processor.set_progress_callback(lambda c, t, m: progress.update_status(m))
            
            # Determinar nome do arquivo de saída
            if self.processing_mode.get() == "content":
                template = self.config_manager.get("output.filename_template", "arquivo_{counter}")
                output_path = self.config_manager.get_next_filename(template, ".txt")
            else:
                template = self.config_manager.get("output.structure_filename_template", "estrutura_{counter}")
                output_path = self.config_manager.get_next_filename(template, ".txt")
            
            progress.update_message("Processando arquivos...")
            
            # Processar baseado no modo
            if self.processing_mode.get() == "content":
                result_path = processor.process_files_content(
                    self.current_directory,
                    output_path,
                    self.include_subdirectories.get()
                )
            else:
                result_path = processor.generate_directory_structure(
                    self.current_directory,
                    output_path,
                    self.include_subdirectories.get(),
                    self.include_files_in_structure.get()
                )
            
            # Salvar estatísticas
            self.last_processing_stats = processor.stats
            
            # Adicionar ao histórico
            self.config_manager.add_processing_entry({
                "directory": self.current_directory,
                "mode": self.processing_mode.get(),
                "output_file": result_path,
                "stats": processor.stats.to_dict()
            })
            
            # Adicionar arquivo aos recentes
            self.config_manager.add_recent_file(result_path)
            
            progress.close()
            
            # Notificar sucesso
            self.root.after(0, lambda: self.notifications.show_success("Processamento concluído!"))
            self.root.after(0, self.refresh_results)
            self.root.after(0, self.update_statistics)
            
            # Abrir resultado se configurado
            if self.auto_open_results.get():
                self.root.after(0, lambda: self.open_file(result_path))
                
        except Exception as e:
            progress.close()
            self.root.after(0, lambda: self.notifications.show_error(f"Erro no processamento: {str(e)}"))
    
    def preview_processing(self):
        """Mostra preview do que será processado"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        # Executar preview em thread
        def preview_thread():
            try:
                preview_data = self.exclusion_manager.get_exclusion_preview(self.current_directory, max_items=500)
                self.root.after(0, lambda: self.show_preview_dialog(preview_data))
            except Exception as e:
                self.root.after(0, lambda: self.notifications.show_error(f"Erro no preview: {str(e)}"))
        
        thread = threading.Thread(target=preview_thread, daemon=True)
        thread.start()
    
    def show_preview_dialog(self, preview_data):
        """Mostra dialog com preview dos arquivos"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Preview do Processamento")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"800x600+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, style='Dark.TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Preview do Processamento", style='Title.TLabel')
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Estatísticas
        stats_text = (f"Total verificado: {preview_data['total_checked']} itens\n"
                     f"Serão incluídos: {len(preview_data['included'])} itens\n"
                     f"Serão excluídos: {len(preview_data['excluded'])} itens")
        
        stats_label = ttk.Label(main_frame, text=stats_text, style='Dark.TLabel')
        stats_label.pack(anchor='w', pady=(0, 10))
        
        # Notebook para incluídos/excluídos
        notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Aba de incluídos
        included_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(included_frame, text=f"Incluídos ({len(preview_data['included'])})")
        
        included_text = tk.Text(included_frame, bg=DarkTheme.COLORS['bg_secondary'],
                               fg=DarkTheme.COLORS['text_primary'], font=('Courier New', 9))
        included_text.pack(fill=tk.BOTH, expand=True)
        included_text.insert('1.0', '\n'.join(preview_data['included']))
        included_text.config(state='disabled')
        
        # Aba de excluídos
        excluded_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(excluded_frame, text=f"Excluídos ({len(preview_data['excluded'])})")
        
        excluded_text = tk.Text(excluded_frame, bg=DarkTheme.COLORS['bg_secondary'],
                               fg=DarkTheme.COLORS['text_primary'], font=('Courier New', 9))
        excluded_text.pack(fill=tk.BOTH, expand=True)
        excluded_text.insert('1.0', '\n'.join(preview_data['excluded']))
        excluded_text.config(state='disabled')
        
        # Botão fechar
        close_button = ttk.Button(main_frame, text="Fechar", 
                                 style='Accent.TButton', command=dialog.destroy)
        close_button.pack()
    
    def clear_all(self):
        """Limpa todas as configurações"""
        self.selected_directory.set("")
        self.current_directory = None
        self.current_directory_tree = None
        
        # Limpar árvores
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        self.status_bar.clear()
        self.notifications.show_info("Configurações limpas")
    
    # Métodos de exclusões
    def update_profiles_list(self):
        """Atualiza lista de perfis de exclusão"""
        profiles = list(self.exclusion_manager.profiles.keys())
        self.profile_combo['values'] = profiles
        
        if self.exclusion_manager.current_profile:
            self.profile_var.set(self.exclusion_manager.current_profile.name)
        
        self.update_exclusions_tree()
    
    def on_profile_changed(self, event=None):
        """Chamado quando perfil é alterado"""
        profile_name = self.profile_var.get()
        if profile_name:
            self.exclusion_manager.set_current_profile(profile_name)
            self.update_exclusions_tree()
    
    def create_new_profile(self):
        """Cria novo perfil de exclusão"""
        name = simpledialog.askstring("Novo Perfil", "Nome do perfil:")
        if name:
            description = simpledialog.askstring("Novo Perfil", "Descrição (opcional):") or ""
            try:
                self.exclusion_manager.create_profile(name, description)
                self.update_profiles_list()
                self.profile_var.set(name)
                self.exclusion_manager.set_current_profile(name)
                self.notifications.show_success(f"Perfil '{name}' criado!")
            except ValueError as e:
                self.notifications.show_error(str(e))
    
    def save_current_profile(self):
        """Salva perfil atual"""
        self.exclusion_manager.save_profiles()
        self.notifications.show_success("Perfil salvo!")
    
    def delete_current_profile(self):
        """Exclui perfil atual"""
        profile_name = self.profile_var.get()
        if profile_name:
            if messagebox.askyesno("Confirmar", f"Excluir perfil '{profile_name}'?"):
                try:
                    self.exclusion_manager.delete_profile(profile_name)
                    self.update_profiles_list()
                    self.notifications.show_success(f"Perfil '{profile_name}' excluído!")
                except ValueError as e:
                    self.notifications.show_error(str(e))
    
    def add_file_exclusion(self):
        """Adiciona exclusão de arquivo"""
        file_path = filedialog.askopenfilename(title="Selecione arquivo para excluir")
        if file_path:
            rule = ExclusionRule('file', file_path, f"Arquivo: {os.path.basename(file_path)}")
            self.exclusion_manager.add_rule_to_current_profile(rule)
            self.update_exclusions_tree()
            self.notifications.show_success("Exclusão de arquivo adicionada!")
    
    def add_folder_exclusion(self):
        """Adiciona exclusão de pasta"""
        folder_path = filedialog.askdirectory(title="Selecione pasta para excluir")
        if folder_path:
            rule = ExclusionRule('folder', folder_path, f"Pasta: {os.path.basename(folder_path)}")
            self.exclusion_manager.add_rule_to_current_profile(rule)
            self.update_exclusions_tree()
            self.notifications.show_success("Exclusão de pasta adicionada!")
    
    def add_extension_exclusion(self):
        """Adiciona exclusão por extensão"""
        extension = simpledialog.askstring("Exclusão por Extensão", 
                                          "Digite a extensão (ex: .tmp, .log):")
        if extension:
            if not extension.startswith('.'):
                extension = '.' + extension
            rule = ExclusionRule('extension', extension, f"Extensão: {extension}")
            self.exclusion_manager.add_rule_to_current_profile(rule)
            self.update_exclusions_tree()
            self.notifications.show_success(f"Exclusão de extensão '{extension}' adicionada!")
    
    def add_regex_exclusion(self):
        """Adiciona exclusão por regex"""
        pattern = simpledialog.askstring("Exclusão por Regex", 
                                        "Digite o padrão regex:")
        if pattern:
            description = simpledialog.askstring("Exclusão por Regex", 
                                                "Descrição (opcional):") or f"Regex: {pattern}"
            rule = ExclusionRule('regex', pattern, description)
            self.exclusion_manager.add_rule_to_current_profile(rule)
            self.update_exclusions_tree()
            self.notifications.show_success("Exclusão por regex adicionada!")
    
    def add_size_exclusion(self):
        """Adiciona exclusão por tamanho"""
        size_pattern = simpledialog.askstring("Exclusão por Tamanho", 
                                             "Digite o padrão de tamanho (ex: >10MB, <1KB):")
        if size_pattern:
            rule = ExclusionRule('size', size_pattern, f"Tamanho: {size_pattern}")
            self.exclusion_manager.add_rule_to_current_profile(rule)
            self.update_exclusions_tree()
            self.notifications.show_success("Exclusão por tamanho adicionada!")
    
    def preview_exclusions(self):
        """Mostra preview das exclusões"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        self.preview_processing()
    
    def update_exclusions_tree(self):
        """Atualiza a árvore de exclusões"""
        # Limpar árvore
        for item in self.exclusions_tree.get_children():
            self.exclusions_tree.delete(item)
        
        # Adicionar regras do perfil atual
        if self.exclusion_manager.current_profile:
            for rule in self.exclusion_manager.current_profile.rules:
                icon = {
                    'file': '📄',
                    'folder': '📁', 
                    'extension': '🏷',
                    'regex': '🔍',
                    'size': '📏',
                    'date': '📅'
                }.get(rule.rule_type, '❓')
                
                enabled_text = "✅" if rule.enabled else "❌"
                
                self.exclusions_tree.insert('', 'end', 
                                           text=f"{icon} {rule.description or rule.pattern}", 
                                           values=(rule.rule_type.title(), rule.pattern, enabled_text))
    
    def remove_selected_exclusion(self, event=None):
        """Remove exclusão selecionada"""
        selection = self.exclusions_tree.selection()
        if selection and self.exclusion_manager.current_profile:
            # Obter índice da regra
            item = selection[0]
            index = self.exclusions_tree.tree.index(item)
            
            # Remover regra
            self.exclusion_manager.remove_rule_from_current_profile(index)
            self.update_exclusions_tree()
            self.notifications.show_success("Exclusão removida!")
    
    def edit_exclusion(self, event=None):
        """Edita exclusão selecionada"""
        self.notifications.show_info("Funcionalidade de edição em desenvolvimento")
    
    # Métodos de resultados
    def refresh_results(self):
        """Atualiza a lista de resultados"""
        # Limpar árvore
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Listar arquivos do diretório de saída
        output_dir = self.config_manager.get_output_directory()
        
        try:
            for file_path in output_dir.iterdir():
                if file_path.is_file():
                    size_str = self._format_file_size(file_path.stat().st_size)
                    modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                    modified_str = modified.strftime("%d/%m/%Y %H:%M")
                    
                    self.results_tree.insert('', 'end', text=f"📄 {file_path.name}", 
                                           values=(size_str, file_path.suffix, modified_str))
        
        except Exception as e:
            self.notifications.show_error(f"Erro ao listar resultados: {str(e)}")
    
    def search_results(self, query):
        """Busca nos resultados"""
        if not query:
            self.refresh_results()
            return
        
        # Limpar árvore
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Buscar arquivos que correspondem à consulta
        output_dir = self.config_manager.get_output_directory()
        query_lower = query.lower()
        
        try:
            for file_path in output_dir.iterdir():
                if file_path.is_file() and query_lower in file_path.name.lower():
                    size_str = self._format_file_size(file_path.stat().st_size)
                    modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                    modified_str = modified.strftime("%d/%m/%Y %H:%M")
                    
                    self.results_tree.insert('', 'end', text=f"📄 {file_path.name}", 
                                           values=(size_str, file_path.suffix, modified_str))
        
        except Exception as e:
            self.notifications.show_error(f"Erro na busca: {str(e)}")
    
    def clear_search(self):
        """Limpa a busca"""
        self.refresh_results()
    
    def open_selected_file(self):
        """Abre arquivo selecionado"""
        selection = self.results_tree.selection()
        if selection:
            item = selection[0]
            filename = self.results_tree.tree.item(item, 'text').replace('📄 ', '')
            file_path = self.config_manager.get_output_directory() / filename
            self.open_file(str(file_path))
    
    def view_selected_file(self):
        """Visualiza arquivo selecionado"""
        selection = self.results_tree.selection()
        if selection:
            item = selection[0]
            filename = self.results_tree.tree.item(item, 'text').replace('📄 ', '')
            file_path = self.config_manager.get_output_directory() / filename
            self.view_file(str(file_path))
    
    def delete_selected_file(self):
        """Exclui arquivo selecionado"""
        selection = self.results_tree.selection()
        if selection:
            item = selection[0]
            filename = self.results_tree.tree.item(item, 'text').replace('📄 ', '')
            
            if messagebox.askyesno("Confirmar", f"Excluir arquivo '{filename}'?"):
                try:
                    file_path = self.config_manager.get_output_directory() / filename
                    file_path.unlink()
                    self.refresh_results()
                    self.notifications.show_success("Arquivo excluído!")
                except Exception as e:
                    self.notifications.show_error(f"Erro ao excluir arquivo: {str(e)}")
    
    def export_results(self):
        """Exporta resultados em múltiplos formatos"""
        if not self.last_processing_stats:
            self.notifications.show_warning("Nenhum processamento realizado ainda!")
            return
        
        # Dialog de seleção de formato
        dialog = tk.Toplevel(self.root)
        dialog.title("Exportar Resultados")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        frame = ttk.Frame(dialog, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = ttk.Label(frame, text="Selecione o formato de exportação:", style='Dark.TLabel')
        label.pack(anchor='w', pady=(0, 10))
        
        # Opções de formato
        format_var = tk.StringVar(value="html")
        
        formats = [
            ("HTML Interativo", "html"),
            ("JSON", "json"),
            ("XML", "xml"),
            ("Markdown", "markdown"),
            ("Relatório PDF", "pdf")
        ]
        
        for text, value in formats:
            radio = ttk.Radiobutton(frame, text=text, variable=format_var, 
                                   value=value, style='Dark.TRadiobutton')
            radio.pack(anchor='w', pady=2)
        
        # Botões
        buttons_frame = ttk.Frame(frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        def export():
            format_type = format_var.get()
            dialog.destroy()
            self.perform_export(format_type)
        
        export_button = ttk.Button(buttons_frame, text="Exportar", 
                                  style='Accent.TButton', command=export)
        export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(buttons_frame, text="Cancelar", 
                                  style='Dark.TButton', command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT)
    
    def perform_export(self, format_type):
        """Realiza a exportação no formato especificado"""
        try:
            # Preparar dados para exportação
            export_data = {
                "root_path": self.current_directory,
                "processing_mode": self.processing_mode.get(),
                "include_subdirectories": self.include_subdirectories.get(),
                "stats": self.last_processing_stats.to_dict() if self.last_processing_stats else {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Adicionar dados da árvore se disponível
            if self.current_directory_tree:
                scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
                export_data["tree_items"] = scanner.generate_tree_items_for_export(self.current_directory_tree)
            
            # Determinar nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == "html":
                output_path = self.config_manager.get_output_directory() / f"relatorio_{timestamp}.html"
                self.export_manager.export_directory_structure_to_html(export_data, str(output_path))
            
            elif format_type == "json":
                output_path = self.config_manager.get_output_directory() / f"dados_{timestamp}.json"
                self.export_manager.export_to_json(export_data, str(output_path))
            
            elif format_type == "xml":
                output_path = self.config_manager.get_output_directory() / f"dados_{timestamp}.xml"
                self.export_manager.export_to_xml(export_data, str(output_path))
            
            elif format_type == "markdown":
                output_path = self.config_manager.get_output_directory() / f"relatorio_{timestamp}.md"
                self.export_manager.export_to_markdown(export_data, str(output_path))
            
            else:
                self.notifications.show_warning(f"Formato '{format_type}' não implementado ainda")
                return
            
            self.notifications.show_success(f"Exportação concluída: {output_path.name}")
            self.refresh_results()
            
            # Abrir arquivo se configurado
            if self.auto_open_results.get():
                self.open_file(str(output_path))
        
        except Exception as e:
            self.notifications.show_error(f"Erro na exportação: {str(e)}")
    
    def open_output_folder(self):
        """Abre pasta de saída"""
        output_dir = self.config_manager.get_output_directory()
        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(output_dir))
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'xdg-open "{output_dir}"')
        except Exception as e:
            self.notifications.show_error(f"Erro ao abrir pasta: {str(e)}")
    
    def open_file(self, file_path):
        """Abre arquivo no programa padrão"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'xdg-open "{file_path}"')
        except Exception as e:
            self.notifications.show_error(f"Erro ao abrir arquivo: {str(e)}")
    
    def view_file(self, file_path):
        """Visualiza arquivo em janela interna"""
        try:
            # Criar janela de visualização
            viewer = tk.Toplevel(self.root)
            viewer.title(f"Visualizando: {os.path.basename(file_path)}")
            viewer.geometry("800x600")
            
            # Área de texto
            text_area = tk.Text(viewer, bg=DarkTheme.COLORS['bg_secondary'],
                               fg=DarkTheme.COLORS['text_primary'], 
                               font=('Courier New', 10), wrap=tk.WORD)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(viewer, orient=tk.VERTICAL, command=text_area.yview)
            text_area.configure(yscrollcommand=scrollbar.set)
            
            # Layout
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Carregar conteúdo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_area.insert('1.0', content)
            
            text_area.config(state='disabled')
        
        except Exception as e:
            self.notifications.show_error(f"Erro ao visualizar arquivo: {str(e)}")
    
    # Métodos de análises
    def update_statistics(self):
        """Atualiza estatísticas na aba de análises"""
        if not self.last_processing_stats:
            return
        
        # Limpar frame de estatísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Criar cards de estatísticas
        stats = self.last_processing_stats.to_dict()
        
        stats_items = [
            ("Arquivos Processados", stats.get('processed_files', 0)),
            ("Arquivos Excluídos", stats.get('excluded_files', 0)),
            ("Diretórios", stats.get('total_directories', 0)),
            ("Tamanho Total", self._format_file_size(stats.get('total_size', 0))),
            ("Duração", f"{stats.get('duration', 0):.1f}s"),
            ("Velocidade", f"{stats.get('processing_speed', 0):.1f} arq/s")
        ]
        
        # Organizar em grid
        for i, (label, value) in enumerate(stats_items):
            row = i // 3
            col = i % 3
            
            card_frame = DarkTheme.create_card_frame(self.stats_frame, padding=10)
            card_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            value_label = ttk.Label(card_frame, text=str(value), 
                                   style='Title.TLabel', anchor='center')
            value_label.pack()
            
            label_label = ttk.Label(card_frame, text=label, 
                                   style='Subtitle.TLabel', anchor='center')
            label_label.pack()
        
        # Configurar expansão das colunas
        for i in range(3):
            self.stats_frame.grid_columnconfigure(i, weight=1)
    
    def show_largest_files(self):
        """Mostra maiores arquivos"""
        if not self.current_directory_tree:
            self.notifications.show_warning("Execute um escaneamento primeiro!")
            return
        
        scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
        largest_files = scanner.get_largest_files(self.current_directory_tree, 20)
        
        # Limpar árvore de análise
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
        
        # Adicionar arquivos
        for file_node in largest_files:
            size_str = self._format_file_size(file_node.size)
            rel_path = os.path.relpath(file_node.path, self.current_directory)
            
            self.analysis_tree.insert('', 'end', text=f"📄 {file_node.name}", 
                                     values=(size_str, file_node.extension, rel_path))
        
        self.notifications.show_info(f"Mostrando {len(largest_files)} maiores arquivos")
    
    def show_extension_distribution(self):
        """Mostra distribuição de extensões"""
        if not self.current_directory_tree:
            self.notifications.show_warning("Execute um escaneamento primeiro!")
            return
        
        distribution = self.current_directory_tree.get_extension_distribution()
        
        # Limpar árvore de análise
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
        
        # Ordenar por quantidade
        sorted_extensions = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        
        # Adicionar extensões
        for ext, count in sorted_extensions:
            ext_display = ext if ext else "(sem extensão)"
            self.analysis_tree.insert('', 'end', text=f"🏷 {ext_display}", 
                                     values=(str(count), "arquivos", ""))
        
        self.notifications.show_info(f"Mostrando distribuição de {len(sorted_extensions)} extensões")
    
    def show_duplicate_names(self):
        """Mostra nomes duplicados"""
        if not self.current_directory_tree:
            self.notifications.show_warning("Execute um escaneamento primeiro!")
            return
        
        scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
        duplicates = scanner.get_duplicate_names(self.current_directory_tree)
        
        # Limpar árvore de análise
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
        
        # Adicionar duplicatas
        for name, nodes in duplicates.items():
            if len(nodes) > 1:
                parent_item = self.analysis_tree.insert('', 'end', text=f"📋 {name}", 
                                                       values=(str(len(nodes)), "duplicatas", ""))
                
                for node in nodes:
                    rel_path = os.path.relpath(node.path, self.current_directory)
                    icon = "📁" if node.is_directory else "📄"
                    self.analysis_tree.insert(parent_item, 'end', text=f"{icon} {rel_path}", 
                                            values=("", "", ""))
        
        self.notifications.show_info(f"Encontradas {len(duplicates)} duplicatas")
    
    def show_empty_directories(self):
        """Mostra diretórios vazios"""
        if not self.current_directory_tree:
            self.notifications.show_warning("Execute um escaneamento primeiro!")
            return
        
        scanner = DirectoryScanner(set(self.get_supported_extensions()), self.exclusion_manager)
        empty_dirs = scanner.get_empty_directories(self.current_directory_tree)
        
        # Limpar árvore de análise
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
        
        # Adicionar diretórios vazios
        for dir_node in empty_dirs:
            rel_path = os.path.relpath(dir_node.path, self.current_directory)
            self.analysis_tree.insert('', 'end', text=f"📁 {dir_node.name}", 
                                     values=("0", "arquivos", rel_path))
        
        self.notifications.show_info(f"Encontrados {len(empty_dirs)} diretórios vazios")
    
    # Métodos de configurações
    def update_extensions(self):
        """Atualiza lista de extensões suportadas"""
        try:
            extensions_text = self.extensions_var.get()
            extensions = [ext.strip() for ext in extensions_text.split() if ext.strip()]
            self.config_manager.set_supported_extensions(extensions)
            self.notifications.show_success("Extensões atualizadas!")
        except Exception as e:
            self.notifications.show_error(f"Erro ao atualizar extensões: {str(e)}")
    
    def export_config(self):
        """Exporta configurações"""
        file_path = filedialog.asksaveasfilename(
            title="Exportar Configurações",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.config_manager.export_config(file_path)
                self.notifications.show_success("Configurações exportadas!")
            except Exception as e:
                self.notifications.show_error(f"Erro ao exportar: {str(e)}")
    
    def import_config(self):
        """Importa configurações"""
        file_path = filedialog.askopenfilename(
            title="Importar Configurações",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.config_manager.import_config(file_path)
                self.load_settings()  # Recarregar interface
                self.notifications.show_success("Configurações importadas!")
            except Exception as e:
                self.notifications.show_error(f"Erro ao importar: {str(e)}")
    
    def reset_to_defaults(self):
        """Restaura configurações padrão"""
        if messagebox.askyesno("Confirmar", "Restaurar todas as configurações para os padrões?"):
            self.config_manager.reset_to_defaults()
            self.load_settings()  # Recarregar interface
            self.notifications.show_success("Configurações restauradas!")
    
    def cleanup_cache(self):
        """Limpa cache e arquivos temporários"""
        try:
            self.config_manager.cleanup_old_files()
            self.notifications.show_success("Cache limpo!")
        except Exception as e:
            self.notifications.show_error(f"Erro ao limpar cache: {str(e)}")
    
    # Métodos auxiliares
    def show_help(self):
        """Mostra ajuda"""
        help_text = """UltraTexto Pro - Ajuda

FUNCIONALIDADES PRINCIPAIS:
• Processamento de arquivos de código
• Sistema avançado de exclusões
• Geração de estruturas de diretório
• Exportação em múltiplos formatos
• Análises estatísticas detalhadas

COMO USAR:
1. Selecione um diretório
2. Configure exclusões se necessário
3. Escolha o modo de processamento
4. Clique em "Processar"

ATALHOS:
• Ctrl+P: Processar
• Ctrl+O: Selecionar diretório
• Ctrl+R: Abrir resultados
• Ctrl+F: Buscar
• Ctrl+,: Configurações

Para mais informações, consulte a documentação."""
        
        messagebox.showinfo("Ajuda - UltraTexto Pro", help_text)
    
    def show_about(self):
        """Mostra informações sobre o programa"""
        about_text = """UltraTexto Pro v2.0

Ferramenta avançada para processamento e análise de arquivos de código.

Desenvolvido com:
• Python 3.8+
• tkinter (interface gráfica)
• Tema escuro moderno

Recursos:
• Interface moderna e intuitiva
• Processamento eficiente de arquivos
• Sistema avançado de exclusões
• Múltiplos formatos de exportação
• Análises estatísticas detalhadas

© 2024 UltraTexto Pro Team"""
        
        messagebox.showinfo("Sobre - UltraTexto Pro", about_text)
    
    def update_exclusions_summary(self):
        """Atualiza o resumo das exclusões ativas na interface"""
        try:
            summary = self.exclusion_manager.get_exclusion_summary()
            
            if "error" in summary:
                self.profile_info_label.config(text="Erro: Nenhum perfil ativo")
                self.rules_info_label.config(text="Regras: 0 ativas")
                self.common_exclusions_label.config(text="Pastas excluídas: N/A")
                return
            
            # Atualizar informações do perfil
            self.profile_info_label.config(text=f"Perfil: {summary['profile_name']}")
            self.rules_info_label.config(text=f"Regras: {summary['enabled_rules']} ativas")
            
            # Mostrar pastas comuns excluídas
            common_exclusions = summary.get('common_exclusions', [])
            if common_exclusions:
                # Limitar a 5 pastas para não sobrecarregar a interface
                display_exclusions = common_exclusions[:5]
                if len(common_exclusions) > 5:
                    display_exclusions.append("...")
                self.common_exclusions_label.config(text=f"Pastas excluídas: {', '.join(display_exclusions)}")
            else:
                self.common_exclusions_label.config(text="Pastas excluídas: Nenhuma")
                
        except Exception as e:
            self.profile_info_label.config(text="Erro ao carregar resumo")
            self.rules_info_label.config(text="Regras: Erro")
            self.common_exclusions_label.config(text="Pastas excluídas: Erro")
            print(f"Erro ao atualizar resumo das exclusões: {e}")
    
    def _format_file_size(self, size_bytes):
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
    
    def on_closing(self):
        """Chamado ao fechar a aplicação"""
        # Salvar configurações
        self.save_settings()
        
        # Fechar aplicação
        self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        # Carregar resultados iniciais
        self.refresh_results()
        
        # Iniciar loop principal
        self.root.mainloop()
    
    def clone_directory_action(self):
        """Ação para clonar diretório com exclusões"""
        source_dir = filedialog.askdirectory(title="Selecione a pasta de origem para clonar")
        if not source_dir:
            return
        dest_dir = filedialog.askdirectory(title="Selecione a pasta de destino para clonagem")
        if not dest_dir:
            return
        include_subdirs = self.include_subdirectories.get()
        scanner = DirectoryScanner(self.get_supported_extensions(), self.exclusion_manager)
        try:
            self.status_bar.set_status("Clonando diretório...")
            total = scanner.clone_directory_with_exclusions(source_dir, dest_dir, include_subdirectories=include_subdirs)
            self.notifications.show_info(f"Clonagem concluída! {total} itens copiados.")
            self.status_bar.set_status(f"Clonagem concluída: {total} itens copiados.")
        except Exception as e:
            self.notifications.show_error(f"Erro ao clonar diretório: {e}")
            self.status_bar.set_status("Erro na clonagem.")

def main():
    """Função principal"""
    app = UltraTextoPro()
    app.run()

if __name__ == "__main__":
    main()

