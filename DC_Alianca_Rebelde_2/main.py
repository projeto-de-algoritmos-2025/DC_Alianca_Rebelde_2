# main.py (Versão 2.3 - Final com Todas as Imagens e Textos Completos)
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont, PhotoImage
import random 
import os 
import sys

# --- Importações das missões (Comente/descomente conforme desenvolve) ---
try:
    from missoes_dc.missao_dc_1 import MissaoDC1
    from missoes_dc.missao_dc_2 import MissaoDC2 
    from missoes_dc.missao_dc_3 import MissaoDC3
    from missoes_dc.missao_dc_4 import MissaoDC4
except ImportError as e:    
    print(f"ALERTA DE IMPORTAÇÃO DE MÓDULO: {e}")

class GameManager:
    def __init__(self, root_tk):
        self.root = root_tk
        self.root.title("Aliança Rebelde 2 - A Volta dos Desafios") 
        self.root.configure(bg="black") 

        try:
            largura_tela = self.root.winfo_screenwidth()
            altura_tela = self.root.winfo_screenheight()
            self.root.geometry(f"{largura_tela}x{altura_tela}+0+0")
        except tk.TclError:
            self.root.state('zoomed') # Fallback para Windows/outros sistemas

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # --- Carregar TODAS as Imagens ---
        self.imagens = {} # Usaremos um dicionário para organizar as imagens
        nomes_imagens = [
            "alianca_simbolo.png", "Cena1.png", "Cena2.png", 
            "Cena3.png", "Cena4.png", "Cena5.png", "Cena6.png"
        ]
        for nome_img in nomes_imagens:
            try:
                caminho_img = os.path.join(self.script_dir, nome_img)
                if os.path.exists(caminho_img):
                    self.imagens[nome_img] = PhotoImage(file=caminho_img)
                    print(f"DEBUG: Imagem '{nome_img}' carregada.")
                else:
                    print(f"AVISO: Imagem '{nome_img}' NÃO ENCONTRADA.")
                    self.imagens[nome_img] = None # Define como None se não encontrar
            except Exception as e_img:
                print(f"AVISO: Erro ao carregar '{nome_img}': {e_img}")
                self.imagens[nome_img] = None

        # --- Cores e Fontes ---
        self.bg_color_dark = "black"
        self.fg_color_light = "white"
        self.title_color_accent = "orangered" 
        self.default_font_family = "Arial" 
        try:
            self.header_font_obj = tkFont.Font(family=self.default_font_family, size=20, weight="bold")
            self.narrative_font_obj = tkFont.Font(family=self.default_font_family, size=12)
            self.button_font_obj = tkFont.Font(family=self.default_font_family, size=11, weight="bold")
            self.small_bold_font_obj = tkFont.Font(family=self.default_font_family, size=10, weight="bold")
            self.points_font_obj = tkFont.Font(family=self.default_font_family, size=12, weight="bold", slant="italic")
        except tk.TclError: 
            print("Aviso: Fontes tkFont.Font não configuradas. Usando fallback.")
            self.header_font_obj = ("Arial", 20, "bold")
            self.narrative_font_obj = ("Arial", 12)
            self.button_font_obj = ("Arial", 11, "bold")
            self.small_bold_font_obj = ("Arial", 10, "bold")
            self.points_font_obj = ("Arial", 12, "bold", "italic")
        
        # --- Estilo ttk ---
        style = ttk.Style()
        try: style.theme_use('clam')
        except tk.TclError: pass
        style.configure("Black.TFrame", background=self.bg_color_dark)
        style.configure("Points.TLabel", background=self.bg_color_dark, foreground="#87CEFA", font=self.points_font_obj)
        style.configure("Accent.Dark.TButton", font=self.button_font_obj, foreground="white", background="#0078D7", padding=10)
        style.map("Accent.Dark.TButton", background=[('active', '#005A9E')])
        style.configure("Dark.TButton", font=self.button_font_obj, foreground="white", background="#333333", padding=5)
        style.map("Dark.TButton", background=[('active', '#444444')])

        self.player_score = 0 
        self.current_mission_obj = None 
        self.content_frame = None 
        self.game_state = "INTRO_V2_A" 
        self.update_display()
        
    def _clear_content_frame(self):
        if self.content_frame: self.content_frame.destroy()
        self.content_frame = ttk.Frame(self.root, padding="20", style="Black.TFrame") 
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def _display_text_screen(self, title_text, narrative_text_lines, button_text, 
                             next_state_or_command, button_style="Dark.TButton", 
                             image_to_display=None): 
        self._clear_content_frame()
        title_label = tk.Label(self.content_frame, text=title_text, font=self.header_font_obj, anchor="center", bg=self.bg_color_dark, fg=self.title_color_accent, pady=5) 
        title_label.pack(pady=(10, 15), fill=tk.X)
        text_widget = tk.Text(self.content_frame, wrap=tk.WORD, height=10, relief=tk.FLAT, background=self.bg_color_dark, foreground=self.fg_color_light, insertbackground=self.fg_color_light, font=self.narrative_font_obj, padx=10, pady=10, borderwidth=0, highlightthickness=0)
        text_widget.insert(tk.END, "\n\n".join(narrative_text_lines))
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=40, pady=5)
        if image_to_display: 
            imagem_label = tk.Label(self.content_frame, image=image_to_display, bg=self.bg_color_dark) 
            imagem_label.pack(pady=(10, 5))
        if isinstance(next_state_or_command, str): command_to_run = lambda: self.set_game_state(next_state_or_command)
        else: command_to_run = next_state_or_command
        button_container = ttk.Frame(self.content_frame, style="Black.TFrame")
        pady_button = (5 if image_to_display else 15, 10) 
        button_container.pack(pady=pady_button, side=tk.BOTTOM, anchor="s")
        actual_button_style = "Accent.Dark.TButton" if button_style == "Accent.TButton" else "Dark.TButton"
        ttk.Button(button_container, text=button_text, command=command_to_run, style=actual_button_style).pack(pady=5)

    def update_display(self):
        self._clear_content_frame()

        # --- INTRODUÇÃO PARA O JOGO 2 (TEXTOS COMPLETOS) ---
        if self.game_state == "INTRO_V2_A":
            narrativa = ["Comandante RZ-479, alguns meses se passaram desde suas vitórias decisivas que desestabilizaram as operações imperiais em múltiplos setores. Sua reputação como um(a) estrategista de elite se espalhou como um incêndio pela galáxia.", "Você se tornou um símbolo de esperança para a Aliança e uma pedra no sapato do Império."]
            self._display_text_screen("A Guerra Não Para", narrativa, "Continuar...", "INTRO_V2_B", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("Cena1.png"))
        elif self.game_state == "INTRO_V2_B":
            narrativa = ["Mas o Império, ferido, não está derrotado. Eles se adaptaram. Seus métodos se tornaram mais complexos, suas táticas mais intrincadas. Problemas que antes podiam ser resolvidos com uma abordagem direta e 'gananciosa' agora exigem uma nova forma de pensar.", "Fulcrum entra em contato. A voz dele, sempre pragmática, agora carrega um novo peso..."]
            self._display_text_screen("A Adaptação do Inimigo", narrativa, "Ouvir a transmissão...", "INTRO_V2_C", image_to_display=self.imagens.get("Cena2.png"))
        elif self.game_state == "INTRO_V2_C":
            narrativa = ["Fulcrum: \"Comandante, a complexidade dos desafios à nossa frente aumentou exponencialmente. As frotas imperiais se movem em padrões que não conseguimos decifrar, e seus códigos de comunicação se tornaram quase impenetráveis.\"", "\"Para vencê-los, precisaremos de uma nova doutrina: **Dividir para Conquistar**. Precisamos quebrar problemas massivos em partes menores e gerenciáveis. Sua expertise será testada como nunca antes.\""]
            self._display_text_screen("Nova Doutrina: Dividir e Conquistar", narrativa, "Aceito o desafio, Fulcrum. Qual a primeira diretriz?", "YODA_INTRO_A", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("Cena2.png"))
        elif self.game_state == "YODA_INTRO_A":
            narrativa = ["A transmissão de Fulcrum termina, deixando um silêncio pesado na cabine. 'Dividir para Conquistar'... a doutrina é lógica, mas a escala do desafio parece esmagadora.", "Você fecha os olhos por um momento, buscando clareza e centrando seus pensamentos..."]
            self._display_text_screen("Um Eco na Força", narrativa, "...", "YODA_INTRO_B", image_to_display=self.imagens.get("Cena3.png"))
        elif self.game_state == "YODA_INTRO_B":
            narrativa = ["...E no silêncio da sua mente, uma voz antiga, sábia e familiar ecoa, uma voz que você não esperava ouvir. Não é através do comunicador, mas dentro de você.", "\"Grande, o Império é. Como uma montanha, imponente ele parece.\""]
            self._display_text_screen("Palavras de um Mestre", narrativa, "Ouvir com atenção...", "YODA_INTRO_C", image_to_display=self.imagens.get("Cena4.png"))
        elif self.game_state == "YODA_INTRO_C":
            narrativa = ["\"Mas a montanha, em pequenas pedras se desfaz. O grande problema, em problemas menores você deve ver. Em cada parte, uma fraqueza encontrar. Conquistar a parte, e a montanha cairá.\"", "\"O caminho que você busca, este é. Confie na Força... e na sua mente.\""]
            self._display_text_screen("Sabedoria Ancestral", narrativa, "Estou pronta(o). Iniciar Missão 1", "START_MISSION_DC_1", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("Cena4.png"))
        
        # --- FLUXO DAS NOVAS MISSÕES ---
        elif self.game_state == "START_MISSION_DC_1":
            if 'MissaoDC1' in globals():
                self._clear_content_frame()
                self.current_mission_obj = MissaoDC1(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe MissaoDC1 não foi carregada.")
        elif self.game_state == "MISSION_DC_1_SUCCESS":
            dialogo = ["Fulcrum: \"Análise impressionante, Comandante. Você encontrou o ponto nevrálgico nos dados imperiais. Isso nos leva diretamente à nossa próxima operação...\""]
            self._display_text_screen("Análise Concluída", dialogo, "Aguardando ordens.", "START_MISSION_DC_2", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        elif self.game_state == "START_MISSION_DC_2":
            if 'MissaoDC2' in globals():
                self._clear_content_frame()
                self.current_mission_obj = MissaoDC2(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe MissaoDC2 não foi carregada.")
        elif self.game_state == "MISSION_DC_2_SUCCESS":
            self._display_text_screen("Operação Concluída", ["Fulcrum: \"Excelente. Prepare-se para o próximo desafio.\""], "Avançar para Missão 3", "START_MISSION_DC_3", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        elif self.game_state == "START_MISSION_DC_3":
            if 'MissaoDC3' in globals():
                self._clear_content_frame()
                self.current_mission_obj = MissaoDC3(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe MissaoDC3 não foi carregada.")
        elif self.game_state == "MISSION_DC_3_SUCCESS":
             dialogo = ["Fulcrum: \"Mais um sucesso para a Aliança. Continue assim.\""]
             self._display_text_screen("Operação Concluída", dialogo, "Avançar para Missão 4", "START_MISSION_DC_4", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        
        elif self.game_state == "START_MISSION_DC_4":
            if 'MissaoDC4' in globals():
                self._clear_content_frame()
                self.current_mission_obj = MissaoDC4(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe MissaoDC4 não foi carregada.")
        elif self.game_state == "MISSION_DC_4_SUCCESS":
             dialogo = ["Fulcrum: \"Inteligência valiosa, Comandante. O Império não saberá o que os atingiu. Sua habilidade com criptografia é um trunfo para a Aliança.\""]
             self._display_text_screen("Transmissão Decodificada", dialogo, "Avançar para a Próxima Missão", "START_MISSION_DC_5", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        
        elif self.game_state == "START_MISSION_DC_5":
            narrativa = ["Missão 5", "\n(Esta missão ainda está em desenvolvimento.)"]
            self._display_text_screen("MISSÃO 5 EM DESENVOLVIMENTO", narrativa, "Finalizar Operações", "ALL_MISSIONS_COMPLETED_V2")
        elif self.game_state == "ALL_MISSIONS_COMPLETED_V2":
             self._display_text_screen("Vitória Através da Divisão", ["Suas estratégias de Dividir e Conquistar foram decisivas para a próxima fase da guerra. A luta continua, mas hoje, a Aliança está mais forte graças a você."], "A Rebelião Viverá para Lutar Mais um Dia (Sair)", self.root.quit, button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        
        else: 
            self._clear_content_frame()
            tk.Label(self.content_frame, text=f"Estado de jogo desconhecido: {self.game_state}", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=20)

    def add_score(self, points):
        self.player_score += points
        print(f"Pontos de Influência: {points}. Total: {self.player_score}")

    def set_game_state(self, new_state):
        print(f"Mudando estado de '{self.game_state}' para: {new_state}") 
        self.game_state = new_state
        self.root.after_idle(self.update_display)

    def mission_completed(self, mission_id):
        print(f"GameManager: Missão {mission_id} concluída.") 
        if mission_id == "MissaoDC1": self.set_game_state("MISSION_DC_1_SUCCESS") 
        elif mission_id == "MissaoDC2": self.set_game_state("MISSION_DC_2_SUCCESS")
        elif mission_id == "MissaoDC3": self.set_game_state("MISSION_DC_3_SUCCESS")
        elif mission_id == "MissaoDC4": self.set_game_state("MISSION_DC_4_SUCCESS")
        elif mission_id == "MissaoDC5": self.set_game_state("ALL_MISSIONS_COMPLETED_V2")
    
    def mission_failed_options(self, mission_obj, msg1, msg2):
        self._clear_content_frame()
        tk.Label(self.content_frame, text="Falha na Missão!", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=10)
        tk.Label(self.content_frame, text=random.choice([msg1, msg2]), font=self.narrative_font_obj, bg=self.bg_color_dark, fg=self.fg_color_light, wraplength=700).pack(pady=15, padx=30)
        button_frame = ttk.Frame(self.content_frame, style="Black.TFrame")
        button_frame.pack(pady=20)
        if mission_obj and hasattr(mission_obj, 'retry_mission'):
            ttk.Button(button_frame, text="Tentar Novamente", command=mission_obj.retry_mission, style="Accent.Dark.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Abandonar Operação", command=self.root.quit, style="Dark.TButton").pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = None 
    try:
        root = tk.Tk()
        app = GameManager(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro fatal ao iniciar a aplicação: {e}")