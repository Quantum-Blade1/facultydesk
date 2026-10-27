import subprocess
import sys

def main():
    print("[*] Initiating FacultyDesk PostgreSQL backup to MinIO...")
    cmd = [
        "docker", "compose", "exec", "-T", "backend",
        "python", "-c",
        "from app.infrastructure.storage.backup_service import BackupService; key = BackupService().create_backup(); print(f'Backup complete: {key}')"
    ]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[!] Backup failed!", file=sys.stderr)
        sys.exit(res.returncode)
    print("[✓] Backup successfully saved to MinIO bucket 'backups' with 14-day retention.")

if __name__ == "__main__":
    main()
