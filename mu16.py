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
        raise ValueError(f"Formato de transição codificada inválido: número incorreto de partes ({len(parts)})")
    
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
    word = ""
    reading_transitions = True
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '-':
                reading_transitions = False
                continue
            if reading_transitions:
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
            else:
                word = line
    
    # Exibe a palavra w
    print(f"Palavra de entrada W: {word}")
    
    # Retorna as transições codificadas separadas por '00' e a palavra w
    return '00'.join(encoded_transitions), word

class TuringMachine:
    def __init__(self, tapes, initial_state, encoded_transitions):
        """Inicializa a Máquina de Turing com fitas e suas cabeças de leitura."""
        self.tapes = [list(tape) for tape in tapes]
        self.head_positions = [0] * len(tapes)
        self.current_state = initial_state
        self.transitions = self.decode_transitions(encoded_transitions)
    
    def decode_transitions(self, encoded_transitions):
        """Decodifica as transições codificadas em um dicionário."""
        decoded_transitions = decode_multiple_transitions(encoded_transitions)
        transitions = {}
        for state_i, symbol_x, next_state_j, symbol_y, direction_d in decoded_transitions:
            transitions[(state_i, symbol_x)] = (next_state_j, symbol_y, direction_d)
        return transitions
    
    def print_fitas(self):
        """Imprime as fitas da Máquina de Turing com cabeças de leitura destacadas."""
        print(f"Estado: {self.current_state}")
        for i, (tape, head_pos) in enumerate(zip(self.tapes, self.head_positions)):
            tape_str = ''.join(tape)
            if head_pos < 0:
                tape_str = '<' + tape_str[0] + tape_str[1:]
            elif head_pos >= len(tape_str):
                tape_str = tape_str + ' >'
            else:
                tape_str = tape_str[:head_pos] + '[' + tape_str[head_pos] + ']' + tape_str[head_pos+1:]
            
            print(f"Fita {i+1}: {tape_str}")
        print()
    
    def step(self):
        """Executa uma única transição ou entra em um loop se a transição não for encontrada."""
        if any(pos < 0 for pos in self.head_positions):
            raise IndexError("Cabeça de leitura fora dos limites das fitas")
        
        # Expande fitas se necessário
        for i, (tape, pos) in enumerate(zip(self.tapes, self.head_positions)):
            if pos >= len(tape):
                tape.extend(['B'] * (pos - len(tape) + 1))
        
        current_symbols = [tape[pos] if pos < len(tape) else 'B' for tape, pos in zip(self.tapes, self.head_positions)]
        
        transition_key = (self.current_state, tuple(current_symbols))
        if transition_key not in self.transitions:
            # Se não houver transição, não faz nada e apenas sai do método
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
            self.print_fitas()
            try:
                self.step()
            except ValueError as e:
                print(e)
                break
            except IndexError as e:
                print(e)
                break

# Exemplo de uso
filename = 'text.txt'  # Nome do arquivo com transições codificadas
encoded_transitions, word = process_transitions_file(filename)

# Inicialização das fitas e estado inicial
tapes = [list(word), 'B', 'B']  # A primeira fita contém a palavra w
initial_state = 'q0'

# Cria a Máquina de Turing
tm = TuringMachine(tapes, initial_state, encoded_transitions)

# Executa a Máquina de Turing
tm.run(max_steps=20)
