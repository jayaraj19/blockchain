"""
DATA STRUCTURE
blockchain[
    block{previous_hash:@#$WEbFFEb,
          index:some number,
          transactions:open_transaction[
                                         transaction1{sender:name,
                                                      recipient:name,
                                                      amount=money},
                                         transaction2{},.......
                                        ]
          },
    block2{},.......
]
"""
MINING_REWARD = 10

# mother block or first block
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
# blockchain containing all the blocks,blockchain is a list of blocks
blockchain = [genesis_block]

# open_transaction list contains all transactions in it
open_transaction = []

# This is sender
owner = 'JAYRAJ'
# participants in a transaction contained in set
participants = {'JAYRAJ'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    """Calculating the balance for a participant after a transaction"""

    # Calculating amount sent by participant.
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print("tx_sender=",tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    # Calculating amount received by participant
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in
                    blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]

    # Calculating balance amount.
    return amount_received - amount_sent


def verify_transaction(transaction):
    """Checking weather the sender have enough money to send the set amount or not
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Arguments:
    : sender: The sender of the coins
    : recipient: The recipient of the coins.
    : amount: The amount of coins sent with the transactions (default =1.0)
    """
    # creating a transaction dictionary
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount}
    # if the verification of transaction is true appending it to open transaction
    if verify_transaction(transaction):
        open_transaction.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    """ after hashing adding of blocks to the blockchain happens"""
    last_block = blockchain[-1]
    # hashing the last block
    hashed_block = hash_block(last_block)
    # creating reward transaction for mining the block
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # adding reward transaction to open_transaction
    open_transaction.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transaction
    }
    # adding a block to blockchain
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction:')
    tx_amount = float(input('Your last transaction amount please:'))
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ output all the blocks"""
    for block in blockchain:
        print("Outputting block :")
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """verify the current current blockchain and return True if  it's valid,False if it's invalid"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


# get the first transaction input and add the value to the blockchain
waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('q: Quit')
    print('h: Manipulate the chain')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # add transaction to the open_transaction
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
            print(open_transaction)
        else:
            print('Transaction failed!')


    # Mine block
    elif user_choice == '2':
        """ after mining that is adding open_transaction to a block ,
        we create again a empty open_transaction for next block to come. """
        if mine_block():
            open_transaction = []

    # output  the blockchain list to the console
    elif user_choice == '3':
        print_blockchain_elements()

    # output participants
    elif user_choice == '4':
        print(participants)

    # quiting the program
    elif user_choice == 'q':
        waiting_for_input = False

    # manipulating the program
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'JAYRAJ', 'recipient': 'KUNDAN', 'amount': 100.0}]
            }

    # for invalid input
    else:
        print('Input was invalid,please pick a value from the list')

    # verifying that the chain is not manipulated
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    # printing the balance left for owner after a transaction.
    print(get_balance(owner))
else:
    print('User left!')

print('Done!')
# git comment now
