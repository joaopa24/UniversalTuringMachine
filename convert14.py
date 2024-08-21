def decode_symbol(encoded_symbol):
    """Decodifica o símbolo conforme a tabela fornecida."""
    if encoded_symbol == '1':
        return '0'
    elif encoded_symbol == '11':
        return '1'
    elif encoded_symbol == '111':
        return 'B'
    else:
        raise ValueError(f"Símbolo codificado desconhecido: {encoded_symbol}")

def decode_state(encoded_state):
    """Decodifica o estado conforme a tabela fornecida usando codificação unária."""
    state_number = len(encoded_state)
    return 'q' + str(state_number - 1)

def decode_direction(encoded_direction):
    """Decodifica a direção da máquina de Turing."""
    if encoded_direction == '1':
        return 'L'
    elif encoded_direction == '11':
        return 'R'
    else:
        raise ValueError(f"Direção codificada desconhecida: {encoded_direction}")

def decode_transition(encoded_transition):
    """Decodifica uma transição da forma especificada."""
    parts = encoded_transition.split('0')
    
    # Verifica se há exatamente 5 partes após a divisão
    if len(parts) != 5:
        raise ValueError("Formato de transição codificada inválido: número incorreto de partes")
    
    enc_state_i = parts[0]
    enc_symbol_x = parts[1]
    enc_state_j = parts[2]
    enc_symbol_y = parts[3]
    enc_direction_d = parts[4]
    
    state_i = decode_state(enc_state_i)
    symbol_x = decode_symbol(enc_symbol_x)
    next_state_j = decode_state(enc_state_j)
    symbol_y = decode_symbol(enc_symbol_y)
    direction_d = decode_direction(enc_direction_d)
    
    return (state_i, symbol_x, next_state_j, symbol_y, direction_d)

def decode_multiple_transitions(encoded_transitions):
    """Decodifica múltiplas transições de uma string codificada, separadas por '00'."""
    encoded_transitions_list = encoded_transitions.split('00')
    
    decoded_transitions = []
    
    for encoded_transition in encoded_transitions_list:
        if encoded_transition:  # Verifica se a parte não está vazia
            try:
                decoded_transition = decode_transition(encoded_transition)
                decoded_transitions.append(decoded_transition)
            except ValueError as e:
                print(f"Erro ao decodificar transição: {e}")
    
    return decoded_transitions

def encode_symbol(symbol):
    """Codifica o símbolo conforme a tabela fornecida."""
    if symbol == '0':
        return '1'
    elif symbol == '1':
        return '11'
    elif symbol == 'B':
        return '111'
    else:
        raise ValueError(f"Símbolo desconhecido: {symbol}")

def encode_state(state):
    """Codifica o estado conforme a tabela fornecida usando codificação unária."""
    state_number = int(state[1:])  # Remove o 'q' e converte para número
    return '1' * (state_number + 1)

def encode_direction(direction):
    """Codifica a direção da máquina de Turing."""
    if direction == 'L':
        return '1'
    elif direction == 'R':
        return '11'
    else:
        raise ValueError(f"Direção desconhecida: {direction}")

def encode_transition(state_i, symbol_x, next_state_j, symbol_y, direction_d):
    """Codifica uma transição no formato especificado."""
    enc_state_i = encode_state(state_i)
    enc_symbol_x = encode_symbol(symbol_x)
    enc_state_j = encode_state(next_state_j)
    enc_symbol_y = encode_symbol(symbol_y)
    enc_direction_d = encode_direction(direction_d)
    
    return enc_state_i + '0' + enc_symbol_x + '0' + enc_state_j + '0' + enc_symbol_y + '0' + enc_direction_d

def process_transitions_file(filename):
    """Processa um arquivo contendo transições e codifica cada uma delas."""
    encoded_transitions = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    # Exemplo de linha: (q0, B) = [q1, B, R]
                    parts = line.split(' = ')
                    left_side = parts[0].strip('()')
                    right_side = parts[1].strip('[]')
                    
                    left_parts = left_side.split(', ')
                    right_parts = right_side.split(', ')
                    
                    if len(left_parts) != 2:
                        raise ValueError("Número incorreto de valores na parte esquerda da transição.")
                    
                    if len(right_parts) != 3:
                        raise ValueError("Número incorreto de valores na parte direita da transição.")
                    
                    state_i, symbol_x = left_parts
                    next_state_j, symbol_y, direction_d = right_parts
                    
                    encoded_transition = encode_transition(state_i, symbol_x, next_state_j, symbol_y, direction_d)
                    encoded_transitions.append(encoded_transition)
                
                except ValueError as e:
                    print(f"Erro ao processar linha: {e}")
    
    # Retorna as transições codificadas separadas por '00'
    return '00'.join(encoded_transitions)

