class TuringMachine:
    def __init__(self, tape="", blank_symbol=" ", initial_state="", final_states=None, transition_function=None):
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

# Exemplo de uso
tape = "111B11"  # Representa a soma de 3 + 2 em unário com separador 'B'
initial_state = "q0"
final_states = {"qf"}
transition_function = {
    ("q0", "1"): ("q0", "1", "R"),  # Move para a direita enquanto lê '1'
    ("q0", "B"): ("q1", "1", "R"),  # Substitui o delimitador 'B' por '1' e vai para q1
    ("q1", "1"): ("q1", "1", "R"),  # Move para a direita enquanto lê '1'
    ("q1", " "): ("qf", " ", "N"),  # Quando encontra o espaço em branco, para
}

tm = TuringMachine(tape=tape, initial_state=initial_state, final_states=final_states, transition_function=transition_function)
result = tm.execute()

print("Resultado na fita:", result)
print("Histórico da fita:", tm.tape_history)
