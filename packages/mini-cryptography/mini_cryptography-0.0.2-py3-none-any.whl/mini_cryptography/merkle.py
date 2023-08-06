""" Merkle file info.
The following script allows users to calculate the Merkle tree root using 
different hash algorithm functions.
"""
import binascii
import hashlib
from enum import Enum

class Merkle:
    """ A class that is used to calculate the Merkle tree root
    """
    class SHA(Enum):
        """ An enumerator that is used to represent possible hash algorithms

        Args:
            Enum (constant): Hash algorithm
        """
        SHA1 = 1
        SHA224 = 2
        SHA256 = 3
        SHA3_224 = 4
        SHA3_256 = 5
        SHA3_384 = 6
        SHA3_512 = 7
        SHA512 = 8
        SHAKE_128 = 9
        SHAKE_256 = 10

    def __init__(self, sha:SHA = SHA.SHA256, shake_length:int = 100):
        """
        Args:
            sha (SHA, optional): Hash algorithm for Merkle tree root calculation.
            Defaults to SHA.SHA256.
        """
        self.sha = sha
        self.shake_length = shake_length

    def calculate_hash(self, value:str):
        """Calculates the hash value from the given text.

        Args:
            value (str): text

        Returns:
            str: hash value
        """
        hash = ""
        match self.sha:
            case self.SHA.SHA1:
                hash = hashlib.sha1(value)
            case self.SHA.SHA224:
                hash = hashlib.sha224(value)
            case self.SHA.SHA256:
                hash = hashlib.sha256(value)
            case self.SHA.SHA3_224:
                hash = hashlib.sha3_224(value)
            case self.SHA.SHA3_256:
                hash = hashlib.sha3_256(value)
            case self.SHA.SHA3_384:
                hash = hashlib.sha384(value)
            case self.SHA.SHA3_512:
                hash = hashlib.sha3_512(value)
            case self.SHA.SHA512:
                hash = hashlib.sha512(value)
            case self.SHA.SHAKE_128:
                hash = hashlib.shake_128(value)
                return hash.digest(self.shake_length)
            case self.SHA.SHAKE_256:
                hash = hashlib.shake_256(value)
                return hash.digest(self.shake_length)
            case _:
                hash = hashlib.sha256(value)

        return hash.digest()

    def __hashIteration__(self, firstHash:str, secondHash:str):
        """Concatenate the hashes together and find the common hash.

        Args:
            firstHash (str): first hash
            secondHash (str): second hash

        Returns:
            str: combined hash in hexadecimal format
        """
        unhex_first = binascii.unhexlify(firstHash)
        unhex_second = binascii.unhexlify(secondHash)

        combined_hash = unhex_first + unhex_second
        common_hash = self.calculate_hash(combined_hash)
        final_hash = self.calculate_hash(common_hash)

        return binascii.hexlify(final_hash)

    def __merkleCalculation__(self, hashList:list[str]):
        """Get a new list of concatenated hashes.

        Args:
            hashList (list[str]): hash list

        Returns:
            list[str]: a new list of combined hashes
        """
        if len(hashList) == 1: #If only one hash left
            return hashList[0]

        newHashList = []
        # Find the common hash from the pair of hashes
        for i in range(0, len(hashList)-1, 2):
            newHashList.append(self.__hashIteration__(hashList[i], hashList[i+1]))
        if len(hashList) % 2 == 1: # If the number of hashed pairs is odd, the hash should be reused
            newHashList.append(self.__hashIteration__(hashList[-1], hashList[-1]))

        return self.__merkleCalculation__(newHashList)

    def shift_hash(self, hash:str):
        """Shifts the hexadecimal hash from little-endian to big-endian, and back.

        Args:
            hash (str): hash

        Returns:
            bytes: The return value is a bytes object. This function is also
            available as "b2a_hex()".
        """
        return binascii.hexlify(binascii.unhexlify(hash)[::-1])

    def transaction_hash(self, transaction:str):
        """Calculates the transaction hash.

        Args:
            transaction (str): transaction

        Returns:
            str: transaction hash
        """
        unhex_hash = binascii.unhexlify(transaction)
        common_hash = self.calculate_hash(unhex_hash)
        final_hash = self.calculate_hash(common_hash)

        return binascii.hexlify(final_hash)

    def merkle_root(self, transactionList:list[str], hashTransaction:bool = 1):
        """Calculates the Merkle root of transactions.

        Args:
            transactionList (list[str]): transaction list.
            hashTransaction (bool, optional): is transactions hashed.
            Defaults to 1 (hashed).

        Returns:
            str: Merkle root value in hexadecimal format
        """
        if hashTransaction:
            for i in range(0, len(transactionList)):
                transactionList[i] = self.transaction_hash(transactionList[i])

        calculatedMerkleRoot = str(
            self.shift_hash(self.__merkleCalculation__(transactionList)), 'utf-8'
        )
        return calculatedMerkleRoot
