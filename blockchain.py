blockchain = []


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_trasaction(trasaction_ammount, last_trasaction):
    blockchain.append([last_trasaction, trasaction_ammount])


def get_trasaction_value():
    user_input = float(input('Your last trasaction amount please:'))
    return user_input


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def verify_chain():
    print(blockchain)
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


# get the first trasaction input and add the value to the blockchain
waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new trasaction value')
    print('2: Output the blockchain blocks')
    print('q: Quit')
    print('h: Manipulate the chain')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_trasaction_value()
        add_trasaction(tx_amount, get_last_blockchain_value())

    # output  the blockchain list to the console
    elif user_choice == '2':
        for block in blockchain:
            print("Outputiing block")
            print(block)
        else:
            print('-' * 20)
    # quiting the program
    elif user_choice == 'q':
        waiting_for_input = False
    # manipulating the program
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    # for invalid input
    else:
        print('Input was invalid,please pick a value from the list')
    # verifing that the chain is not manipulated
    if not verify_chain():
        print('Invalid blockchain!')
        break
else:
    print('User left!')
    print("Choice registered!")
