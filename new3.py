import json

class MultiTapeTuringMachine:
    def __init__(self, tapes=None, blank_symbol="B", initial_state="", final_states=None, transition_function=None):
        self.tapes = [list(tape) for tape in tapes]
        self.blank_symbol = blank_symbol
        self.head_positions = [0] * len(self.tapes)  # Uma cabeça de leitura por fita
        self.current_state = initial_state
        self.final_states = final_states or set()
        self.transition_function = transition_function or {}
        self.tape_history = [self.get_tape_3_string()]

    def get_tape_3_string(self):
        tape = self.tapes[2]  # Fita 3
        head_pos = self.head_positions[2]
        # Construir a string da fita 3 com colchetes ao redor do símbolo lido
        if head_pos < len(tape):
            return ''.join(tape[:head_pos]) + '[' + tape[head_pos] + ']' + ''.join(tape[head_pos+1:])
        else:
            return ''.join(tape) + '[]'  # Caso a cabeça esteja fora da fita

    def step(self):
        if self.current_state in self.final_states:
            return False

        # Obter símbolo sob a cabeça de leitura da fita 3
        tape_symbol = self.tapes[2][self.head_positions[2]]  # Usando a fita 3 (índice 2)
        key = (self.current_state, tape_symbol)
        
        if key not in self.transition_function:
            return False

        # Aplicar a transição
        new_state, new_symbol, direction = self.transition_function[key]
        self.current_state = new_state
        
        # Atualizar fita 3 com o novo símbolo e direção
        self.tapes[2][self.head_positions[2]] = new_symbol

        if direction == 'R':
            self.head_positions[2] += 1
            if self.head_positions[2] == len(self.tapes[2]):
                self.tapes[2].append(self.blank_symbol)
        elif direction == 'L':
            if self.head_positions[2] == 0:
                self.tapes[2].insert(0, self.blank_symbol)
            else:
                self.head_positions[2] -= 1

        self.tape_history.append(self.get_tape_3_string())
        return True

    def execute(self):
        while self.step():
            pass
        return self.get_tape_3_string()

    def is_accepted(self):
        return self.current_state in self.final_states

# Carregar dados do arquivo JSON
with open('text.json', 'r') as file:
    data = json.load(file)
    print(data)  # Adicione esta linha para depuração

# Verificar se as chaves necessárias estão presentes
required_keys = ['tapes', 'initial_state', 'final_states', 'transition_function']
for key in required_keys:
    if key not in data:
        raise KeyError(f"Missing required key: {key}")

# Convertendo final_states de lista para set
data['final_states'] = set(data['final_states'])

# Convertendo as chaves da transition_function de string para tuplas
transition_function = {}
for key, value in data['transition_function'].items():
    # Removendo os parênteses e dividindo o conteúdo pelo separador
    key = key.strip("()")
    state, symbol = key.split(", ")
    symbol = symbol.strip("'")
    transition_function[(state, symbol)] = (value[0], value[1], value[2])

# Atualizar transition_function no dicionário de dados
data['transition_function'] = transition_function

# Instanciar a máquina de Turing com os dados do JSON
tm = MultiTapeTuringMachine(
    tapes=data['tapes'],
    initial_state=data['initial_state'],
    final_states=data['final_states'],
    transition_function=data['transition_function']
)

# Executar a máquina de Turing
result = tm.execute()

# Verificar se a palavra é aceita
accepted = tm.is_accepted()

# Exibir o resultado
print("Resultado na fita 3:")
print(result)
print("Histórico da fita 3:")
for tape_state in tm.tape_history:
    print(tape_state)
print("Palavra aceita?" , "Sim" if accepted else "Não")
