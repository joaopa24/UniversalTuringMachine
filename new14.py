class MaquinaDeTuring:
    def __init__(self, estado_inicial, estados_finais, palavra):
        self.fita1 = []
        self.fita2 = []
        self.fita3 = list(palavra)
        self.cabeca_fita1 = 0
        self.cabeca_fita2 = 0
        self.cabeca_fita3 = 0
        self.transicoes = {
            ("q0", "0"): ("q0", "0", "R"),
            ("q0", "B"): ("q1", "B", "R"),
            ("q1", "1"): ("q2", "1", "R"),
            ("q2", "1"): ("q2", "1", "R"),
        }
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.estado_atual = estado_inicial
        self.fita2.append(self.codificar_estado(estado_inicial))
        self.processar_transicoes()

    def codificar_estado(self, estado):
        if estado.startswith('q'):
            try:
                numero_estado = int(estado[1:])
                return '1' * (numero_estado + 1)
            except ValueError:
                return '0'
        return '0'

    def processar_transicoes(self):
        self.fita1.append('000')
        transicoes = list(self.transicoes.items())
        num_transicoes = len(transicoes)

        for i, ((estado_atual, simbolo_lido), (estado_destino, simbolo_substituto, direcao)) in enumerate(transicoes):
            self.fita1.append(self.codificar_estado(estado_atual))
            self.fita1.append('0')

            if simbolo_lido == '0':
                self.fita1.append('1')
            elif simbolo_lido == '1':
                self.fita1.append('11')
            elif simbolo_lido == 'B':
                self.fita1.append('111')
            self.fita1.append('0')

            self.fita1.append(self.codificar_estado(estado_destino))
            self.fita1.append('0')

            if simbolo_substituto == '0':
                self.fita1.append('1')
            elif simbolo_substituto == '1':
                self.fita1.append('11')
            elif simbolo_substituto == 'B':
                self.fita1.append('111')
            self.fita1.append('0')

            if direcao == 'L':
                self.fita1.append('1')
            elif direcao == 'R':
                self.fita1.append('11')

            if i < num_transicoes - 1:
                self.fita1.append('00')

        self.fita1.append('000')

    def executar_passo(self):
        simbolo_atual = self.fita3[self.cabeca_fita3] if self.cabeca_fita3 < len(self.fita3) else 'B'
        estado_codificado = self.codificar_estado(self.estado_atual)
        simbolo_codificado = '11' if simbolo_atual == '1' else '1' if simbolo_atual == '0' else '111'

        i = 1  # Começa após o '000' inicial
        while i < len(self.fita1) - 1:
            transicao_atual = self.fita1[i:i+10]
            if (self.fita1[i] == estado_codificado and 
                self.fita1[i+2] == simbolo_codificado):
                novo_estado_codificado = self.fita1[i+4]
                novo_simbolo_codificado = self.fita1[i+6]
                direcao = self.fita1[i+8]

                self.fita2 = [novo_estado_codificado]

                if novo_simbolo_codificado == '1':
                    self.fita3[self.cabeca_fita3] = '0'
                elif novo_simbolo_codificado == '11':
                    self.fita3[self.cabeca_fita3] = '1'
                elif novo_simbolo_codificado == '111':
                    self.fita3[self.cabeca_fita3] = 'B'

                if direcao == '1':
                    self.cabeca_fita3 = max(0, self.cabeca_fita3 - 1)
                elif direcao == '11':
                    self.cabeca_fita3 += 1

                self.estado_atual = f"q{len(novo_estado_codificado) - 1}"

                # Exibe a transição válida
                self.mostrar_estado(i, valida=True)
                return True

            i += 10  # Pula para a próxima transição

        # Se não encontrou uma transição válida
        self.mostrar_estado(i, valida=False)
        return False

    def mostrar_estado(self, transicao_index=None, valida=False):
        fita1_com_transicao = ''
        i = 0
        while i < len(self.fita1):
            if transicao_index is not None and i == transicao_index:
                fita1_com_transicao += '['
                while i < len(self.fita1) and i < transicao_index + 9:
                    fita1_com_transicao += self.fita1[i]
                    i += 1
                fita1_com_transicao += ']'
            else:
                fita1_com_transicao += self.fita1[i]
                i += 1

        fita2_com_transicao = ''.join(
            f"[{comp}]" if idx == 0 else comp
            for idx, comp in enumerate(self.fita2)
        )
        fita3_com_transicao = ''.join(
            f"[{comp}]" if idx == self.cabeca_fita3 else comp
            for idx, comp in enumerate(self.fita3)
        )

        print("Fita 1:", fita1_com_transicao)
        print("Fita 2:", fita2_com_transicao)
        print("Fita 3:", fita3_com_transicao)
        if transicao_index is not None:
            transicao_mostrada = ''.join(self.fita1[transicao_index:transicao_index + 9])
            print("Transição atual:", transicao_mostrada)
            print("Transição", "válida." if valida else "inválida.")

    def verificar_aceitacao(self):
        # Destaca a primeira transição
        self.mostrar_estado(1, valida=False)

        while True:
            if self.estado_atual in self.estados_finais:
                print("Palavra aceita.")
                return True
            if not self.executar_passo():
                if not self.tentar_proxima_transicao():
                    print("Palavra não aceita.")
                    return False

    def tentar_proxima_transicao(self):
        estado_codificado = self.codificar_estado(self.estado_atual)
        simbolo_atual = self.fita3[self.cabeca_fita3] if self.cabeca_fita3 < len(self.fita3) else 'B'
        simbolo_codificado = '11' if simbolo_atual == '1' else '1' if simbolo_atual == '0' else '111'

        i = 1  # Começa após o '000' inicial
        encontrou_transicao_valida = False
        while i < len(self.fita1) - 1:
            if (self.fita1[i] == estado_codificado and 
                self.fita1[i+2] == simbolo_codificado):
                # Encontrou uma transição válida
                self.mostrar_estado(i)
                print("Transição inválida. Tentando a próxima...")
                encontrou_transicao_valida = True
            i += 10  # Pula para a próxima transição

        return encontrou_transicao_valida

# Exemplo de uso
estado_inicial = "q0"
estados_finais = ["q2"]
palavra = "11011"

maquina = MaquinaDeTuring(estado_inicial, estados_finais, palavra)
maquina.verificar_aceitacao()
