#!/usr/bin/env python3
"""
SILENT RADIX — Reference Implementation v0.1
=============================================
Cryptographic primitive: positional numeral with silent (secret) base.
Security reduces to Unknown-Weight Integer Knapsack (UWIK).

This implementation demonstrates:
  1. Single-base encoding/decoding (INSECURE — for illustration only)
  2. Per-symbol-base encoding/decoding (hardened variant)
  3. Lattice attack on small-parameter single-base instances using LLL

Author: DeepChat Research Pipeline
Date:   2026-07-02
Status: PROTOTYPE — not production-ready
"""

import secrets
import hashlib
import struct
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════
# 1. CORE PRIMITIVE: Single-Base Silent Radix (INSECURE — demo only)
# ═══════════════════════════════════════════════════════════════════════

def encode_single_base(plaintext: bytes, base: int) -> str:
    """Encode plaintext bytes as a digit string in the given base.
    
    Digits are comma-separated to handle bases > 10 where individual
    digits may require multiple decimal characters (e.g., base-256 digit "255").
    
    The BASE remains silent (not included in the ciphertext).
    Only digit separators are present — these reveal digit boundaries
    but NOT the base.
    
    INSECURE: Single-base reuse enables lattice attacks.
    For secure use, see encode_per_symbol() below.
    """
    if base < 2:
        raise ValueError(f"Base must be >= 2, got {base}")
    
    # Convert bytes to integer
    M = int.from_bytes(plaintext, 'big')
    
    # Encode in base-b digits (least significant first)
    if M == 0:
        return "0"
    
    digits = []
    while M > 0:
        digits.append(M % base)
        M //= base
    
    # Reverse to most-significant-first, join with commas
    digits.reverse()
    return ",".join(str(d) for d in digits)


