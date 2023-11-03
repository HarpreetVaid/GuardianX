import psutil
import os
import sqlite3
import hashlib

conn = sqlite3.connect('virus-hashes.db')
cursor = conn.cursor()


def list_partitions():
    partitions = psutil.disk_partitions(all=True)
    partition_mountpoints = []
    for partition in partitions:
        partition_mountpoints.append(partition.mountpoint)
    return partition_mountpoints

def check_virus(directory):
    # List all files and subdirectories in the current directory
    file_ptr = open("virus_path",'w')
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            # If it's a directory, recursively traverse it
            if os.path.isdir(item_path):
                check_virus(item_path)
            # If it's a file, do something with it (e.g., print its path)
            if os.path.isfile(item_path):
                print("File:", item_path.encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
                virus_result = convert_hash(item_path.encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
                if virus_result is None:
                    continue
                else :
                    file_ptr.writelines(f"Path is {virus_result[0]}, name is {virus_result[1]}, date of report is {virus_result[2]} ")
    except Exception as e:
        pass

    file_ptr.close()


def check_hash(hash):
    global cursor
    query = "SELECT * FROM data_hashes WHERE sha256_hash = ?"
    cursor.execute(query, (hash,))
    results = cursor.fetchall()
    # Check if there are any matching files
    if results:
        return True
    else:
        return False

def get_hash_info(hash):
    global cursor
    query = "SELECT * FROM data_hashes WHERE sha256_hash = ?"
    cursor.execute(query, (hash,))
    return cursor.fetchall()

def convert_hash(path):
    try:
       with open(path, 'rb') as f:
        hashsha256 = hashlib.sha256()
        for data in iter(lambda :f.read(8192), b'') :
            hashsha256.update(data)
        hash_file = hashsha256.digest()
        if check_hash(hash_file) :
            return get_hash_info(hash_file)
        else:
            return None
    except :
        return None 
    
for path in list_partitions() :
    check_virus(path)
conn.commit()
conn.close()

