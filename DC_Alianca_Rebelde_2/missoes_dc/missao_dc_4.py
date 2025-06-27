# Arquivo: missoes_dc/missao_dc_4.py

import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random

try:
    from algoritmos_dc.karatsuba import karatsuba
except ImportError:
    print("AVISO: Módulo 'karatsuba' não encontrado. Usando multiplicação padrão como fallback.")
    def karatsuba(x_bin, y_bin):
        return int(x_bin, 2) * int(y_bin, 2)

class MissaoDC4:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame
        self._carregar_estilos()

        # --- Estado da Missão ---
        self.etapa_atual = None
        self.proxima_etapa = None
        self.valores = {}
        self.componente_selecionado = None
        self.widgets = {}

    def _carregar_estilos(self):
        try:
            self.cor_fundo_base = self.game_manager.bg_color_dark
            self.cor_texto_principal = self.game_manager.fg_color_light
            self.cor_texto_titulo_missao = self.game_manager.title_color_accent
            self.cor_info = "#87CEFA"
            self.cor_sucesso = "#7FFF00"
            self.cor_erro = "#FF6347"
            self.cor_selecao = self.game_manager.title_color_accent
            self.cor_componente = "#4A4A4A"
            self.cor_slot = "#1A1A1A"
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.button_font_obj = self.game_manager.button_font_obj
            self.binary_font_obj = tkFont.Font(family="Courier", size=14, weight="bold")
            self.binary_font_small = tkFont.Font(family="Courier", size=11)
        except AttributeError:
            self.cor_fundo_base, self.cor_texto_principal, self.cor_texto_titulo_missao = "black", "white", "orangered"
            self.cor_sucesso, self.cor_erro, self.cor_selecao = "green", "red", "gold"
            self.cor_componente, self.cor_slot = "#4A4A4A", "#1A1A1A"
            self.header_font_obj, self.narrative_font_obj, self.button_font_obj = ("Arial", 20, "bold"), ("Arial", 12), ("Arial", 14, "bold")
            self.binary_font_obj, self.binary_font_small = ("Courier", 14, "bold"), ("Courier", 11)

    def _limpar_widgets_do_frame(self, frame):
        for widget in frame.winfo_children(): widget.destroy()
        chaves_persistentes = {'content_frame', 'dados_labels'}
        widgets_para_limpar = {k: v for k, v in self.widgets.items() if k not in chaves_persistentes}
        for chave in widgets_para_limpar: del self.widgets[chave]
        self.componente_selecionado = None
        
    def iniciar_missao_contexto(self):
        self._limpar_widgets_do_frame(self.base_content_frame)
        tk.Label(self.base_content_frame, text="MISSÃO 4: Quebra de Códigos", font=self.header_font_obj, fg=self.cor_texto_titulo_missao, bg=self.cor_fundo_base).pack(pady=(10,15))
        try:
            imagem_missao = self.game_manager.imagens.get("Cena6.png")
            if imagem_missao: tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo_base).pack(pady=10)
        except: pass
        contexto = "Fulcrum: \"Comandante, a chave de um protocolo Imperial é o produto de dois números-semente binários. Use a 'Multiplicação de Karatsuba' para guiar nosso computador e quebrar o código a tempo.\""
        tk.Label(self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT, font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=10, padx=20)
        ttk.Button(self.base_content_frame, text="Iniciar Análise Criptográfica...", command=self.iniciar_missao, style="Accent.Dark.TButton").pack(pady=20)

    def iniciar_missao(self):
        self._gerar_numeros()
        self._criar_layout_principal()
        self.mudar_etapa('DIVIDIR')

    def _gerar_numeros(self):
        self.valores.clear()
        self.n = 4; n = self.n; self.n2 = n // 2
        num1 = random.randint(2**(n - 1), 2**n - 1); num2 = random.randint(2**(n - 1), 2**n - 1)
        self.valores['x'] = bin(num1)[2:].zfill(n); self.valores['y'] = bin(num2)[2:].zfill(n)
        self.valores['resultado_final'] = karatsuba(self.valores['x'], self.valores['y'])

    def _criar_layout_principal(self):
        self._limpar_widgets_do_frame(self.base_content_frame)
        
        painel_dados = tk.Frame(self.base_content_frame, bg="#101010", width=300, relief=tk.SUNKEN, bd=2)
        painel_dados.pack(side=tk.LEFT, fill=tk.Y, padx=(5,2), pady=5); painel_dados.pack_propagate(False)

        self.widgets['content_frame'] = tk.Frame(self.base_content_frame, bg=self.cor_fundo_base)
        self.widgets['content_frame'].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2,5), pady=5)

        tk.Label(painel_dados, text="Painel de Criptografia", font=self.button_font_obj, fg=self.cor_info, bg="#101010").pack(pady=10)
        grid_frame = tk.Frame(painel_dados, bg="#101010"); grid_frame.pack(fill=tk.X, padx=10)
        
        self.widgets['dados_labels'] = {}
        formulas_data = [
            ("x:", 'x', self.valores['x']), ("y:", 'y', self.valores['y']),
            ("--- DIVISÃO ---", 'sep1', ""), ("x1:", 'x1', "?"), ("x0:", 'x0', "?"), ("y1:", 'y1', "?"), ("y0:", 'y0', "?"),
            ("--- CÁLCULOS ---", 'sep2', ""), ("A = x1*y1:", 'A', "?"), ("C = x0*y0:", 'C', "?"),
            ("soma_x = x1+x0:", 'soma_x', "?"), ("soma_y = y1+y0:", 'soma_y', "?"),
            ("B = soma_x*soma_y:", 'B', "?"), ("TermoMeio = B-A-C:", 'TermoMeio', "?"),
        ]
        
        for i, (texto_label, chave_dados, valor_inicial) in enumerate(formulas_data):
            lbl_chave = tk.Label(grid_frame, text=texto_label, font=self.binary_font_small, fg=self.cor_info, bg="#101010", anchor='w')
            lbl_chave.grid(row=i, column=0, sticky='w')
            
            if not chave_dados.startswith('sep'):
                lbl_valor = tk.Label(grid_frame, text=valor_inicial, font=self.binary_font_small, fg="white", bg="#101010", anchor='w')
                lbl_valor.grid(row=i, column=1, sticky='w', padx=5); self.widgets['dados_labels'][chave_dados] = lbl_valor

        tk.Label(painel_dados, text="Fórmula Final:", font=self.binary_font_small, fg=self.cor_info, bg="#101010").pack(pady=(20, 5))
        formula_final = f"(A << {2*self.n2}) + (TermoMeio << {self.n2}) + C"
        tk.Label(painel_dados, text=formula_final, font=self.binary_font_small, fg="white", bg="#101010", wraplength=280).pack()

    def _atualizar_painel_dados(self):
        if 'dados_labels' not in self.widgets: return
        for chave_dados, widget in self.widgets['dados_labels'].items():
            if chave_dados in self.valores:
                valor = self.valores[chave_dados]
                texto = bin(valor)[2:] if isinstance(valor, int) else str(valor)
                if widget.cget('text') != texto: widget.config(text=texto, fg=self.cor_sucesso)

    def mudar_etapa(self, nova_etapa):
        self.etapa_atual = nova_etapa
        content_frame = self.widgets['content_frame']
        self._limpar_widgets_do_frame(content_frame)
        self._atualizar_painel_dados()

        etapa_info = {
            'DIVIDIR': (1, "Dividir as Chaves"), 'CALC_A': (2, "Calcular Componente A"),
            'CALC_C': (3, "Calcular Componente C"), 'CALC_SOMAS': (4, "Calcular Somas Intermediárias"),
            'CALC_B': (5, "Calcular Componente B"), 'ISOLAR_MEIO': (6, "Isolar o Termo do Meio"),
            'COMBINAR': (7, "Alinhar Componentes Finais"), 'CALC_FINAL': (8, "Calcular Chave Final")
        }
        num_etapa, desc_etapa = etapa_info[nova_etapa]
        tk.Label(content_frame, text=f"Etapa {num_etapa}/8: {desc_etapa}", font=self.button_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=(10,20))
        
        bottom_frame = tk.Frame(content_frame, bg=self.cor_fundo_base)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.widgets['status_label'] = tk.Label(bottom_frame, text="", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base, height=2, wraplength=450, justify=tk.LEFT)
        self.widgets['status_label'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(bottom_frame, text="Ajuda (?)", command=self._mostrar_ajuda, style="Dark.TButton").pack(side=tk.RIGHT, padx=10)

        getattr(self, f'_montar_tela_{self.etapa_atual.lower()}')(content_frame)
        
    def _mostrar_ajuda(self):
        dicas = {
            'DIVIDIR': "Divida cada número de 4 bits em duas partes de 2 bits. 'x1' são os 2 primeiros bits de 'x', e 'x0' são os 2 últimos.",
            'CALC_A': f"Multiplique os binários x1 ({self.valores.get('x1','?')}) e y1 ({self.valores.get('y1','?')}). Lembre-se que 10 é 2 em decimal, e 11 é 3.",
            'CALC_C': f"Similarmente, multiplique x0 ({self.valores.get('x0','?')}) por y0 ({self.valores.get('y0','?')}).",
            'CALC_SOMAS': "Some os binários de cada par: (x1 + x0) e (y1 + y0). Esta é a preparação para o truque de Karatsuba.",
            'CALC_B': "Agora multiplique os resultados das duas somas que você acabou de fazer.",
            'ISOLAR_MEIO': "Este é o coração do algoritmo! A fórmula para o termo do meio é sempre B - A - C. Clique nos componentes na ordem correta para encaixá-los na fórmula.",
            'COMBINAR': "Quase lá! Cada peça (A, TermoMeio, C) tem uma posição final. A posição é definida pelo deslocamento de bits (<<). Clique nas peças e coloque-as nos seus respectivos slots de alinhamento.",
            'CALC_FINAL': "Some os três números alinhados que aparecem na tela. Você pode fazer isso em um papel ou calculadora. O resultado é a chave final!"
        }
        dica = dicas.get(self.etapa_atual, "Nenhuma dica específica para esta etapa.")
        messagebox.showinfo("Dica do PA09CD", dica, parent=self.base_content_frame)

    def _set_status(self, text, status="normal"):
        self.widgets['status_label'].config(text=text, fg={"normal": self.cor_texto_principal, "sucesso": self.cor_sucesso, "erro": self.cor_erro}[status])

    def _selecionar_componente(self, nome_componente):
        if self.componente_selecionado and self.componente_selecionado in self.widgets: self.widgets[self.componente_selecionado].config(bg=self.cor_componente)
        self.componente_selecionado = nome_componente; self.widgets[nome_componente].config(bg=self.cor_selecao)
        self._set_status(f"Componente '{nome_componente}' selecionado. Clique no slot de destino.")

    def _colocar_componente(self, slot_destino):
        if not self.componente_selecionado:
            self._set_status("Nenhum componente selecionado. Clique em um componente na bancada.", "erro"); return
        
        if self.componente_selecionado == slot_destino:
            self._set_status(f"Correto! Componente '{slot_destino}' posicionado.", "sucesso")
            
            slot_widget_label = self.widgets[f"slot_{slot_destino}_label"]
            valor_bin = bin(self.valores[slot_destino])[2:]
            slot_widget_label.config(text=f"{slot_destino}\n{valor_bin}", bg=self.cor_sucesso, fg="black", font=self.binary_font_small)
            
            comp_widget = self.widgets[self.componente_selecionado]
            comp_widget.config(bg="#222", fg="#555", relief=tk.SUNKEN); comp_widget.unbind("<Button-1>")
            
            self.componente_selecionado = None
            del self.widgets[f"slot_{slot_destino}_label"]

            if not any(key.startswith('slot_') for key in self.widgets):
                 self.root.after(1500, lambda: self.mudar_etapa(self.proxima_etapa))
        else: self._set_status(f"Incorreto. O componente '{self.componente_selecionado}' não pertence a esse slot.", "erro")
    
    def _montar_tela_dividir(self, parent):
        self._set_status("PA09CD: Divida cada chave em duas metades."); self.proxima_etapa = 'CALC_A'
        container = tk.Frame(parent, bg=self.cor_fundo_base); container.pack(pady=20)
        # ... (código deste método permanece o mesmo da versão anterior) ...
        tk.Label(container, text=f"Chave x: {self.valores['x']}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=0, column=0, columnspan=4, pady=(0, 5))
        tk.Label(container, text="x1 =", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=1, column=0, sticky='e', padx=5)
        self.widgets['entry_x1'] = ttk.Entry(container, width=5, font=self.binary_font_obj, justify='center'); self.widgets['entry_x1'].grid(row=1, column=1)
        tk.Label(container, text="x0 =", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=1, column=2, sticky='e', padx=5)
        self.widgets['entry_x0'] = ttk.Entry(container, width=5, font=self.binary_font_obj, justify='center'); self.widgets['entry_x0'].grid(row=1, column=3)
        tk.Label(container, text=f"Chave y: {self.valores['y']}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=0, columnspan=4, pady=(20, 5))
        tk.Label(container, text="y1 =", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=3, column=0, sticky='e', padx=5)
        self.widgets['entry_y1'] = ttk.Entry(container, width=5, font=self.binary_font_obj, justify='center'); self.widgets['entry_y1'].grid(row=3, column=1)
        tk.Label(container, text="y0 =", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=3, column=2, sticky='e', padx=5)
        self.widgets['entry_y0'] = ttk.Entry(container, width=5, font=self.binary_font_obj, justify='center'); self.widgets['entry_y0'].grid(row=3, column=3)
        ttk.Button(parent, text="Confirmar Divisão", command=self._validar_dividir).pack(pady=25)

    def _validar_dividir(self):
        corretos = {'x1': self.valores['x'][:-self.n2], 'x0': self.valores['x'][-self.n2:],'y1': self.valores['y'][:-self.n2], 'y0': self.valores['y'][-self.n2:]}
        jogador = {'x1': self.widgets['entry_x1'].get().strip(), 'x0': self.widgets['entry_x0'].get().strip(), 'y1': self.widgets['entry_y1'].get().strip(), 'y0': self.widgets['entry_y0'].get().strip()}
        if all(jogador[k] == v for k, v in corretos.items()):
            self._set_status("Divisão correta!", "sucesso"); self.valores.update(corretos); self.root.after(1000, lambda: self.mudar_etapa(self.proxima_etapa))
        else: self._set_status("Divisão incorreta. Verifique os valores.", "erro")

    def _montar_calc_vertical(self, parent, var_resultado, title, n1, op, n2, proxima, dica):
        self._set_status(f"PA09CD: {dica}"); self.proxima_etapa = proxima
        frame = tk.Frame(parent, bg=self.cor_fundo_base); frame.pack(pady=20)
        tk.Label(frame, text=title, font=self.narrative_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=0, column=0, columnspan=2, pady=(0,10))
        tk.Label(frame, text=n1, font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=1, column=1, sticky='e')
        tk.Label(frame, text=op, font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=0, sticky='e', padx=(0,5))
        tk.Label(frame, text=n2, font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=1, sticky='e')
        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        self.widgets['entry_resultado'] = ttk.Entry(frame, width=10, justify='right', font=self.binary_font_obj); self.widgets['entry_resultado'].grid(row=4, column=1, sticky='e')
        ttk.Button(parent, text="Confirmar Cálculo", command=lambda: self._validar_calc_generico(var_resultado)).pack(pady=20)

    def _validar_calc_generico(self, var_resultado):
        jogador = self.widgets['entry_resultado'].get().strip()
        correto = bin(self.valores[var_resultado])[2:]
        if jogador == correto:
            self._set_status("Cálculo correto!", "sucesso"); self.root.after(1000, lambda: self.mudar_etapa(self.proxima_etapa))
        else: self._set_status(f"Incorreto. A resposta correta é {correto}", "erro")

    def _montar_tela_calc_a(self, parent):
        self.valores['A'] = int(self.valores['x1'], 2) * int(self.valores['y1'], 2)
        self._montar_calc_vertical(parent, 'A', "Cálculo de A: (x1 * y1)", self.valores['x1'], 'x', self.valores['y1'], 'CALC_C', "Calcule o produto das partes mais significativas.")

    def _montar_tela_calc_c(self, parent):
        self.valores['C'] = int(self.valores['x0'], 2) * int(self.valores['y0'], 2)
        self._montar_calc_vertical(parent, 'C', "Cálculo de C: (x0 * y0)", self.valores['x0'], 'x', self.valores['y0'], 'CALC_SOMAS', "Agora, o produto das partes menos significativas.")

    def _montar_tela_calc_somas(self, parent):
        self._set_status("PA09CD: Prepare para o truque. Some as partes.")
        self.proxima_etapa = 'CALC_B'
        self.valores['soma_x'] = int(self.valores['x1'], 2) + int(self.valores['x0'], 2)
        self.valores['soma_y'] = int(self.valores['y1'], 2) + int(self.valores['y0'], 2)
        
        frame = tk.Frame(parent, bg=self.cor_fundo_base); frame.pack(pady=20)
        
        # --- Frame para a Soma de X ---
        frame_x = tk.Frame(frame, bg=self.cor_fundo_base)
        frame_x.grid(row=0, column=0, padx=20)
        
        # Usa um f-string para mostrar os números a serem somados
        tk.Label(frame_x, text=f"{self.valores['x1']} + {self.valores['x0']} = ?", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=(0,5))
        self.widgets['entry_soma_x'] = ttk.Entry(frame_x, width=8, justify='center', font=self.binary_font_obj)
        self.widgets['entry_soma_x'].pack()

        # --- Frame para a Soma de Y ---
        frame_y = tk.Frame(frame, bg=self.cor_fundo_base)
        frame_y.grid(row=0, column=1, padx=20)

        # Usa um f-string para mostrar os números a serem somados
        tk.Label(frame_y, text=f"{self.valores['y1']} + {self.valores['y0']} = ?", font=self.binary_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=(0,5))
        self.widgets['entry_soma_y'] = ttk.Entry(frame_y, width=8, justify='center', font=self.binary_font_obj)
        self.widgets['entry_soma_y'].pack()
        
        # Botão de confirmação
        ttk.Button(parent, text="Confirmar Somas", command=self._validar_somas).pack(pady=20)

    def _validar_somas(self):
        soma_x_c = bin(self.valores['soma_x'])[2:]; soma_y_c = bin(self.valores['soma_y'])[2:]
        if self.widgets['entry_soma_x'].get().strip() == soma_x_c and self.widgets['entry_soma_y'].get().strip() == soma_y_c:
            self._set_status("Somas corretas!", "sucesso"); self.root.after(1000, lambda: self.mudar_etapa(self.proxima_etapa))
        else: self._set_status("Uma ou mais somas estão incorretas.", "erro")

    def _montar_tela_calc_b(self, parent):
        self.valores['B'] = self.valores['soma_x'] * self.valores['soma_y']
        self._montar_calc_vertical(parent, 'B', "Cálculo de B: (soma_x * soma_y)", bin(self.valores['soma_x'])[2:], 'x', bin(self.valores['soma_y'])[2:], 'ISOLAR_MEIO', "Calcule o produto das somas.")

    def _montar_montagem_generica(self, parent, slots, proxima, dica):
        self._set_status(f"PA09CD: {dica}"); self.proxima_etapa = proxima
        bancada = tk.Frame(parent, bg="#202020", relief=tk.RIDGE, bd=2); bancada.pack(pady=10, fill=tk.X, ipady=10)
        tk.Label(bancada, text="BANCADA DE COMPONENTES", font=self.binary_font_small, fg=self.cor_info, bg="#202020").pack()
        comp_frame = tk.Frame(bancada, bg="#202020"); comp_frame.pack()
        
        componentes_shuffled = list(slots.keys()); random.shuffle(componentes_shuffled)
        for i, comp_nome in enumerate(componentes_shuffled):
            w = tk.Label(comp_frame, text=comp_nome, font=self.binary_font_obj, bg=self.cor_componente, fg="white", relief=tk.RAISED, bd=2, padx=10, pady=5)
            w.bind("<Button-1>", lambda e, name=comp_nome: self._selecionar_componente(name)); w.grid(row=0, column=i, padx=15, pady=10)
            self.widgets[comp_nome] = w

        formula_frame = tk.Frame(parent, bg=self.cor_fundo_base); formula_frame.pack(pady=20)
        for i, (slot_nome, slot_label) in enumerate(slots.items()):
            slot_frame = tk.Frame(formula_frame, width=150, height=60, bg=self.cor_slot, relief=tk.SUNKEN, bd=2)
            slot_frame.grid(row=0, column=i*2, padx=5); slot_frame.pack_propagate(False)
            slot_frame.bind("<Button-1>", lambda e, name=slot_nome: self._colocar_componente(name))
            
            label = tk.Label(slot_frame, text="?", font=self.binary_font_obj, bg=self.cor_slot, fg="#555")
            label.pack(expand=True); label.bind("<Button-1>", lambda e, name=slot_nome: self._colocar_componente(name))
            self.widgets[f"slot_{slot_nome}_label"] = label
            
            if slot_label: tk.Label(formula_frame, text=slot_label, font=self.header_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=0, column=i*2+1)
            if "<<" in slot_label: tk.Label(formula_frame, text=slot_label, font=self.narrative_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).grid(row=1, column=i*2)


    def _montar_tela_isolar_meio(self, parent):
        self.valores['TermoMeio'] = self.valores['B'] - self.valores['A'] - self.valores['C']
        slots = {'B':'-', 'A':'-', 'C':''}
        self._montar_montagem_generica(parent, slots, 'COMBINAR', "Monte a fórmula B - A - C.")

    def _montar_tela_combinar(self, parent):
        slots = {'A': f"<< {self.n}", 'TermoMeio': f"<< {self.n2}", 'C': ''}
        self._montar_montagem_generica(parent, slots, 'CALC_FINAL', "Alinhe os componentes nos deslocadores corretos!")

    def _montar_tela_calc_final(self, parent):
        self._set_status("PA09CD: Some os termos alinhados para encontrar a chave secreta!")
        a_shifted = self.valores['A'] << (2 * self.n2); tm_shifted = self.valores['TermoMeio'] << self.n2; c = self.valores['C']
        
        frame = tk.Frame(parent, bg=self.cor_fundo_base); frame.pack(pady=20)
        max_len = len(bin(self.valores['resultado_final'])[2:]) + 1
        
        tk.Label(frame, text=bin(a_shifted)[2:].zfill(max_len), font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=0, column=1, sticky='e')
        tk.Label(frame, text="+", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=1, column=0, sticky='e', padx=5)
        tk.Label(frame, text=bin(tm_shifted)[2:].zfill(max_len), font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=1, column=1, sticky='e')
        tk.Label(frame, text="+", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=0, sticky='e', padx=5)
        tk.Label(frame, text=bin(c)[2:].zfill(max_len), font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=1, sticky='e')
        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        self.widgets['entry_final'] = ttk.Entry(frame, width=max_len, justify='right', font=self.binary_font_obj); self.widgets['entry_final'].grid(row=4, column=1, sticky='e')

        ttk.Button(parent, text="DECODIFICAR!", command=self._validar_final, style="Accent.Dark.TButton").pack(pady=20)
        
    def _validar_final(self):
        jogador = self.widgets['entry_final'].get().strip()
        correto = bin(self.valores['resultado_final'])[2:]
        if jogador == correto: self._mostrar_tela_sucesso()
        else: self._set_status(f"Chave final incorreta. A resposta certa era {correto}. Tente recalcular.", "erro")
            
    def _mostrar_tela_sucesso(self):
        content_frame = self.widgets['content_frame']
        self._limpar_widgets_do_frame(content_frame)
        
        tk.Label(content_frame, text="TRANSMISSÃO DECODIFICADA!", font=self.header_font_obj, fg=self.cor_sucesso, bg=self.cor_fundo_base).pack(pady=20)
        resultado_str = bin(self.valores['resultado_final'])[2:]
        tk.Label(content_frame, text=f"Chave Final: {resultado_str}", font=self.binary_font_obj, fg="white", bg=self.cor_fundo_base).pack(pady=10)
        pontos = 500
        self.game_manager.add_score(pontos)
        mensagem = f"A mensagem revela os planos de movimentação da frota do Moff Gideon! Graças a você, a Aliança pode preparar uma emboscada.\n\nVocê ganhou {pontos} pontos de influência."
        tk.Label(content_frame, text=mensagem, font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base, wraplength=500).pack(pady=20)
        
        # NOVO: Botão para o jogador controlar a saída
        ttk.Button(content_frame, text="Concluir Missão", command=lambda: self.game_manager.mission_completed("MissaoDC4"), style="Accent.Dark.TButton").pack(pady=20)

    def retry_mission(self):
        self.game_manager.set_game_state("START_MISSION_DC_4")