class TuringMachine:
    def __init__(self, tapes, initial_state, encoded_transitions):
        self.tapes = [list(tape) for tape in tapes]  # Cada fita é uma lista
        self.head_positions = [0] * len(tapes)  # Inicializa a posição da cabeça para cada fita
        self.current_state = initial_state
        self.transitions = self.decode_transitions(encoded_transitions)
    
    def decode_transitions(self, encoded_transitions):
        """Decodifica as transições codificadas em um dicionário."""
        decoded_transitions = decode_multiple_transitions(encoded_transitions)
        transitions = {}
        for state_i, symbol_x, next_state_j, symbol_y, direction_d in decoded_transitions:
            transitions[(state_i, symbol_x)] = (next_state_j, symbol_y, direction_d)
        return transitions
    
    def print_transitions(self):
        """Imprime as transições da Máquina de Turing."""
        print("Transições da Máquina de Turing:")
        for (state_i, symbol_x), (next_state_j, symbol_y, direction_d) in self.transitions.items():
            print(f"Se estiver no estado {state_i} e ler o símbolo {symbol_x}:")
            print(f"  - Escreva {symbol_y}")
            print(f"  - Mova para a direção {direction_d}")
            print(f"  - Vá para o estado {next_state_j}")
            print()
    
    def step(self):
        """Executa uma única transição ou entra em um loop se a transição não for encontrada."""
        if any(pos < 0 for pos in self.head_positions):
            raise IndexError("Cabeça de leitura fora dos limites das fitas")
        
        # Expande fitas se necessário
        for i, tape in enumerate(self.tapes):
            if self.head_positions[i] >= len(tape):
                tape.extend(['B'] * (self.head_positions[i] - len(tape) + 1))
        
        current_symbols = [tape[pos] if pos < len(tape) else 'B' for tape, pos in zip(self.tapes, self.head_positions)]
        
        transition_key = (self.current_state, tuple(current_symbols))
        if transition_key not in self.transitions:
            # Se não houver transição, adicione um símbolo 'B' e mova as cabeças para a direita
            for i in range(len(self.tapes)):
                if self.head_positions[i] >= len(self.tapes[i]):
                    self.tapes[i].append('B')
                else:
                    self.tapes[i][self.head_positions[i]] = 'B'
                self.head_positions[i] += 1
            return
        
        next_state, write_symbols, directions = self.transitions[transition_key]
        
        for i, (write_symbol, direction) in enumerate(zip(write_symbols, directions)):
            if self.head_positions[i] >= len(self.tapes[i]):
                self.tapes[i].append(write_symbol)
            else:
                self.tapes[i][self.head_positions[i]] = write_symbol
            
            if direction == 'R':
                self.head_positions[i] += 1
            elif direction == 'L':
                self.head_positions[i] -= 1
        
        self.current_state = next_state
    
    def run(self, max_steps=10):
        """Executa a Máquina de Turing até atingir o número máximo de passos."""
        for _ in range(max_steps):
            print(f"Estado: {self.current_state}")
            for i, (tape, pos) in enumerate(zip(self.tapes, self.head_positions)):
                print(f"  Fita {i}: {''.join(tape)} (Cabeça na posição {pos})")
            try:
                self.step()
            except ValueError as e:
                print(e)
                break
            except IndexError as e:
                print(e)
                break

# Exemplo de uso
filename = 'text.txt'  # Nome do arquivo com transições
encoded_transitions = process_transitions_file(filename)

#print("Sequência codificada:", encoded_transitions)

# Inicializa a Máquina de Turing com fitas iniciais e as transições codificadas
tm = TuringMachine(tapes=['B', 'B', 'B'], initial_state='q0', encoded_transitions=encoded_transitions)

