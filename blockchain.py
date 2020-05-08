from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict

from hash_util import *

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
# The reward we give to miners (for creating a new block)
MINING_REWARD = 10

# mother block or first block
# Our starting block for the blockchain
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
# blockchain containing all the blocks,blockchain is a list of blocks
# Initializing our (empty) blockchain list
blockchain = [genesis_block]

# open_transaction list contains all transactions in it
# Unhandled transactions
open_transaction = []

# We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
# This is sender
owner = 'JAYRAJ'

# participants in a transaction contained in set
# Registered participants: Ourself + other people sending/ receiving coins
participants = {'JAYRAJ'}


def valid_proof(transactions, last_hash, proof):
    """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

        Arguments:
            :transactions: The transactions of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
    # Create a string with all the hash inputs
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # Hash the string
    # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash.
    # It's a not a block's hash. It's only used for the proof-of-work algorithm.
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
    # This condition is of course defined by you. You could also require 10 leading 0s -
    # this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
    return guess_hash[0:2] == '00'


def proof_of_work():
    """Generate a proof of work for the open transactions,
    the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    # Try different PoW numbers and return the first valid one
    while not valid_proof(open_transaction, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    # Calculating the balance for a participant after a transaction
    """Calculate and return the balance for a participant.

        Arguments:
            :participant: The person for whom to calculate the balance.
        """

    # Calculating amount sent by participant.

    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount'] for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    # print("tx_sender=", tx_sender)
    # Calculating the total amount of coins sent
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                         tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]

    # Calculating amount received by participant

    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in
                    blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                             tx_recipient, 0)
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]

    # Calculating balance amount.
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

       Arguments:
           :transaction: The transaction that should be verified.
       """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    # creating a transaction dictionary(using ordered dictionary)
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount}
    transaction = OrderedDict([('sender', sender),
                               ('recipient', recipient),
                               ('amount', amount)])
    # if the verification of transaction is true appending it to open transaction
    if verify_transaction(transaction):
        open_transaction.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it."""
    # Fetch the currently last block of the blockchain
    last_block = blockchain[-1]
    # hashing the last block
    # Hash the last block (=> to be able to compare it to the stored hash value)
    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    # ordered dictionary for reward_transaction
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    # adding reward transaction to open_transaction
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail,
    # we don't have the reward transaction stored in the open transactions
    copied_transactions = open_transaction[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input('Enter the recipient of the transaction:')
    tx_amount = float(input('Your last transaction amount please:'))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
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

        # REWARD TRANSACTION:
        # last transaction in reward_transaction => reward of mining in the block we are mining
        # Reward transaction is appended after calculation of proof of work
        # So the valid proof need to be calculated excluding the reward_transaction

        # Calculating if proof of work is valid
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True


def verify_transactions():
    """Verifies all open transactions."""
    return all([verify_transaction(tx) for tx in open_transaction])


# get the first transaction input and add the value to the blockchain
waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
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
        """ after mining that we is adding open_transaction to a block ,
        we create again a empty open_transaction for next block to come. """
        if mine_block():
            open_transaction = []

    # output  the blockchain list to the console
    elif user_choice == '3':
        print_blockchain_elements()

    # output participants
    elif user_choice == '4':
        print(participants)

    # Verify all open transactions
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')

    # quiting the program
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False

    # manipulating the program
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
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
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left!')

print('Done!')
# git comment now
