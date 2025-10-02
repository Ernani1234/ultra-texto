#!/usr/bin/env python3
"""
Visualizador de Cores do Tema - UltraTexto Pro
Mostra como ficaram as novas cores amigáveis
"""

import tkinter as tk
from tkinter import ttk
from dark_theme import DarkTheme

class ColorPreview:
    """Janela para visualizar as cores do tema"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Visualizador de Cores - UltraTexto Pro")
        self.root.geometry("800x600")
        
        # Aplicar tema
        self.style = DarkTheme.apply_theme(self.root)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface de visualização"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = DarkTheme.create_title_label(main_frame, "🎨 Paleta de Cores Amigável")
        title.pack(pady=(0, 20))
        
        subtitle = DarkTheme.create_subtitle_label(main_frame, "Novas cores suaves e agradáveis para a interface")
        subtitle.pack(pady=(0, 30))
        
        # Grid de cores
        self.create_color_grid(main_frame)
        
        # Exemplos de widgets
        self.create_widget_examples(main_frame)
    
    def create_color_grid(self, parent):
        """Cria grid com as cores do tema"""
        colors_frame = DarkTheme.create_card_frame(parent, padding=20)
        colors_frame.pack(fill=tk.X, pady=(0, 20))
        
        colors_label = ttk.Label(colors_frame, text="🎨 Paleta de Cores", style='Title.TLabel')
        colors_label.pack(anchor='w', pady=(0, 15))
        
        # Grid de cores
        grid_frame = ttk.Frame(colors_frame, style='Dark.TFrame')
        grid_frame.pack(fill=tk.X)
        
        colors = [
            ('bg_primary', 'Fundo Principal', '#2b2b3a'),
            ('bg_secondary', 'Fundo Secundário', '#3a3a4a'),
            ('card_bg', 'Fundo dos Cards', '#323242'),
            ('button_bg', 'Fundo dos Botões', '#4a5a6a'),
            ('accent_primary', 'Destaque Principal', '#64b5f6'),
            ('accent_secondary', 'Destaque Secundário', '#42a5f5'),
            ('text_primary', 'Texto Principal', '#f0f0f5'),
            ('text_secondary', 'Texto Secundário', '#c0c0d0'),
            ('success', 'Sucesso', '#81c784'),
            ('warning', 'Aviso', '#ffb74d'),
            ('error', 'Erro', '#e57373'),
            ('border', 'Bordas', '#6a6a7a'),
        ]
        
        for i, (key, name, color) in enumerate(colors):
            row = i // 3
            col = i % 3
            
            # Frame para cada cor
            color_frame = ttk.Frame(grid_frame, style='Dark.TFrame')
            color_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            # Amostra da cor
            color_sample = tk.Label(color_frame, bg=color, width=8, height=2, relief='solid', borderwidth=1)
            color_sample.pack(pady=(0, 5))
            
            # Nome da cor
            name_label = ttk.Label(color_frame, text=name, style='Dark.TLabel')
            name_label.pack()
            
            # Código da cor
            code_label = ttk.Label(color_frame, text=color, style='Subtitle.TLabel')
            code_label.pack()
        
        # Configurar pesos das colunas
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(2, weight=1)
    
    def create_widget_examples(self, parent):
        """Cria exemplos de widgets com o novo tema"""
        examples_frame = DarkTheme.create_card_frame(parent, padding=20)
        examples_frame.pack(fill=tk.X)
        
        examples_label = ttk.Label(examples_frame, text="🔧 Exemplos de Widgets", style='Title.TLabel')
        examples_label.pack(anchor='w', pady=(0, 15))
        
        # Grid de exemplos
        examples_grid = ttk.Frame(examples_frame, style='Dark.TFrame')
        examples_grid.pack(fill=tk.X)
        
        # Coluna 1: Botões
        buttons_frame = ttk.Frame(examples_grid, style='Dark.TFrame')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        buttons_label = ttk.Label(buttons_frame, text="Botões", style='Dark.TLabel')
        buttons_label.pack(anchor='w', pady=(0, 10))
        
        normal_button = ttk.Button(buttons_frame, text="Botão Normal", style='Dark.TButton')
        normal_button.pack(fill=tk.X, pady=2)
        
        accent_button = ttk.Button(buttons_frame, text="Botão Destaque", style='Accent.TButton')
        accent_button.pack(fill=tk.X, pady=2)
        
        # Coluna 2: Inputs
        inputs_frame = ttk.Frame(examples_grid, style='Dark.TFrame')
        inputs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        inputs_label = ttk.Label(inputs_frame, text="Campos de Entrada", style='Dark.TLabel')
        inputs_label.pack(anchor='w', pady=(0, 10))
        
        entry = ttk.Entry(inputs_frame, style='Dark.TEntry')
        entry.pack(fill=tk.X, pady=2)
        entry.insert(0, "Texto de exemplo")
        
        combobox = ttk.Combobox(inputs_frame, style='Dark.TCombobox')
        combobox.pack(fill=tk.X, pady=2)
        combobox['values'] = ['Opção 1', 'Opção 2', 'Opção 3']
        combobox.set('Opção 1')
        
        # Coluna 3: Outros
        others_frame = ttk.Frame(examples_grid, style='Dark.TFrame')
        others_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        others_label = ttk.Label(others_frame, text="Outros Elementos", style='Dark.TLabel')
        others_label.pack(anchor='w', pady=(0, 10))
        
        checkbox = ttk.Checkbutton(others_frame, text="Checkbox", style='Dark.TCheckbutton')
        checkbox.pack(anchor='w', pady=2)
        
        radio = ttk.Radiobutton(others_frame, text="Radio Button", style='Dark.TRadiobutton')
        radio.pack(anchor='w', pady=2)
        
        progress = ttk.Progressbar(others_frame, style='Dark.Horizontal.TProgressbar', length=150)
        progress.pack(pady=2)
        progress['value'] = 65
        
        # Configurar pesos das colunas
        examples_grid.columnconfigure(0, weight=1)
        examples_grid.columnconfigure(1, weight=1)
        examples_grid.columnconfigure(2, weight=1)
    
    def run(self):
        """Executa a visualização"""
        self.root.mainloop()

def main():
    """Função principal"""
    preview = ColorPreview()
    preview.run()

if __name__ == "__main__":
    main()
