import numpy as np

M = 10000
alice_key = np.random.randint(0, M)
bob_key = np.random.randint(0, M)
global_key = np.random.randint(0, M)
n = np.random.randint(0, M ** 2)

print(" --- Secret Keys ----")
print(" Alice Key: {}".format(alice_key))
print("   Bob Key: {}".format(bob_key))
print(" --- Global Keys ----")
print("         G: {}".format(global_key))
print("         N: {}".format(n))
print("=" * 50)
# 1.
alice_hash = (global_key ** alice_key) % n
bob_hash = (global_key ** bob_key) % n
print("Alice Hash: {}".format(alice_hash))
print("  Bob Hash: {}".format(bob_hash))
print("=" * 50)

# 2.
bob_alice_hash = (alice_hash ** bob_key) % n
alice_bob_hash = (bob_hash ** alice_key) % n
print("Bob-Alice Hash: {}".format(bob_alice_hash))
print("Alice-Bob Hash: {}".format(alice_bob_hash))
if alice_bob_hash == bob_alice_hash:
    print("You are connected!")
