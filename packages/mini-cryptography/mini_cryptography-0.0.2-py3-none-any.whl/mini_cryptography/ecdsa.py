""" ECDSA file info.
The following script allows users to perform ECC (Elliptic Curve Cryptography)
arithmetic operations, including ECDSA (Elliptic Curve Digital Signature Algorithm)
signature formation and verification.

Pre-requisite :
tiny.ec package to be installed within the Python runtime environment
"""
import random
from tinyec import ec

class Point:
    """ A class used to represent an ECC (Elliptic Curve Cryptography) point
    """

    def __init__(self, x:int, y:int):
        """
        Args:
            x (int): Point coordinate x
            y (int): Point coordinate y
        """
        self.x = x
        self.y = y

    def to_array(self):
        """ Returns point x, y coordinates as array

        Returns:
            list[int]: Array of coordinates x, y
        """
        return [self.x, self.y]

    def __eq__(self, other):
        """ Compares two Point class objects

        Args:
            other (Point): Other Point class object

        Returns:
            bool: Are two objects equal
        """
        if isinstance(other, Point):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

class Field:
    """ A class used to represent an ECC finite field
    """

    def __init__(self, a:int, b:int, n:int, p:int, G:Point):
        """
        Args:
            a (int): elliptic curve parameter (equal to q-3 for P-256)
            b (int): elliptic curve parameter
            n (int): the order of the base point G
            p (int): the size of the underlying field
            G (Point):  (xG, y G), a point on the curve, known as the base point
        """
        self.a = a
        self.b = b
        self.n = n
        self.p = p
        self.g = G.to_array()

class Ecdsa:
    """ A class used to do ECC arithmetic operations and 
        ECDSA (Elliptic Curve Digital Signature Algorithm)
        signature formation and verification
    """

    def __init__(self, field:Field, name:str):
        """
        Args:
            field (Field): Curve field
            name (str): Curve name
        """
        self.curve = ec.Curve(a=field.a, b=field.b, field=field, name=name)
        self.field = field

    def getName(self):
        """ Returns ECDSA curve name

        Returns:
            str: ECDS curve name
        """
        return self.curve.name

    def G_multiplication(self, multiplyer:int):
        """Multiplies G point from the given multiplier

        Args:
            multiplyer (int): Given point multipliers

        Returns:
            Point: A new point after multiplication
        """
        newPoint = self.curve.g * multiplyer
        return Point(newPoint.x, newPoint.y)

    def calculate_public_key(self, private_key:int):
        """Calculate the public key

        Args:
            private_key (int): private key value

        Returns:
            Point: A public key
        """
        return self.G_multiplication(private_key)

    def sum_points(self, point1:Point, point2:Point):
        """ Points sum

        Args:
            point1 (Point): First point
            point2 (Point): Second point

        Returns:
            Point: A new point that is the sum of the first and second points
        """
        point1 = ec.Point(curve=self.curve, x=point1.x, y=point1.y)
        point2 = ec.Point(curve=self.curve, x=point2.x, y=point2.y)

        newPoint = point1 + point2
        return Point(newPoint.x, newPoint.y)

    def multiply_points(self, point:Point, multiplyer:int):
        """Point multiplication from a given multiplier

        Args:
            point (Point): Curve point
            multiplyer (int): Given point multiplier

        Returns:
            Point: A new point after multiplication
        """
        point = ec.Point(curve=self.curve, x=point.x, y=point.y)

        newPoint = point * multiplyer
        return Point(newPoint.x, newPoint.y)

    def generate_random_number(self, lower:int, upper:int):
        """Generates random number [lower, ... upper range]
        
        Args:
            lower (int): lower is the lower limit of the range
            upper (int): upper is the upper limit of the range

        Returns:
            int: generated number
        """
        return random.randint(1, self.field.n-1)

    def k_generator(self):
        """Generates random k [1, ... n-1]

        Returns:
            int: random number k
        """
        return self.generate_random_number(1, self.field.n-1)

    def private_key_generator(self):
        """Generates random x [1, ... n-1]

        Returns:
            int: private key x
        """
        return self.generate_random_number(1, self.field.n-1)

    def sign_message(self, private_key:int, k:int, hash:str):
        """Create a signature for the given message.

        Args:
            private_key (int): private key value
            k (int): random number k
            hash (str): message hash value

        Returns:
            int, int:  e. signature component values r, s
            bool: 0 if wrong r or 1 if wrong s
        """
        k_Gx = self.G_multiplication(k).x
        r = k_Gx % self.field.n
        if r == 0:
            return 0

        s = (pow(k, -1, self.field.n) * (hash + private_key * r)) % self.field.n
        if s == 0:
            return 1

        return r, s

    def verify_signature(self, r:int, s:int, hash:str, public_key:Point):
        """Verifies signature validity

        Args:
            r (int): Signature component r
            s (int): Signature component s
            hash (str): Message hash
            public_key (Point): Public key

        Returns:
            bool: Verification result
        """
        if (s > self.field.n-1 or r > self.field.n-1 or s < 1 or r < 1): #[1, n – 1]
            return False

        w = pow(s, -1, self.field.n)
        u1 = (hash * w) % self.field.n
        u2 = (r * w) % self.field.n

        x2 = self.sum_points(self.G_multiplication(u1), self.multiply_points(public_key, u2)).x
        v = x2 % self.field.n

        if r == v:
            return True
        return False
