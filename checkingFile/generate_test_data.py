import os
import random
import string
import json
import time
import uuid

# ==========================================
# Configuration
# ==========================================
TARGET_DIR = "stress_test_data"
TOTAL_FILES = 2000          # Total number of files
LEAK_PROBABILITY = 0.15     # Increased to 15% to ensure we see enough variety
MAX_DEPTH = 5               
MAX_SUBDIRS = 3             

# Distribution of risk levels within the leaks
# Must sum to 1.0
RISK_DISTRIBUTION = {
    "CRITICAL": 0.1,  # 10% (Rare)
    "HIGH": 0.2,      # 20%
    "MEDIUM": 0.3,    # 30%
    "LOW": 0.4        # 40% (Most common noise)
}

# ==========================================
# Fake Data Patterns
# ==========================================

# 1. CRITICAL (Specific Patterns + High Entropy)
PATTERNS_CRITICAL = {
    "AWS_ACCESS_KEY": lambda: "AKIA" + "".join(random.choices(string.ascii_uppercase + string.digits, k=16)),
    "OPENAI_API_KEY": lambda: "sk-" + "".join(random.choices(string.ascii_letters + string.digits, k=48)),
    "RSA_PRIVATE_KEY": lambda: "-----BEGIN RSA PRIVATE KEY-----\n" + "".join(random.choices(string.ascii_letters + string.digits + "+/", k=100))
}

# 2. HIGH (High Entropy but generic)
PATTERNS_HIGH = {
    "AWS_SECRET_KEY": lambda: "".join(random.choices(string.ascii_letters + string.digits + "/+", k=40)),
    "GENERIC_SECRET_64": lambda: "".join(random.choices(string.ascii_letters + string.digits, k=64)),
    "SLACK_TOKEN": lambda: "xoxb-" + "".join(random.choices(string.digits, k=10)) + "-" + "".join(random.choices(string.ascii_letters + string.digits, k=24))
}

# 3. MEDIUM (Medium Entropy, Hex strings, Base64)
PATTERNS_MEDIUM = {
    "GENERIC_TOKEN_32": lambda: "".join(random.choices(string.ascii_letters + string.digits, k=32)),
    "MD5_HASH": lambda: "".join(random.choices("abcdef0123456789", k=32)), # Looks like a secret but might be just a hash
    "INTERNAL_ID": lambda: "ID-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=20))
}

# 4. LOW (Keywords present but Low Entropy / Common IDs)
PATTERNS_LOW = {
    "SIMPLE_PASSWORD": lambda: random.choice(["password123", "admin", "12345678", "qwerty", "changeme"]),
    "SHORT_API_KEY": lambda: "key_" + "".join(random.choices(string.digits, k=6)),
    "UUID": lambda: str(uuid.uuid4()), # UUIDs often generate false positives in entropy checks
    "LOCAL_IP": lambda: f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
}

EXTENSIONS = ['.py', '.js', '.json', '.env', '.txt', '.yml']

# ==========================================
# Generators
# ==========================================

def get_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_safe_content(ext):
    """Generates harmless content."""
    if ext == '.json':
        return json.dumps({"version": "1.0.0", "name": get_random_string()}, indent=2)
    elif ext == '.env':
        return f"HOST=localhost\nPORT=8080\nENV=production"
    elif ext == '.py':
        return f"def main():\n    print('Hello World')\n    # This is a safe comment"
    else:
        return f"Just some logs: {get_random_string(50)}"

def generate_leak_content(ext, risk_level):
    """Generates content based on the requested risk level."""
    
    # Select pattern pool based on risk
    if risk_level == "CRITICAL":
        pool = PATTERNS_CRITICAL
    elif risk_level == "HIGH":
        pool = PATTERNS_HIGH
    elif risk_level == "MEDIUM":
        pool = PATTERNS_MEDIUM
    else:
        pool = PATTERNS_LOW
    
    key_type = random.choice(list(pool.keys()))
    secret = pool[key_type]()
    
    # Format based on file type to make it look realistic
    if ext == '.json':
        return json.dumps({key_type.lower(): secret, "risk_test": risk_level}, indent=2)
    elif ext == '.env':
        return f"# Risk Level: {risk_level}\n{key_type}={secret}"
    elif ext == '.py':
        # Python often assigns secrets to variables
        var_name = key_type.lower()
        return f"# Risk: {risk_level}\n{var_name} = '{secret}'\nconnect({var_name})"
    else:
        return f"Found {risk_level} secret: {key_type} = {secret}"

def create_random_directory_structure(base_path, current_depth=0):
    if current_depth >= MAX_DEPTH:
        return [base_path]
    paths = [base_path]
    if random.random() > 0.3:
        num_subdirs = random.randint(1, MAX_SUBDIRS)
        for _ in range(num_subdirs):
            subdir = os.path.join(base_path, f"dir_{get_random_string(6)}")
            if not os.path.exists(subdir):
                os.makedirs(subdir)
                paths.extend(create_random_directory_structure(subdir, current_depth + 1))
    return paths

def main():
    print(f"[*] Starting ADVANCED stress test data generation...")
    print(f"[*] Target Directory: {TARGET_DIR}")
    
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    all_dirs = create_random_directory_structure(TARGET_DIR)
    
    stats = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "SAFE": 0}
    
    start_time = time.time()
    
    for i in range(TOTAL_FILES):
        target_folder = random.choice(all_dirs)
        ext = random.choice(EXTENSIONS)
        filename = f"file_{i}_{get_random_string(5)}{ext}"
        file_path = os.path.join(target_folder, filename)
        
        # Determine if this file is a leak
        if random.random() < LEAK_PROBABILITY:
            # Determine Risk Level based on distribution
            rand_r = random.random()
            if rand_r < RISK_DISTRIBUTION["CRITICAL"]:
                risk = "CRITICAL"
            elif rand_r < (RISK_DISTRIBUTION["CRITICAL"] + RISK_DISTRIBUTION["HIGH"]):
                risk = "HIGH"
            elif rand_r < (RISK_DISTRIBUTION["CRITICAL"] + RISK_DISTRIBUTION["HIGH"] + RISK_DISTRIBUTION["MEDIUM"]):
                risk = "MEDIUM"
            else:
                risk = "LOW"
                
            content = generate_leak_content(ext, risk)
            stats[risk] += 1
        else:
            content = generate_safe_content(ext)
            stats["SAFE"] += 1
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        if (i + 1) % 200 == 0:
            print(f"    - Generated {i + 1} files...")

    elapsed = time.time() - start_time
    print(f"\n[SUCCESS] Generated {TOTAL_FILES} files in {elapsed:.2f}s")
    print("-" * 30)
    print("Distribution Summary:")
    for k, v in stats.items():
        print(f"  [{k}]: {v} files")
    print("-" * 30)
    print(f"[NEXT] Select '{os.path.abspath(TARGET_DIR)}' in CodeSentry to test!")

if __name__ == "__main__":
    main()