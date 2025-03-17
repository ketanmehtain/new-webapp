import os
import subprocess
import sys
from config import AZURE_DB_CONFIG, GCP_DB_CONFIG

def dump_database():
    backup_file = "backup.sql"
    env = os.environ.copy()
    env["PGPASSWORD"] = AZURE_DB_CONFIG["password"]
    command = [
        "pg_dump", 
        "-h", AZURE_DB_CONFIG["host"], 
        "-p", str(AZURE_DB_CONFIG["port"]), 
        "-U", AZURE_DB_CONFIG["user"], 
        "-d", AZURE_DB_CONFIG["dbname"]
        ]
    try:
        with open(backup_file, "w") as output_file:
            subprocess.run(command, env=env, stdout=output_file, stderr=subprocess.PIPE, check=True)
        print("Database Dump successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error dumping database: {e.stderr.decode()}")
        exit(1)

def restore_database():
    backup_file = "backup.sql"
    env = os.environ.copy()
    env["PGPASSWORD"] = GCP_DB_CONFIG["password"]
    command = [
        "psql", 
        "-h", GCP_DB_CONFIG["host"], 
        "-p", str(GCP_DB_CONFIG["port"]), 
        "-U", GCP_DB_CONFIG["user"], 
        "-d", GCP_DB_CONFIG["dbname"], 
        "-f", backup_file
        ]
    try:
        subprocess.run(command, env=env, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Database Restore successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error restore database: {e.stderr.decode()}")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["dump", "restore"]:
        print("Usage: python script.py [dump|restore]")
        exit(1)
    
    if sys.argv[1] == "dump":
        dump_database()
    else:
        restore_database()
