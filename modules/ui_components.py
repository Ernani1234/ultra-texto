"""
Componentes de interface reutilizáveis para UltraTexto Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class ProgressDialog:
    """Dialog de progresso com barra e cancelamento"""
    
    def __init__(self, parent, title="Processando...", message="Aguarde..."):
        self.parent = parent
        self.cancelled = False
        
        # Criar janela modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (150 // 2)
        self.dialog.geometry(f"400x150+{x}+{y}")
        
        # Configurar layout
        main_frame = ttk.Frame(self.dialog, style='Dark.TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de mensagem
        self.message_label = ttk.Label(main_frame, text=message, style='Dark.TLabel')
        self.message_label.pack(pady=(0, 10))
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, style='Dark.Horizontal.TProgressbar', 
                                       mode='indeterminate', length=350)
        self.progress.pack(pady=(0, 10))
        self.progress.start(10)
        
        # Label de status
        self.status_label = ttk.Label(main_frame, text="", style='Subtitle.TLabel')
        self.status_label.pack(pady=(0, 10))
        
        # Botão cancelar
        self.cancel_button = ttk.Button(main_frame, text="Cancelar", 
                                       style='Dark.TButton', command=self.cancel)
        self.cancel_button.pack()
        
        # Protocolo de fechamento
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def update_message(self, message):
        """Atualiza a mensagem principal"""
        self.message_label.config(text=message)
        self.dialog.update()
    
    def update_status(self, status):
        """Atualiza o status"""
        self.status_label.config(text=status)
        self.dialog.update()
    
    def set_progress(self, value):
        """Define progresso específico (0-100)"""
        self.progress.config(mode='determinate')
        self.progress['value'] = value
        self.dialog.update()
    
    def cancel(self):
        """Cancela a operação"""
        self.cancelled = True
        self.close()
    
    def close(self):
        """Fecha o dialog"""
        self.progress.stop()
        self.dialog.destroy()

class NotificationManager:
    """Gerenciador de notificações toast"""
    
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
    
    def show_success(self, message, duration=3000):
        """Mostra notificação de sucesso"""
        self._show_notification(message, "success", duration)
    
    def show_error(self, message, duration=5000):
        """Mostra notificação de erro"""
        self._show_notification(message, "error", duration)
    
    def show_warning(self, message, duration=4000):
        """Mostra notificação de aviso"""
        self._show_notification(message, "warning", duration)
    
    def show_info(self, message, duration=3000):
        """Mostra notificação de informação"""
        self._show_notification(message, "info", duration)
    
    def _show_notification(self, message, type_="info", duration=3000):
        """Mostra uma notificação toast"""
        from themes.dark_theme import DarkTheme
        
        # Criar janela de notificação
        notification = tk.Toplevel(self.parent)
        notification.overrideredirect(True)
        notification.attributes('-topmost', True)
        
        # Configurar cores baseadas no tipo
        colors = {
            'success': DarkTheme.COLORS['success'],
            'error': DarkTheme.COLORS['error'],
            'warning': DarkTheme.COLORS['warning'],
            'info': DarkTheme.COLORS['info']
        }
        
        bg_color = colors.get(type_, DarkTheme.COLORS['info'])
        
        # Frame principal
        frame = tk.Frame(notification, bg=bg_color, padx=15, pady=10)
        frame.pack()
        
        # Label da mensagem
        label = tk.Label(frame, text=message, bg=bg_color, 
                        fg=DarkTheme.COLORS['text_primary'],
                        font=('Segoe UI', 9))
        label.pack()
        
        # Posicionar no canto superior direito
        notification.update_idletasks()
        width = notification.winfo_width()
        height = notification.winfo_height()
        x = self.parent.winfo_screenwidth() - width - 20
        y = 20 + len(self.notifications) * (height + 10)
        notification.geometry(f"+{x}+{y}")
        
        # Adicionar à lista
        self.notifications.append(notification)
        
        # Agendar remoção
        def remove_notification():
            if notification in self.notifications:
                self.notifications.remove(notification)
                notification.destroy()
                # Reposicionar outras notificações
                self._reposition_notifications()
        
        notification.after(duration, remove_notification)
        
        # Permitir fechar clicando
        frame.bind("<Button-1>", lambda e: remove_notification())
        label.bind("<Button-1>", lambda e: remove_notification())
    
    def _reposition_notifications(self):
        """Reposiciona as notificações após remoção"""
        for i, notification in enumerate(self.notifications):
            if notification.winfo_exists():
                height = notification.winfo_height()
                x = self.parent.winfo_screenwidth() - notification.winfo_width() - 20
                y = 20 + i * (height + 10)
                notification.geometry(f"+{x}+{y}")

class FileTreeView:
    """Componente de visualização em árvore de arquivos"""
    
    def __init__(self, parent, columns=None, **kwargs):
        self.parent = parent
        
        # Frame principal
        self.frame = ttk.Frame(parent, style='Dark.TFrame')
        
        # Treeview com scrollbars
        self.tree = ttk.Treeview(self.frame, style='Dark.Treeview', **kwargs)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, 
                                   command=self.tree.yview, style='Dark.Vertical.TScrollbar')
        h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, 
                                   command=self.tree.xview, style='Dark.Horizontal.TScrollbar')
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Configurar colunas
        if columns:
            self.tree['columns'] = columns
            self.tree.heading('#0', text='Nome', anchor='w')
            # Não configurar headings automáticos para colunas personalizadas
        else:
            # Configuração padrão
            self.tree['columns'] = ('size', 'type', 'modified')
            self.tree.heading('#0', text='Nome', anchor='w')
            self.tree.heading('size', text='Tamanho', anchor='e')
            self.tree.heading('type', text='Tipo', anchor='w')
            self.tree.heading('modified', text='Modificado', anchor='w')
            
            self.tree.column('#0', width=300, minwidth=200)
            self.tree.column('size', width=100, minwidth=80)
            self.tree.column('type', width=100, minwidth=80)
            self.tree.column('modified', width=150, minwidth=120)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def insert(self, parent, index, **kwargs):
        return self.tree.insert(parent, index, **kwargs)
    
    def delete(self, *items):
        self.tree.delete(*items)
    
    def get_children(self, item=''):
        return self.tree.get_children(item)
    
    def selection(self):
        return self.tree.selection()
    
    def item(self, item, option=None, **kwargs):
        return self.tree.item(item, option, **kwargs)

class SearchBox:
    """Componente de caixa de busca com filtros"""
    
    def __init__(self, parent, on_search=None, on_clear=None):
        self.parent = parent
        self.on_search = on_search
        self.on_clear = on_clear
        
        # Frame principal
        self.frame = ttk.Frame(parent, style='Card.TFrame', padding=10)
        
        # Label
        label = ttk.Label(self.frame, text="Buscar:", style='Dark.TLabel')
        label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # Entry de busca
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var, 
                                     style='Dark.TEntry', width=30)
        self.search_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        
        # Botão buscar
        self.search_button = ttk.Button(self.frame, text="Buscar", 
                                       style='Accent.TButton', command=self._on_search)
        self.search_button.grid(row=0, column=2, padx=(0, 5))
        
        # Botão limpar
        self.clear_button = ttk.Button(self.frame, text="Limpar", 
                                      style='Dark.TButton', command=self._on_clear)
        self.clear_button.grid(row=0, column=3)
        
        # Configurar expansão
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Bind Enter
        self.search_entry.bind('<Return>', lambda e: self._on_search())
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def get_text(self):
        return self.search_var.get()
    
    def set_text(self, text):
        self.search_var.set(text)
    
    def clear(self):
        self.search_var.set("")
    
    def _on_search(self):
        if self.on_search:
            self.on_search(self.get_text())
    
    def _on_clear(self):
        self.clear()
        if self.on_clear:
            self.on_clear()

class StatusBar:
    """Barra de status na parte inferior"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Frame principal
        self.frame = ttk.Frame(parent, style='Card.TFrame', padding=(10, 5))
        
        # Label de status
        self.status_var = tk.StringVar(value="Pronto")
        self.status_label = ttk.Label(self.frame, textvariable=self.status_var, 
                                     style='Subtitle.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Separador
        separator = ttk.Separator(self.frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Informações adicionais
        self.info_var = tk.StringVar(value="")
        self.info_label = ttk.Label(self.frame, textvariable=self.info_var, 
                                   style='Subtitle.TLabel')
        self.info_label.pack(side=tk.LEFT)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def set_status(self, status):
        self.status_var.set(status)
    
    def set_info(self, info):
        self.info_var.set(info)
    
    def clear(self):
        self.status_var.set("Pronto")
        self.info_var.set("")

