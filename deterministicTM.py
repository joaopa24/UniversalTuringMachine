from automata.fa.nfa import NFA

# Máquina de Turing para adicionar 1 a um número binário na fita
ntm_successor = NTA (
    states={'q0', 'q1', 'q2', 'qf'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    transitions={
        'q0': {
            'B': ('q1', 'B', 'R')
        },
        'q1': {
            '1': ('q1', '1', 'R'),
            'B': ('qf', '1', 'L')
        },
        'qf': {
            '1': ('qf', '1', 'L')
        }
    },
    initial_state='q0',
    blank_symbol='B',
    final_states={'qf'}
)

def run_ntm_successor(input_str):
    # Inicializa a fita com a entrada fornecida
    ntm_successor.initialize(input_str)

    # Executa a DTM
    dtm_successor.process_input()

    # Retorna a fita após processamento
    return dtm_successor.get_tape_content()

# Testando com alguns exemplos
input_str = "1011"
result = run_ntm_successor(input_str)
print(f"Fita após processamento: {result}")

input_str = "111"
result = run_ntm_successor(input_str)
print(f"Fita após processamento: {result}")

input_str = "000"
result = run_ntm_successor(input_str)
print(f"Fita após processamento: {result}")