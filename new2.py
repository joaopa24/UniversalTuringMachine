import json

class MultiTapeTuringMachine:
    def __init__(self, tapes=None, blank_symbol="B", initial_state="", final_states=None, transition_function=None):
        self.tapes = [list(tape) for tape in tapes]
        self.blank_symbol = blank_symbol
        self.head_positions = [0] * len(self.tapes)  # Uma cabeça de leitura por fita
        self.current_state = initial_state
        self.final_states = final_states or set()
        self.transition_function = transition_function or {}
        self.tape_history = [self.get_tapes_string()]

    def get_tapes_string(self):
        return ["".join(tape).strip() for tape in self.tapes]

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

        self.tape_history.append(self.get_tapes_string())
        return True

    def execute(self):
        while self.step():
            pass
        return self.get_tapes_string()

    def is_accepted(self):
        return self.current_state in self.final_states

# JSON string contendo as informações da máquina de Turing multifita
json_data = '''
{
    "tapes": ["111B", "B", "111B11"],
    "initial_state": "q0",
    "final_states": ["qf"],
    "transition_function": {
        "(q0, '1')": ["q0", "1", "R"],
        "(q0, 'B')": ["q1", "B", "R"],
        "(q1, '1')": ["qf", "0", "N"]
    }
}
'''

# Carregar dados do JSON
data = json.loads(json_data)

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
print("Resultado nas fitas:", result)
print("Histórico das fitas:", tm.tape_history)
print("Palavra aceita?" , "Sim" if accepted else "Não")
