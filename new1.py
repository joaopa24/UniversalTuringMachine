import json

class TuringMachine:
    def __init__(self, tape="", blank_symbol="B", initial_state="", final_states=None, transition_function=None):
        self.tape = list(tape)
        self.blank_symbol = blank_symbol
        self.head_position = 0
        self.current_state = initial_state
        self.final_states = final_states or set()
        self.transition_function = transition_function or {}
        self.tape_history = [self.get_tape_string()]

    def get_tape_string(self):
        return "".join(self.tape).strip()

    def step(self):
        if self.current_state in self.final_states:
            return False

        tape_symbol = self.tape[self.head_position]
        key = (self.current_state, tape_symbol)
        if key not in self.transition_function:
            return False

        new_state, new_symbol, direction = self.transition_function[key]
        self.tape[self.head_position] = new_symbol
        self.current_state = new_state

        if direction == 'R':
            self.head_position += 1
            if self.head_position == len(self.tape):
                self.tape.append(self.blank_symbol)
        elif direction == 'L':
            if self.head_position == 0:
                self.tape.insert(0, self.blank_symbol)
            else:
                self.head_position -= 1

        self.tape_history.append(self.get_tape_string())
        return True

    def execute(self):
        while self.step():
            pass
        return self.get_tape_string()

# JSON string contendo as informações da máquina de Turing
json_data = '''
{
    "tape": "111B1B",
    "initial_state": "q0",
    "final_states": ["qf"],
    "transition_function": {
        "(q0, 1)": ["q0", "1", "R"],
        "(q0, B)": ["q1", "1", "R"],
        "(q1, 1)": ["q1", "1", "R"],
        "(q1, B)": ["qf", "0", "N"]
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
    state, symbol = key.strip("()").split(", ")
    transition_function[(state, symbol)] = tuple(value)

# Atualizar transition_function no dicionário de dados
data['transition_function'] = transition_function

# Instanciar a máquina de Turing com os dados do JSON
tm = TuringMachine(
    tape=data['tape'],
    initial_state=data['initial_state'],
    final_states=data['final_states'],
    transition_function=data['transition_function']
)

# Executar a máquina de Turing
result = tm.execute()

# Exibir o resultado
print("Resultado na fita:", result)
print("Histórico da fita:", tm.tape_history)
