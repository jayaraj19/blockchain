# mother block or first block
genesis_block = {
	'previous_hash': '',
	'index': 0,
	'transactions': []
}
# blockchain containing all the blocks
blockchain = [genesis_block]

# open_transaction contains a dictionary with transaction data in it
open_transaction = []

# This is sender
owner = 'JAYRAJ'


def hash_block(block):
	return '-'.join([str(block[key]) for key in block])


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
	transcation = {
		'sender': sender,
		'recipient': recipient,
		'amount': amount}
	open_transaction.append(transcation)


def mine_block():
	""" after hashing adding of blocks to the blockchain happens"""
	last_block = blockchain[-1]
	hashed_block = hash_block(last_block)
	print(hashed_block)
	block = {
		'previous_hash': hashed_block,
		'index': len(blockchain),
		'transactions': open_transaction
	}
	blockchain.append(block)


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
	print('q: Quit')
	print('h: Manipulate the chain')
	user_choice = get_user_choice()

	if user_choice == '1':
		tx_data = get_transaction_value()
		recipient, amount = tx_data
		# add transaction to the open_transaction
		add_transaction(recipient, amount=amount)
		print(open_transaction)

	# Mine block
	elif user_choice == '2':
		mine_block()

	# output  the blockchain list to the console
	elif user_choice == '3':
		print_blockchain_elements()

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
else:
	print('User left!')

print('Done!')
