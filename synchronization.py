import argparse
import hashlib
import datetime
import os
import shutil
import time


def calculate_md5(file_path):
    with open(file_path, 'rb') as file_data:
        return hashlib.md5(file_data.read()).hexdigest()


def synchronization(source_folder, replica_folder, log_file):
    with open(log_file, 'a') as log:

        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        log.write(f"{timestamp} Synchronization started.\n")

        source_contents = set(os.listdir(source_folder))
        replica_contents = set(os.listdir(replica_folder))


        source_hashes = {file: calculate_md5(os.path.join(source_folder,file))
                         for file in source_contents if os.path.isfile(os.path.join(source_folder,file))}

        replica_hashes = {file: calculate_md5(os.path.join(replica_folder,file))
                          for file in replica_contents if os.path.isfile(os.path.join(replica_folder,file))}

        files_to_copy = []
        for file in source_contents:
            if file not in replica_contents:
                status ="New"
            elif source_hashes[file] != replica_hashes.get(file):
                status = "Modified"
            else:
                status ="Unchanged"

            files_to_copy.append((file,status))

        # Add status for files in replica but not in source
        for file in replica_contents:
            if file not in source_contents:
                files_to_copy.append((file, "Deleted"))

        # Process files based on their status (copy or delete)
        for file, status in files_to_copy:
            source_path = os.path.join(source_folder,file)
            replica_path = os.path.join(replica_folder,file)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if status == "Deleted":
                os.remove(replica_path)
                log.write(f"[{timestamp}] The file {replica_path} is removed.\n")
            else:
                shutil.copy2(source_path, replica_path)
                if status != "Unchanged":
                    log.write(f"[{timestamp}] The file {source_path} is {status} and copied to {replica_path}\n")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] Synchronization completed.\n\n")

def main():
    print("Main function called.")
    parser = argparse.ArgumentParser(description='Folder Synchronization Program')
    parser.add_argument('source_folder', help= ' Path to the source folder')
    parser.add_argument('replica_folder', help= ' Path to the replica folder')
    parser.add_argument('sync_period', type=int, nargs='?', default=60, help='Synchronization period')
    parser.add_argument('log_file', help= ' Path to the log file')

    args = parser.parse_args()

    while True:
        try:
            synchronization(args.source_folder, args.replica_folder, args.log_file)
            time.sleep(args.sync_period)
        except Exception as e:
            print(f"Error during synchronization: {str(e)}")

if __name__ == "__main__":
    main()