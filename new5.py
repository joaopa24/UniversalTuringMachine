class MaquinaDeTuring:
    def __init__(self):
        # Inicializa as fitas com listas vazias
        self.fita1 = []
        self.fita2 = []
        self.fita3 = []
        
        # Inicializa as cabeças de leitura
        self.cabeca_fita1 = 0
        self.cabeca_fita2 = 0
        self.cabeca_fita3 = 0
        
        # Inicializa a tabela de transições
        self.transicoes = {
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", "B"): ("q1", "1", "R"),
            ("q1", "1"): ("q1", "1", "R"),
            ("q4", "0"): ("q2", "B", "L")
        }

        # Processa as transições e adiciona na fita 1
        self.processar_transicoes()

    def codificar_estado(self, estado):
        """Codifica um estado no formato dinâmico baseado em 'qX'"""
        if estado.startswith('q'):
            try:
                numero_estado = int(estado[1:])  # Remove o 'q' inicial e converte para inteiro
                return '1' * (numero_estado + 1)  # Codifica como '1' * (numero_estado + 1)
            except ValueError:
                return '0'  # Caso não consiga converter para inteiro, retorna '0'
        return '0'  # Default caso o estado não seja reconhecido

    def processar_transicoes(self):
        # Adiciona '000' no início como um único componente
        self.fita1.append('000')

        transicoes = list(self.transicoes.items())
        num_transicoes = len(transicoes)

        for i, ((estado_atual, simbolo_lido), (estado_destino, simbolo_substituto, direcao)) in enumerate(transicoes):
            # Codifica o estado atual
            self.fita1.append(self.codificar_estado(estado_atual))
            # Adiciona separador
            self.fita1.append('0')

            # Codifica o símbolo lido
            if simbolo_lido == '0':
                self.fita1.append('1')
            elif simbolo_lido == '1':
                self.fita1.append('11')
            elif simbolo_lido == 'B':
                self.fita1.append('111')
            # Adiciona separador
            self.fita1.append('0')

            # Codifica o estado destino
            self.fita1.append(self.codificar_estado(estado_destino))
            # Adiciona separador
            self.fita1.append('0')

            # Codifica o símbolo substituto
            if simbolo_substituto == '0':
                self.fita1.append('1')
            elif simbolo_substituto == '1':
                self.fita1.append('11')
            elif simbolo_substituto == 'B':
                self.fita1.append('111')
            # Adiciona separador
            self.fita1.append('0')

            # Codifica a direção
            if direcao == 'L':
                self.fita1.append('1')
            elif direcao == 'R':
                self.fita1.append('11')

            # Adiciona separador de transições, exceto após a última transição
            if i < num_transicoes - 1:
                self.fita1.append('00')

        # Adiciona '000' no final como um único componente
        self.fita1.append('000')

    def mostrar_componentes(self):
        # Imprime cada componente da fita1
        for componente in self.fita1:
            print(componente)

    def mostrar_estado(self):
        # Exibe o estado atual das fitas e das cabeças
        print("Fita 1:", ''.join(self.fita1))
        print("Cabeça Fita 1:", self.cabeca_fita1)
        print("Fita 2:", ''.join(self.fita2))
        print("Cabeça Fita 2:", self.cabeca_fita2)
        print("Fita 3:", ''.join(self.fita3))
        print("Cabeça Fita 3:", self.cabeca_fita3)

# Exemplo de uso
maquina = MaquinaDeTuring()
maquina.mostrar_componentes()  # Imprime cada componente da fita1
maquina.mostrar_estado()
