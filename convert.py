def encode_symbol(symbol):
    """Codifica o símbolo conforme a tabela fornecida."""
    if symbol == '0':
        return '1'
    elif symbol == '1':
        return '11'
    elif symbol == 'B':
        return '111'
    elif symbol == 'L':
        return '1'
    elif symbol == 'R':
        return '11'
    else:
        raise ValueError(f"Símbolo desconhecido: {symbol}")

def encode_state(state):
    """Codifica o estado conforme a tabela fornecida."""
    return '1' * (len(state) + 1)

def encode_transition(state_i, symbol_x, next_state_j, symbol_y, direction_d):
    """Codifica a transição na forma especificada."""
    enc_state_i = encode_state(state_i)
    enc_symbol_x = encode_symbol(symbol_x)
    enc_state_j = encode_state(next_state_j)
    enc_symbol_y = encode_symbol(symbol_y)
    enc_direction_d = encode_symbol(direction_d)
    
    # Monta a string codificada
    return f"{enc_state_i}0{enc_symbol_x}0{enc_state_j}0{enc_symbol_y}0{enc_direction_d}"

# Exemplo de uso
state_i = "q0"
symbol_x = "1"
next_state_j = "q1"
symbol_y = "0"
direction_d = "R"

encoded_transition = encode_transition(state_i, symbol_x, next_state_j, symbol_y, direction_d)
print("Transição codificada:", encoded_transition)
