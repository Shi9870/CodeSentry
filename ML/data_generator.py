import pandas as pd
import random
import string
import secrets
import hashlib
import uuid
import sys
import os

OPENAI_PREFIX = "sk-"
GITHUB_PREFIX = "ghp_"
AWS_PREFIX = "AKIA"
ALNUM = string.ascii_letters + string.digits

def gen_active_like_secret():
    """Label = 1: High risk, looks real and could be active"""
    kind = random.choice(["openai", "github", "aws"])

    if kind == "openai":
        return OPENAI_PREFIX + ''.join(random.choices(ALNUM, k=48)), 1
    if kind == "github":
        return GITHUB_PREFIX + ''.join(random.choices(ALNUM, k=36)), 1
    if kind == "aws":
        return AWS_PREFIX + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)), 1

def gen_revoked_or_fake_but_valid_format():
    """Label = 0: Correct format, but revoked or fake (Hard Negative)"""
    kind = random.choice(["openai", "github", "aws"])

    if kind == "openai":
        return OPENAI_PREFIX + ''.join(random.choices(ALNUM, k=48)), 0
    if kind == "github":
        return GITHUB_PREFIX + ''.join(random.choices(ALNUM, k=36)), 0
    if kind == "aws":
        return AWS_PREFIX + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)), 0

def gen_low_risk_noise():
    """Label = 0: Obvious noise or common placeholders"""
    text = random.choice([
        "your_api_key_here",
        "example_token",
        "sk-example-123456",
        "TODO: replace this",
        secrets.token_urlsafe(random.randint(10, 50)), # Random Base64 string
        hashlib.sha256(secrets.token_bytes(32)).hexdigest(), # Hash
        str(uuid.uuid4()) # UUID
    ])
    return text, 0

def generate_dataset(n_samples=5000):
    data = []
    
    print(f"Generating dataset with {n_samples} samples...")
    
    for _ in range(n_samples):
        roll = random.random()

        if roll < 0.35:
            # 35% Active/Real-looking secrets
            text, label = gen_active_like_secret()
        elif roll < 0.70:
            # 35% Format-compliant but fake/revoked (Hard Negatives)
            text, label = gen_revoked_or_fake_but_valid_format()
        else:
            # 30% Noise
            text, label = gen_low_risk_noise()
            
        data.append({"text": text, "label": label})

    df = pd.DataFrame(data)
    
    # Save the file
    output_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset created: {output_path}")
    print(df['label'].value_counts())
    return df

if __name__ == "__main__":
    generate_dataset()