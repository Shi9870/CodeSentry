import math
import re

def shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = data.count(x) / len(data)
        entropy += - p_x * math.log2(p_x)
    return entropy

def extract_features(text: str):
    length = len(text)
    if length == 0:
        return [0] * 7

    # 1. Entropy
    entropy = shannon_entropy(text)

    # 2. Character Ratios
    digit_ratio = sum(c.isdigit() for c in text) / length
    upper_ratio = sum(c.isupper() for c in text) / length
    symbol_ratio = sum(not c.isalnum() for c in text) / length

    # 3. Prefix Check (Logic Update)
    # We remove the * 0.3 multiplier to let the model learn the weight
    has_known_prefix = 1.0 if text.startswith(("sk-", "ghp_", "AKIA", "xoxb-", "AIza")) else 0.0

    # 4. Length Ratio (Normalized)
    # Focus on standard key lengths (20-80 chars)
    # If len is between 20 and 80, this score is higher
    len_score = 1.0 if 20 <= length <= 80 else (0.5 if length > 80 else 0.2)

    return [
        entropy,
        length,
        digit_ratio,
        upper_ratio,
        symbol_ratio,
        has_known_prefix, # Prefix Score
        len_score         # Length Score (Replaced Prefix Len Ratio)
    ]