#!/usr/bin/env python3
import clr
import sys
import os
import shutil

# ------------------------
# .NET references
# ------------------------
clr.AddReference("System.Runtime.Serialization.Formatters")
clr.AddReference("mscorlib")

from System.IO import FileStream, FileMode
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter

# ------------------------
# Load / Save functions
# ------------------------
def load_save(path):
    bf = BinaryFormatter()
    with FileStream(path, FileMode.Open, FileMode.Read) as fs:
        return bf.Deserialize(fs)

def save_save(data, path):
    bf = BinaryFormatter()
    with FileStream(path, FileMode.Create, FileMode.Write) as fs:
        bf.Serialize(fs, data)
    print(f"[✓] Saved: {path}")

def backup(path):
    bak = path + ".bak"
    if not os.path.exists(bak):
        shutil.copy(path, bak)
        print(f"[+] Backup created: {bak}")

# ------------------------
# Display function
# ------------------------
def show(data):
    print("\n====== SAVE DATA ======")
    for attr in dir(data):
        if attr.startswith("_"):
            continue
        try:
            val = getattr(data, attr)
            if not callable(val):
                print(f"{attr}: {val}")
        except:
            pass
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
    if not hasattr(data, field):
        print(f"[!] Field '{field}' not found")
        return
    setattr(data, field, value)
    print(f"[✓] {field} set to {value}")

def set_all_events(data, value):
    if not hasattr(data, "eventData"):
        print("[!] eventData not found")
        return
    for i in range(len(data.eventData)):
        data.eventData[i] = value
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

    # Backup before editing
    backup(file_path)

    data = load_save(file_path)

    if cmd == "view":
        show(data)

    elif cmd == "set":
        if len(sys.argv) != 5:
            print("Usage: svd-editor set <file.svd> <field> <value>")
            sys.exit(1)
        field = sys.argv[3]
        value = auto_cast(sys.argv[4])
        set_field(data, field, value)
        save_save(data, file_path)

    elif cmd == "set-events":
        if len(sys.argv) != 4:
            print("Usage: svd-editor set-events <file.svd> <value>")
            sys.exit(1)
        value = auto_cast(sys.argv[3])
        set_all_events(data, value)
        save_save(data, file_path)

    else:
        print("[!] Unknown command")

# Entry point
if __name__ == "__main__":
    main()
