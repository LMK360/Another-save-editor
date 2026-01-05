#!/usr/bin/env python3
import sys
import os
import shutil
import UnityPy

# ------------------------
# Backup function
# ------------------------
def backup(path):
    bak = path + ".bak"
    if not os.path.exists(bak):
        shutil.copy(path, bak)
        print(f"[+] Backup created: {bak}")

# ------------------------
# Load / Save
# ------------------------
def load_save(path):
    if not os.path.exists(path):
        print(f"[!] File not found: {path}")
        sys.exit(1)
    env = UnityPy.load(path)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            try:
                data = obj.read_typetree()
                return data, env, obj
            except Exception as e:
                print(f"[!] Failed to read MonoBehaviour data: {e}")
                sys.exit(1)
    print("[!] No MonoBehaviour data found in save")
    sys.exit(1)

def save_save(data, env, obj, path):
    try:
        obj.save_typetree(data)
        env.save(path)
        print(f"[✓] Saved: {path}")
    except Exception as e:
        print(f"[!] Failed to save file: {e}")
        sys.exit(1)

# ------------------------
# Display function
# ------------------------
def show(data):
    print("\n====== SAVE DATA ======")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print("[!] Data format unexpected")
    print("=======================\n")

# ------------------------
# Editors
# ------------------------
def auto_cast(value):
    if isinstance(value, str):
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value
    return value

def set_field(data, field, value):
    if not isinstance(data, dict) or field not in data:
        print(f"[!] Field '{field}' not found")
        return
    data[field] = value
    print(f"[✓] {field} set to {value}")

def set_all_events(data, value):
    if not isinstance(data, dict) or "eventData" not in data:
        print("[!] eventData not found")
        return
    for i in range(len(data["eventData"])):
        data["eventData"][i] = value
    print(f"[✓] All eventData values set to {value}")

# ------------------------
# CLI
# ------------------------
def main():
    if len(sys.argv) < 3:
        print("""
Usage:
  svd-editor view <file.svd>
  svd-editor set <file.svd> <field> <value>
  svd-editor set-events <file.svd> <value>
""")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    file_path = sys.argv[2]

    # Backup
    backup(file_path)

    data, env, obj = load_save(file_path)

    if cmd == "view":
        show(data)

    elif cmd == "set":
        if len(sys.argv) != 5:
            print("Usage: svd-editor set <file.svd> <field> <value>")
            sys.exit(1)
        field = sys.argv[3]
        value = auto_cast(sys.argv[4])
        set_field(data, field, value)
        save_save(data, env, obj, file_path)

    elif cmd == "set-events":
        if len(sys.argv) != 4:
            print("Usage: svd-editor set-events <file.svd> <value>")
            sys.exit(1)
        value = auto_cast(sys.argv[3])
        set_all_events(data, value)
        save_save(data, env, obj, file_path)

    else:
        print("[!] Unknown command")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    main()    print("\n====== SAVE DATA ======")
    for k, v in data.items():
        print(f"{k}: {v}")
    print("=======================\n")

# ------------------------
# Editors
# ------------------------
def auto_cast(value):
    if isinstance(value, str):
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except:
            return value
    return value

def set_field(data, field, value):
    if field not in data:
        print(f"[!] Field '{field}' not found")
        return
    data[field] = value
    print(f"[✓] {field} set to {value}")

def set_all_events(data, value):
    if "eventData" not in data:
        print("[!] eventData not found")
        return
    for i in range(len(data["eventData"])):
        data["eventData"][i] = value
    print(f"[✓] All eventData values set to {value}")

# ------------------------
# CLI
# ------------------------
def main():
    if len(sys.argv) < 3:
        print("""
Usage:
  svd-editor view <file.svd>
  svd-editor set <file.svd> <field> <value>
  svd-editor set-events <file.svd> <value>
""")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    file_path = sys.argv[2]

    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        sys.exit(1)

    # Backup
    backup(file_path)

    data, env, obj = load_save(file_path)

    if cmd == "view":
        show(data)

    elif cmd == "set":
        if len(sys.argv) != 5:
            print("Usage: svd-editor set <file.svd> <field> <value>")
            sys.exit(1)
        field = sys.argv[3]
        value = auto_cast(sys.argv[4])
        set_field(data, field, value)
        save_save(data, env, obj, file_path)

    elif cmd == "set-events":
        if len(sys.argv) != 4:
            print("Usage: svd-editor set-events <file.svd> <value>")
            sys.exit(1)
        value = auto_cast(sys.argv[3])
        set_all_events(data, value)
        save_save(data, env, obj, file_path)

    else:
        print("[!] Unknown command")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    main()
