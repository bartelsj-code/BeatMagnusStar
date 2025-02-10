import hashlib

def hash_string(input_string):
    """Returns a SHA-256 hash of the input string."""
    return hashlib.sha256(input_string.encode()).hexdigest()