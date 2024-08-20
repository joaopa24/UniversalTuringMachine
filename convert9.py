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

class TuringMachine:
    def __init__(self, tape, initial_state, transitions):
        self.tape = list(tape)
        self.head_position = 0
        self.current_state = initial_state
        self.transitions = transitions
    
    def run(self, max_steps=2000):
        """Executa a Máquina de Turing até atingir o número máximo de passos."""
        for _ in range(max_steps):
            print(f"Estado: {self.current_state}, Posição: {self.head_position}, Fita: {''.join(self.tape)}")
            try:
                self.step()
            except ValueError as e:
                print(e)
                break

    def step(self):
        """Executa uma única transição."""
        # Expande a fita se a cabeça da fita estiver fora dos limites
        if self.head_position < 0:
            self.tape.insert(0, 'B')
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append('B')
        
        # Verifica o símbolo atual da fita
        current_symbol = self.tape[self.head_position]
        
        transition_key = (self.current_state, current_symbol)
        print(f"Verificando transição para a chave: {transition_key}")
        if transition_key not in self.transitions:
            raise ValueError(f"Transição não encontrada para a chave: {transition_key}")
        
        next_state, write_symbol, direction = self.transitions[transition_key]
        
        # Atualiza a fita e a posição da cabeça
        self.tape[self.head_position] = write_symbol
        
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        
        self.current_state = next_state


# Exemplo de uso
encoded_transitions = "101110110111011"

print("Sequência codificada:", encoded_transitions)

decoded_transitions = decode_multiple_transitions(encoded_transitions)

# Imprime as transições decodificadas para revisão
print("Transições decodificadas:")
for transition in decoded_transitions:
    print(transition)

# Constrói o dicionário de transições
transitions = {}
for state_i, symbol_x, next_state_j, symbol_y, direction_d in decoded_transitions:
    transitions[(state_i, symbol_x)] = (next_state_j, symbol_y, direction_d)

# Cria uma fita inicial
tape = "B"

# Inicializa a Máquina de Turing
tm = TuringMachine(tape=tape, initial_state='q0', transitions=transitions)

# Executa a Máquina de Turing
tm.run()
