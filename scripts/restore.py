import subprocess
import sys

def main():
    backup_key = sys.argv[1] if len(sys.argv) > 1 else "None"
    print(f"[*] Restoring FacultyDesk database from MinIO backup (key: {backup_key})...")
    key_arg = f"'{backup_key}'" if backup_key != "None" else "None"
    cmd = [
        "docker", "compose", "exec", "-T", "backend",
        "python", "-c",
        f"from app.infrastructure.storage.backup_service import BackupService; BackupService().restore_backup({key_arg}); print('Restore completed successfully')"
    ]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[!] Restore failed!", file=sys.stderr)
        sys.exit(res.returncode)
    print("[✓] Database restore verified successfully.")

if __name__ == "__main__":
    main()