# Imprime as transições da Máquina de Turing
#tm.print_transitions()

# Executa a Máquina de Turing
tm.run()

class TuringMachine:
    def __init__(self, tapes, initial_state, encoded_transitions):
        """Inicializa a Máquina de Turing com três fitas e suas cabeças de leitura."""
        self.tapes = [list(tape) for tape in tapes]
        self.head_positions = [0] * 3
        self.current_state = initial_state
        self.transitions = self.decode_transitions(encoded_transitions)
    
    def decode_transitions(self, encoded_transitions):
        """Decodifica as transições codificadas em um dicionário."""
        decoded_transitions = decode_multiple_transitions(encoded_transitions)
        transitions = {}
        for state_i, symbol_x, next_state_j, symbol_y, direction_d in decoded_transitions:
            # Adapte a transição para múltiplas fitas
            transitions[(state_i, symbol_x)] = (next_state_j, symbol_y, direction_d)
        return transitions
    
    def print_transitions(self):
        """Imprime as transições da Máquina de Turing."""
        print("Transições da Máquina de Turing:")
        for (state_i, symbol_x), (next_state_j, symbol_y, direction_d) in self.transitions.items():
            print(f"Se estiver no estado {state_i} e ler o símbolo {symbol_x}:")
            print(f"  - Escreva {symbol_y}")
            print(f"  - Mova para a direção {direction_d}")
            print(f"  - Vá para o estado {next_state_j}")
            print()
    
    def step(self):
        """Executa uma única transição ou entra em um loop se a transição não for encontrada."""
        if any(pos < 0 for pos in self.head_positions):
            raise IndexError("Cabeça de leitura fora dos limites da fita")
        
        # Verifica se as posições das cabeças estão dentro dos limites das fitas
        for i, (head_pos, tape) in enumerate(zip(self.head_positions, self.tapes)):
            if head_pos >= len(tape):
                tape.extend(['B'] * (head_pos - len(tape) + 1))
        
        # Lê os símbolos das três fitas
        current_symbols = [tape[pos] if pos < len(tape) else 'B' for tape, pos in zip(self.tapes, self.head_positions)]
        
        # Prepara a chave de transição
        transition_key = (self.current_state, tuple(current_symbols))
        if transition_key not in self.transitions:
            # Se não houver transição, adicione um símbolo 'B' em cada fita e mova as cabeças para a direita
            for i, (head_pos, tape) in enumerate(zip(self.head_positions, self.tapes)):
                if head_pos >= len(tape):
                    tape.append('B')
                else:
                    tape[head_pos] = 'B'
                self.head_positions[i] += 1
            return
        
        next_state, write_symbols, directions = self.transitions[transition_key]
        
        # Escreve os símbolos nas fitas correspondentes
        for i, (write_symbol, direction) in enumerate(zip(write_symbols, directions)):
            if self.head_positions[i] >= len(self.tapes[i]):
                self.tapes[i].append(write_symbol)
            else:
                self.tapes[i][self.head_positions[i]] = write_symbol
            
            # Move as cabeças de leitura
            if direction == 'R':
                self.head_positions[i] += 1
            elif direction == 'L':
                self.head_positions[i] -= 1
        
        self.current_state = next_state
    
    def run(self, max_steps=10):
        """Executa a Máquina de Turing até atingir o número máximo de passos."""
        for _ in range(max_steps):
            print(f"Estado: {self.current_state}, Posições das cabeças: {self.head_positions}, Fitas: {[''.join(tape) for tape in self.tapes]}")
            try:
                self.step()
            except ValueError as e:
                print(e)
                break
            except IndexError as e:
                print(e)
                break

# Exemplo de uso
filename = 'text.txt'  # Nome do arquivo com transições
encoded_transitions = process_transitions_file(filename)

#print("Sequência codificada:", encoded_transitions)

# Inicializa a Máquina de Turing com três fitas e suas transições codificadas
tapes = ['B', 'B', 'B']  # Três fitas iniciais
tm = TuringMachine(tapes=tapes, initial_state='q0', encoded_transitions=encoded_transitions)

# Imprime as transições da Máquina de Turing
tm.print_transitions()

# Executa a Máquina de Turing
tm.run()
