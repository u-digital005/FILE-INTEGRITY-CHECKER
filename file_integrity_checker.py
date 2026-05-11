import hashlib
import os
import json

# step 1- we are making a function of calculating the hash of a file
def calculate_file_hash(file_path):
    # we are using the sha256 algorithm to calculate the hash of the file
    hash_fun=hashlib.sha256()
    # we are opening the file in binary mode and reading it in chunks to calculate the hash
    with open(file_path,'rb') as f:
        chunk=f.read(4096)
        while chunk:
            hash_fun.update(chunk)
            chunk=f.read(4096)
    return hash_fun.hexdigest()
#step 2- then we are making a function to scan the folder and calculate the hash of each file in the folder
def scan_folder(folder_path):
    file_hash={}
    for root,dirs,files in os.walk(folder_path):
        for filename in files:
            full_path=os.path.join(root,filename)
            try:
                hash_value = calculate_file_hash(full_path)
                file_hash[full_path] = hash_value
                print(f"[scanned] {full_path}")
            except:
                print(f"[error] {full_path}")
    return file_hash
# step 3- then we are making a function to save the hash records in a json file
def save_hash_records(hash_record,base_file="hash_records.json"):
    with open(base_file,'w') as f:
        json.dump(hash_record,f,indent=4)
    print(f"\n[saved] Hash records saved to {base_file}")
# step 4- then we are making a function to load the hash records from the json file
def load_hash_records(base_file="hash_records.json"):
    if not os.path.exists(base_file):
        print("[error] no hash records found")
        return None
    with open(base_file,'r') as f:
        return json.load(f)
# step 5- then we are making a function to check the integrity of the files by comparing the current hash with the saved hash
def check_integrity(folder_path,base_file="hash_records.json"):
    old_hashes = load_hash_records(base_file)
    if old_hashes is None:
        return
    
    new_hashes=scan_folder(folder_path)
    print("\n" + "="*50)
    print("             File Integrity report")
    print("="*50)
    issue_found = False
    for file_path,new_hash in new_hashes.items():
        if file_path not in old_hashes:
            print(f"[new file]{file_path}")
            issue_found = True
        elif old_hashes[file_path]!=new_hash:
            print(f"[modified] {file_path}")
            issue_found = True
        else:
            print(f"[ok] {file_path}")
    for file_path in old_hashes:
        if file_path not in new_hashes:
            print(f"[deleted] {file_path}")
            issue_found = True
    print("\n" + "="*50)
    if issue_found:
        print("[alert] changes detected in the files")
    else:
        print("[safe] No integrity issues found")
# step 6- then we are making a main function to run the program
def main():
    print("=" * 50)
    print("Welcome to the File Integrity Checker"
          "\n1. Scan folder and save hash records"
          "\n2. Check integrity of files")
    print("=" * 50)
    folder_path = input("Enter the folder path: ").strip()
    if not os.path.exists(folder_path):
        print("[error] folder path does not exist")
        return
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        hash_records = scan_folder(folder_path)
        save_hash_records(hash_records)
    elif choice == '2':
        check_integrity(folder_path)
        print("Integrity check completed.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
if __name__ == "__main__":    main()