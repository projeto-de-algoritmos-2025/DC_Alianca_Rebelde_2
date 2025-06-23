<h2 align="center">Star Wars: Aliança Rebelde 2 - A volta dos desafios</h2>

<div align="center">
    Figura 1: Aliança Rebelde
    <br>
    <img src="https://raw.githubusercontent.com/projeto-de-algoritmos-2025/Alianca_Rebelde-Algoritmos_Ambiciosos/refs/heads/main/Alianca_Rebelde/alianca_simbolo.png" width="500">
    <br>
    <br>
</div>

<h2 align="center">É dividindo que se consquista!</h2>

<strong>"Aliança Rebelde 2 - A volta dos desafios"</strong> é um jogo de estratégia e puzzle narrativo, que se passa depois do jogo "Aliança Rebelde-  Operações Críticas". Nele o jogador assume o papel de um(a) Coordenador(a) de Operações da Aliança Rebelde. Com uma atmosfera inspirada na seriedade e tensão de narrativas como "Andor" e "Rogue One", o jogo desafia o jogador a aplicar os algoritmos de dividir e conquistar para resolver problemas complexos em diversas missões. Cada nível é uma etapa crucial na campanha contra o Império, exigindo lógica e precisão.

Cada missão foi pensada para explorar não só os fundamentos dos algoritmos, mas também como eles podem ser aplicados em situações críticas, onde o tempo, a precisão e a estratégia são vitais.

Que a Força esteja com você!

**Número da Lista**: 3
**Conteúdo da Disciplina**: Dividir e conquistar <br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1039573 | Larissa Stéfane Barboza Santos |
| 21/1029497  | Mylena Angélica Silva Farias  |

## Sobre 

Esse repositório apresenta o jogo Aliança Rebelde 2 - A volta dos desafioss, uma aventura textual interativa onde você assume o papel de um(a) estrategista crucial para a Aliança Rebelde. 

Para mais detalhes sobre a história, os personagens, os algoritmos abordados e a mecânica de jogo, acesse a documentação em [descrição](/Descricao.md)

### Missões do Jogo

- Missão 1: O Enigma da Mediana - Mediana das Medianas
- Missão 2: Dicas do mestre - Contagem de inversões 
- Missão 3: Duelo no Hiperespaço - Par de Pontos Mais Próximos
- Missão 4:Quebra de Códigos - Multiplicação de Karatsuba
- Missão 5: Ataque Coordenado em Coruscant - Multiplicação de Matrizes com Strassen   


Para ter acesso aos códigos clique em [Aliança Rebelde 2]()

## Link do vídeo


## Screenshots

Abaixo estão os screenshots do projeto



## Instalação 

### Para mais detalhes:

Para mais detalhes e passo a passo da execução, acesse a documentação em [Aliança Rebelde 2](INCLUIR LINK)

#### 1. Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

* **Python 3:** O jogo foi desenvolvido usando Python 3 (versão 3.7 ou superior é recomendada). Você pode baixar o Python em [python.org](https://www.python.org/downloads/).
    * Durante a instalação no Windows, marque a opção "Add Python to PATH" ou similar.
* **Git:** Necessário para clonar o repositório do jogo. Você pode baixar o Git em [git-scm.com](https://git-scm.com/downloads).
* **Tkinter:** Esta é a biblioteca gráfica que o jogo utiliza.
    * **Windows e macOS:** Geralmente, o Tkinter já vem instalado com o Python.
    * **Linux:** Se não estiver instalado, você pode instalá-lo usando o gerenciador de pacotes da sua distribuição. Por exemplo, em sistemas baseados em Debian/Ubuntu:
        ```bash
        sudo apt-get update
        sudo apt-get install python3-tk
        ```

#### 2. Configuração do Jogo

Siga os passos abaixo para configurar o jogo no seu computador:

##### a. Clonar o Repositório:

Abra o seu terminal ou prompt de comando e navegue até o diretório onde você deseja salvar o jogo. Em seguida, clone o repositório do GitHub com o seguinte comando (substitua `SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO` pelo link correto do seu projeto):

```bash
git clone [https://github.com/SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO.git)
```

sso criará uma pasta com o nome do repositório contendo todos os arquivos do jogo. Acesse essa pasta:

```bash
cd NOME_DO_REPOSITORIO
```

##### b. (Opcional, mas Recomendado) Criar um Ambiente Virtual:

Usar um ambiente virtual é uma boa prática para isolar as dependências do projeto.

```bash
python3 -m venv venv_alianca_rebelde2
```

Ative o ambiente virtual:

#### No Windows:

```bash.\venv_alianca_rebelde2\Scripts\activate
```

#### No macOS e Linux:

```bash
source venv_alianca_rebelde2/bin/activate
```

Você saberá que o ambiente virtual está ativo porque o nome dele aparecerá no início do seu prompt do terminal.

#### 3. Estrutura de Pastas Esperada
Para que o jogo funcione corretamente, especialmente o carregamento de imagens e módulos, ele espera a seguinte estrutura de pastas dentro do diretório principal do projeto:

      NOME_DO_REPOSITORIO/
      ├── main.py                     # Arquivo principal para executar o jogo
      ├── algoritmos/                 # Pasta para os algoritmos
      │   ├── __init__.py
      │   ├── contagem_de_inversao.py
      │   ├── karatsuba.py
      │   ├── mediana_da_mediana.py
      │   ├── par_de_pontos.py
      │   ├── strassen.py
      |
      ├── missoes/                    # Pasta para as missões e minigames
      │   ├── __init__.py
      │   ├── missao1.py
      │   ├── missao2.py
      │   ├── missao3.py
      │   ├── missao4.py
      │   ├── missao5.py
      │   
      ├── assets/                     # Pasta para recursos gráficos e sonoros
      │   └── images/
      │       └── Alianca_Rebelde.png # Imagem do símbolo da Aliança
      │       └── fundo_espacial.png  # Exemplo de imagem de fundo para a janela
      └── README.md                   # Este arquivo de manual


#### 4. Como Rodar o Jogo

Depois de clonar o repositório e (opcionalmente) ativar o ambiente virtual:

Navegue pelo terminal até a pasta raiz do projeto (onde o arquivo main.py está localizado).

Execute o jogo com o seguinte comando:

```bash
python3 main.py
```
(Ou python main.py dependendo da sua configuração do Python).

Isso deve iniciar a janela do jogo "Aliança Rebelde - Operações Críticas".

**Linguagem**: python<br>
