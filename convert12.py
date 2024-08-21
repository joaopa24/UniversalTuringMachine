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
                # Exemplo de linha: (q0, B) = [q1, B, R]
                parts = line.split(' = ')
                left_side = parts[0].strip('()')
                right_side = parts[1].strip('[]')
                
                state_i, symbol_x = left_side.split(', ')
                next_state_j, symbol_y, direction_d = right_side.split(', ')
                
                encoded_transition = encode_transition(state_i, symbol_x, next_state_j, symbol_y, direction_d)
                encoded_transitions.append(encoded_transition)
    
    # Retorna as transições codificadas separadas por '00'
    return '00'.join(encoded_transitions)

class TuringMachine:
    def __init__(self, tape, initial_state, encoded_transitions):
        self.tape = list(tape)
        self.head_position = 0
        self.current_state = initial_state
        self.transitions = self.decode_transitions(encoded_transitions)
    
    def decode_transitions(self, encoded_transitions):
        """Decodifica as transições codificadas em um dicionário."""
        decoded_transitions = decode_multiple_transitions(encoded_transitions)
        transitions = {}
        for state_i, symbol_x, next_state_j, symbol_y, direction_d in decoded_transitions:
            transitions[(state_i, symbol_x)] = (next_state_j, symbol_y, direction_d)
        return transitions
    
    def step(self):
        """Executa uma única transição ou entra em um loop se a transição não for encontrada."""
        if self.head_position < 0:
            raise IndexError("Cabeça de leitura fora dos limites da fita")
        
        # Verifica se a posição da cabeça está dentro dos limites da fita
        if self.head_position >= len(self.tape):
            self.tape.extend(['B'] * (self.head_position - len(self.tape) + 1))
        
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else 'B'
        
        transition_key = (self.current_state, current_symbol)
        if transition_key not in self.transitions:
            # Se não houver transição, adicione um símbolo 'B' e mova a cabeça para a direita
            if self.head_position >= len(self.tape):
                self.tape.append('B')
            else:
                self.tape[self.head_position] = 'B'
            self.head_position += 1
            return
        
        next_state, write_symbol, direction = self.transitions[transition_key]
        
        if self.head_position >= len(self.tape):
            self.tape.append(write_symbol)
        else:
            self.tape[self.head_position] = write_symbol
        
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        
        self.current_state = next_state
    
    def run(self, max_steps=10):
        """Executa a Máquina de Turing até atingir o número máximo de passos."""
        for _ in range(max_steps):
            print(f"Estado: {self.current_state}, Posição: {self.head_position}, Fita: {''.join(self.tape)}")
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

print("Sequência codificada:", encoded_transitions)

# Inicializa a Máquina de Turing com a fita inicial e as transições codificadas
tm = TuringMachine(tape='B', initial_state='q0', encoded_transitions=encoded_transitions)

# Executa a Máquina de Turing
tm.run()
