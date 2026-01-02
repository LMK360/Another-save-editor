#!/usr/bin/env python3
import clr
import sys
import os

clr.AddReference("System.Runtime.Serialization.Formatters")
clr.AddReference("mscorlib")

from System.IO import FileStream, FileMode
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter

------------------------

Load / Save

------------------------

def load_save(path):
bf = BinaryFormatter()
with FileStream(path, FileMode.Open, FileMode.Read) as fs:
return bf.Deserialize(fs)

def save_save(data, path):
bf = BinaryFormatter()
with FileStream(path, FileMode.Create, FileMode.Write) as fs:
bf.Serialize(fs, data)
print(f"[✓] Saved: {path}")

------------------------

Display

------------------------

def show(data):
print("\n====== SAVE DATA ======")
for attr in dir(data):
if not attr.startswith("_"):
try:
val = getattr(data, attr)
if not callable(val):
print(f"{attr}: {val}")
except:
pass
print("=======================\n")

------------------------

Editors

------------------------

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

------------------------

CLI

------------------------

def parse_value(v):
if v.lower() in ("true", "false"):
return v.lower() == "true"
if v.isdigit():
return int(v)
try:
return float(v)
except:
return v

def main():
if len(sys.argv) < 3:
print("""
Usage:
svd-editor view <file.svd>
svd-editor set <file.svd> <field> <value>
svd-editor set-events <file.svd> <value>
""")
sys.exit(1)

cmd = sys.argv[1]  
file = sys.argv[2]  

if not os.path.exists(file):  
    print("[!] File not found")  
    sys.exit(1)  

data = load_save(file)  

if cmd == "view":  
    show(data)  

elif cmd == "set":  
    field = sys.argv[3]  
    value = parse_value(sys.argv[4])  
    set_field(data, field, value)  
    save_save(data, file)  

elif cmd == "set-events":  
    value = parse_value(sys.argv[3])  
    set_all_events(data, value)  
    save_save(data, file)  

else:  
    print("[!] Unknown command")

if name == "main":
main()
