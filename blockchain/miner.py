import hashlib
import requests

import sys

from uuid import uuid4
import time

from timeit import default_timer as timer

import random

# Find a number p' such that the last six digits of hash(p) are equal to the first six digits of hash(p') - IE: last_hash: ...999123456, new hash 123456888... - p is the previous proof, and p' is the new proof


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = time.time()

    print("Searching for next proof")
    print('last proof: ', last_proof)
    # proof = int(time.time())
    proof = 43524354326624
    while valid_proof(last_proof, proof) is False:
        time_now = time.time()
        if time_now - start > 5:
            return
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))

    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    #: Your code here!
    guess = f'{proof}'.encode()
    hashed_p_prime = hashlib.sha256(guess).hexdigest()

    prev_proof = f'{last_hash}'.encode()
    hashed_p = hashlib.sha256(prev_proof).hexdigest()
    return hashed_p_prime[:6] == hashed_p[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        if not new_proof:
            continue
        print('attempting to submit')

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
            print("Total coins mined: " + str(coins_mined))
