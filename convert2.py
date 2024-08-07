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
    """Decodifica o estado conforme a tabela fornecida."""
    return 'q' + str(len(encoded_state))

def decode_transition(encoded_transition):
    """Decodifica a transição da forma especificada."""
    parts = encoded_transition.split('0')
    
    if len(parts) != 5:
        raise ValueError("Formato de transição codificada inválido")
    
    enc_state_i = parts[0]
    enc_symbol_x = parts[1]
    enc_state_j = parts[2]
    enc_symbol_y = parts[3]
    enc_direction_d = parts[4]
    
    state_i = decode_state(enc_state_i)
    symbol_x = decode_symbol(enc_symbol_x)
    next_state_j = decode_state(enc_state_j)
    symbol_y = decode_symbol(enc_symbol_y)
    direction_d = decode_symbol(enc_direction_d)
    
    return (state_i, symbol_x, next_state_j, symbol_y, direction_d)

# Exemplo de uso
encoded_transition = "1" + "0" + "11" + "0" + "11" + "0" + "1" + "0" + "11"
decoded_transition = decode_transition(encoded_transition)

print("Transição decodificada:", decoded_transition)