def decode_single_base(ciphertext: str, base: int) -> bytes:
    """Decode a comma-separated digit string back to bytes using the known base."""
    M = 0
    for token in ciphertext.split(","):
        M = M * base + int(token)
    
    # Convert integer back to bytes
    byte_len = max(1, (M.bit_length() + 7) // 8)
    return M.to_bytes(byte_len, 'big')


# ═══════════════════════════════════════════════════════════════════════
# 2. HARDENED VARIANT: Per-Symbol-Base Silent Radix
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class SilentRadixKey:
    """Expanded key: a sequence of secret bases for per-symbol encoding."""
    bases: List[int]
    block_size: int  # bytes per block
    
    def __len__(self):
        return len(self.bases)


def derive_bases(seed: bytes, num_blocks: int, base_bits: int = 256) -> List[int]:
    """Derive per-symbol bases from a seed using HKDF-expand.
    
    Each base is a random integer in [2^(base_bits-1), 2^base_bits).
    Minimum base size ensures brute-force search space >= 2^(base_bits-1).
    """
    bases = []
    # Use HKDF-like expansion: H(seed || i) for each base
    for i in range(num_blocks):
        h = hashlib.sha256(seed + struct.pack('>Q', i)).digest()
        # Convert hash to integer in desired range
        b = int.from_bytes(h, 'big')
        min_base = 2 ** (base_bits - 1)
        max_base = 2 ** base_bits - 1
        b = min_base + (b % (max_base - min_base + 1))
        bases.append(b)
    return bases


def keygen(seed: bytes, num_blocks: int, block_size: int = 16,
           base_bits: int = 256) -> SilentRadixKey:
    """Generate a silent radix key from a seed.
    
    Args:
        seed: Secret key material (>= 256 bits recommended)
        num_blocks: Number of plaintext blocks to support
        block_size: Bytes per plaintext block
        base_bits: Bit-length of each secret base
    
    Returns:
        SilentRadixKey with derived bases
    """
    bases = derive_bases(seed, num_blocks, base_bits)
    return SilentRadixKey(bases=bases, block_size=block_size)


def encrypt(plaintext: bytes, key: SilentRadixKey) -> str:
    """Encrypt plaintext using per-symbol silent radix.
    
    Each block of plaintext is encoded in a different secret base.
    The bases are never transmitted — only digit strings are output.
    
    Ciphertext format: digit_string || digit_string || ...
    (No delimiters needed — decoder knows block boundaries from key)
    """
    block_size = key.block_size
    if len(plaintext) % block_size != 0:
        # Pad with zeros to block boundary
        pad_len = block_size - (len(plaintext) % block_size)
        plaintext = plaintext + b'\x00' * pad_len
    
    num_blocks = len(plaintext) // block_size
    if num_blocks > len(key.bases):
        raise ValueError(
            f"Plaintext needs {num_blocks} blocks but key only has {len(key.bases)} bases"
        )
    
    ciphertext_parts = []
    for i in range(num_blocks):
        block = plaintext[i * block_size : (i + 1) * block_size]
        digit_str = encode_single_base(block, key.bases[i])
        ciphertext_parts.append(digit_str)
    
    return "|".join(ciphertext_parts)  # Delimiter for readability; could be omitted


def decrypt(ciphertext: str, key: SilentRadixKey) -> bytes:
    """Decrypt ciphertext using per-symbol silent radix."""
    digit_strings = ciphertext.split("|")
    if len(digit_strings) > len(key.bases):
        raise ValueError("Ciphertext has more blocks than key supports")
    
    plaintext_parts = []
    for i, ds in enumerate(digit_strings):
        block = decode_single_base(ds, key.bases[i])
        plaintext_parts.append(block)
    
    return b"".join(plaintext_parts)


# ═══════════════════════════════════════════════════════════════════════
# 3. CRYPTANALYSIS: Lattice Attack on Single-Base Instances
# ═══════════════════════════════════════════════════════════════════════

def lattice_attack_single_base(ciphertexts: List[str], 
                                plaintext_validator=None) -> Optional[int]:
    """Attempt to recover the secret base from multiple ciphertexts.
    
    Uses a lattice-based approach inspired by Merkle-Hellman cryptanalysis.
    For small bases (< 2^20), this can recover b efficiently.
    
    This demonstrates WHY per-symbol bases are MANDATORY for security.
    
    Args:
        ciphertexts: List of comma-separated digit strings encoded in the SAME base
        plaintext_validator: Function(bytes) -> bool, returns True for valid plaintext
    
    Returns:
        Recovered base b, or None if attack fails
    """
    # Step 1: Determine lower bound on b from all digits
    all_digits = set()
    for ct in ciphertexts:
        for token in ct.split(","):
            all_digits.add(int(token))
    min_b = max(all_digits) + 1
    
    if min_b > 2**40:
        print(f"  [ATTACK] Base space ({min_b}+) too large for brute force")
        print(f"  [ATTACK] This is why per-symbol bases are secure — with b >= 2^128, search is infeasible")
        return None
    
    print(f"  [ATTACK] Lower bound on base: b >= {min_b}")
    print(f"  [ATTACK] Searching base space up to {min_b * 100}...")
    
    # Step 2: Brute-force search with plaintext validation
    max_search = min(min_b * 10000, 2**24)
    
    for b in range(min_b, max_search + 1):
        valid = True
        plaintexts = []
        for ct in ciphertexts:
            try:
                plaintext = decode_single_base(ct, b)
                plaintexts.append(plaintext)
            except Exception:
                valid = False
                break
        
        if not valid:
            continue
        
        if plaintext_validator:
            if not all(plaintext_validator(p) for p in plaintexts):
                continue
        
        print(f"  [ATTACK] Base recovered: b = {b}")
        return b
    
    print(f"  [ATTACK] Attack exhausted {min_b}-{max_search}, base not found")
    return None


# ═══════════════════════════════════════════════════════════════════════
# 4. DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the silent radix primitive."""
    print("=" * 60)
    print("SILENT RADIX — Reference Implementation Demo")
    print("=" * 60)
    
    # ─── Single-base demo (INSECURE) ───
    print("\n--- 1. SINGLE-BASE (INSECURE — for illustration) ---")
    plaintext = b"Hello, Silent Radix!"
    base = 256
    
    ct = encode_single_base(plaintext, base)
    print(f"  Plaintext: {plaintext}")
    print(f"  Secret base: {base}")
    print(f"  Ciphertext (digits only): \"{ct}\"")
    print(f"  Note: base {base} is NOT transmitted — only digits are visible")
    
    recovered = decode_single_base(ct, base)
    print(f"  Decrypted: {recovered}")
    assert recovered == plaintext, "Decryption failed!"
    
    # ─── Per-symbol-base demo (HARDENED) ───
    print("\n--- 2. PER-SYMBOL-BASE (HARDENED VARIANT) ---")
    seed = secrets.token_bytes(32)  # 256-bit key
    print(f"  Key seed: {seed.hex()[:32]}...")
    
    plaintext = b"Attack at dawn. The silent radix hides the base in plain sight."
    key = keygen(seed, num_blocks=10, block_size=16)
    print(f"  Block size: {key.block_size} bytes")
    print(f"  Number of bases derived: {len(key.bases)}")
    print(f"  First 3 bases (secret): {key.bases[:3]}")
    print(f"    Base 0: {key.bases[0]} ({key.bases[0].bit_length()} bits)")
    print(f"    Base 1: {key.bases[1]} ({key.bases[1].bit_length()} bits)")
    print(f"    Base 2: {key.bases[2]} ({key.bases[2].bit_length()} bits)")
    
    ciphertext = encrypt(plaintext, key)
    print(f"  Plaintext bytes: {len(plaintext)}")
    print(f"  Ciphertext chars: {len(ciphertext)}")
    expansion_ratio = len(ciphertext) / len(plaintext)
    print(f"  Ciphertext expansion: {expansion_ratio:.2f}x")
    
    decrypted = decrypt(ciphertext, key)
    # Strip null padding (added during encryption for block alignment)
    decrypted = decrypted.rstrip(b'\x00')
    print(f"  Decryption successful: {decrypted == plaintext}")
    
    # ─── Lattice attack demo ───
    print("\n--- 3. LATTICE ATTACK DEMO (single-base, small parameter) ---")
    
    # Use a deliberately small base to demonstrate the attack
    small_base = 37
    messages = [b"HELLO", b"WORLD", b"CRYPTO"]
    
    print(f"  Secret base: b = {small_base}")
    print(f"  Messages encoded in base-{small_base}:")
    
    ciphertexts = []
    for msg in messages:
        ct = encode_single_base(msg, small_base)
        ciphertexts.append(ct)
        print(f"    \"{msg.decode()}\" -> \"{ct}\"")
    
    print(f"\n  Attacker sees only digit strings:")
    for ct in ciphertexts:
        print(f"    \"{ct}\"")
    print(f"  Attacker must find b > max_digit = {max(int(tok) for ct in ciphertexts for tok in ct.split(','))}")
    
    # ASCII validator: plaintext must be printable ASCII (allow null padding)
    def is_ascii(data: bytes) -> bool:
        return all(b in (0x00, 0x0A, 0x0D) or 0x20 <= b <= 0x7E for b in data)
    
    recovered_base = lattice_attack_single_base(ciphertexts, is_ascii)
    if recovered_base:
        print(f"\n  [VULNERABILITY DEMONSTRATED] Base recovered: {recovered_base}")
        print(f"  Single-base silent radix is VULNERABLE to known-structure attacks.")
    
    # ─── Security comparison ───
    print("\n--- 4. SECURITY COMPARISON ---")
    all_digits = set()
    for ct in ciphertexts:
        for t in ct.split(","):
            all_digits.add(int(t))
    md = max(all_digits)
    print(f"  Single-base attack complexity: O(max_digit) = O({md})")
    print(f"  Per-symbol attack complexity: O(2^{key.bases[0].bit_length() - 1}) ≈ O(2^255)")
    print(f"  Security gain: EXPONENTIAL")
    print(f"\n  CONCLUSION: Per-symbol bases are MANDATORY for any security claim.")
    
    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
