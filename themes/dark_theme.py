"""
Tema escuro moderno e amigável para UltraTexto Pro
"""

import tkinter as tk
from tkinter import ttk

class DarkTheme:
    """Classe para aplicar tema escuro moderno e amigável à interface"""
    
    # Paleta de cores amigável e suave
    COLORS = {
        'bg_primary': '#2b2b3a',      # Fundo principal - azul escuro suave
        'bg_secondary': '#3a3a4a',    # Fundo secundário - azul médio
        'bg_tertiary': '#4a4a5a',     # Fundo terciário - azul claro
        'bg_hover': '#5a5a6a',        # Hover - azul mais claro
        'bg_selected': '#4a7c59',     # Selecionado - verde azulado suave
        'text_primary': '#f0f0f5',    # Texto principal - branco suave
        'text_secondary': '#c0c0d0',  # Texto secundário - cinza azulado
        'text_disabled': '#808090',   # Texto desabilitado - cinza médio
        'accent_primary': '#64b5f6',  # Cor de destaque principal - azul claro
        'accent_secondary': '#42a5f5', # Cor de destaque secundária - azul médio
        'success': '#81c784',         # Verde sucesso - verde suave
        'warning': '#ffb74d',         # Laranja aviso - laranja suave
        'error': '#e57373',           # Vermelho erro - vermelho suave
        'info': '#81c784',            # Azul informação - verde azulado
        'border': '#6a6a7a',          # Bordas - cinza azulado
        'border_light': '#8a8a9a',    # Bordas claras - cinza claro
        'card_bg': '#323242',         # Fundo dos cards - azul escuro
        'button_bg': '#4a5a6a',       # Fundo dos botões - azul acinzentado
        'button_hover': '#5a6a7a',    # Hover dos botões - azul mais claro
        'input_bg': '#3a3a4a',        # Fundo dos inputs - azul médio
        'tab_bg': '#4a4a5a',          # Fundo das abas - azul claro
        'tab_selected': '#5a5a6a',    # Aba selecionada - azul mais claro
    }
    
    @classmethod
    def apply_theme(cls, root):
        """Aplica o tema escuro amigável à janela principal"""
        
        # Configurar estilo ttk
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Configurar cores da janela principal
        root.configure(bg=cls.COLORS['bg_primary'])
        
        # Configurar estilos dos widgets ttk
        cls._configure_ttk_styles(style)
        
        return style
    
    @classmethod
    def _configure_ttk_styles(cls, style):
        """Configura estilos específicos para widgets ttk"""
        
        # Frame
        style.configure('Dark.TFrame',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=cls.COLORS['card_bg'],
                       relief='solid',
                       borderwidth=1,
                       bordercolor=cls.COLORS['border'])
        
        # Label
        style.configure('Dark.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 10))
        
        style.configure('Title.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=('Segoe UI', 10))
        
        # Button
        style.configure('Dark.TButton',
                       background=cls.COLORS['button_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       focuscolor='none',
                       font=('Segoe UI', 9),
                       relief='flat')
        
        style.map('Dark.TButton',
                 background=[('active', cls.COLORS['button_hover']),
                           ('pressed', cls.COLORS['bg_selected'])])
        
        style.configure('Accent.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        
        style.map('Accent.TButton',
                 background=[('active', cls.COLORS['accent_secondary']),
                           ('pressed', cls.COLORS['accent_secondary'])])
        
        # Entry
        style.configure('Dark.TEntry',
                       fieldbackground=cls.COLORS['input_bg'],
                       background=cls.COLORS['input_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       insertcolor=cls.COLORS['text_primary'],
                       relief='flat')
        
        style.map('Dark.TEntry',
                 focuscolor=[('!focus', cls.COLORS['border']),
                           ('focus', cls.COLORS['accent_primary'])])
        
        # Combobox
        style.configure('Dark.TCombobox',
                       fieldbackground=cls.COLORS['input_bg'],
                       background=cls.COLORS['input_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       arrowcolor=cls.COLORS['text_primary'],
                       relief='flat')
        
        # Checkbutton
        style.configure('Dark.TCheckbutton',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        # Radiobutton
        style.configure('Dark.TRadiobutton',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        # Progressbar
        style.configure('Dark.Horizontal.TProgressbar',
                       background=cls.COLORS['accent_primary'],
                       troughcolor=cls.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['accent_primary'],
                       darkcolor=cls.COLORS['accent_primary'])
        
        # Notebook (abas)
        style.configure('Dark.TNotebook',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('Dark.TNotebook.Tab',
                       background=cls.COLORS['tab_bg'],
                       foreground=cls.COLORS['text_secondary'],
                       padding=[20, 10],
                       font=('Segoe UI', 9),
                       relief='flat')
        
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', cls.COLORS['tab_selected']),
                           ('active', cls.COLORS['bg_hover'])],
                 foreground=[('selected', cls.COLORS['text_primary']),
                           ('active', cls.COLORS['text_primary'])])
        
        # Treeview
        style.configure('Dark.Treeview',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       fieldbackground=cls.COLORS['bg_secondary'],
                       borderwidth=1,
                       font=('Segoe UI', 9),
                       relief='flat')
        
        style.configure('Dark.Treeview.Heading',
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        
        style.map('Dark.Treeview',
                 background=[('selected', cls.COLORS['bg_selected'])],
                 foreground=[('selected', cls.COLORS['text_primary'])])
        
        # Scrollbar
        style.configure('Dark.Vertical.TScrollbar',
                       background=cls.COLORS['bg_tertiary'],
                       troughcolor=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       arrowcolor=cls.COLORS['text_secondary'],
                       darkcolor=cls.COLORS['bg_tertiary'],
                       lightcolor=cls.COLORS['bg_tertiary'])
        
        style.configure('Dark.Horizontal.TScrollbar',
                       background=cls.COLORS['bg_tertiary'],
                       troughcolor=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       arrowcolor=cls.COLORS['text_secondary'],
                       darkcolor=cls.COLORS['bg_tertiary'],
                       lightcolor=cls.COLORS['bg_tertiary'])
    
    @classmethod
    def create_styled_widget(cls, widget_class, parent, style_name, **kwargs):
        """Cria um widget com estilo aplicado"""
        widget = widget_class(parent, style=style_name, **kwargs)
        return widget
    
    @classmethod
    def create_card_frame(cls, parent, **kwargs):
        """Cria um frame estilizado como card"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
    
    @classmethod
    def create_title_label(cls, parent, text, **kwargs):
        """Cria um label de título"""
        label = ttk.Label(parent, text=text, style='Title.TLabel', **kwargs)
        return label
    
    @classmethod
    def create_subtitle_label(cls, parent, text, **kwargs):
        """Cria um label de subtítulo"""
        label = ttk.Label(parent, text=text, style='Subtitle.TLabel', **kwargs)
        return label

