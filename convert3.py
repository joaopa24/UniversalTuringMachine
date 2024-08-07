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
    """Decodifica uma transição da forma especificada."""
    parts = encoded_transition.split('0')
    
    # Diagnóstico para verificar as partes
    print(f"Encoded Transition: {encoded_transition}")
    print(f"Parts after split: {parts}")
    
    # Verifica se há exatamente 5 partes após a divisão
    # Adiciona partes vazias para garantir o formato esperado
    if len(parts) < 5:
        parts += [''] * (5 - len(parts))
    
    if len(parts) != 5:
        raise ValueError("Formato de transição codificada inválido: número incorreto de partes")
    
    # Pode haver partes vazias se a sequência de zeros estiver no início ou fim
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

def decode_multiple_transitions(encoded_transitions):
    """Decodifica múltiplas transições de uma string codificada, separadas por '00'."""
    # Divide a string de transições usando o delimitador '00'
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

# Exemplo de uso
encoded_transitions = "10111011011101100110101010100110110111011011001110110101101"

print("Sequência codificada:", encoded_transitions)

decoded_transitions = decode_multiple_transitions(encoded_transitions)

print("Transições decodificadas:", decoded_transitions)
