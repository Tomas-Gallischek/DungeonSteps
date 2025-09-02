import subprocess

def migrace():
    try:
        subprocess.run(["python", "./manage.py", "makemigrations"], check=True)
        print("MAKE MIGRATIONS ✅'.")
        subprocess.run(["python", "./manage.py", "migrate"], check=True)
        print("MIGRATE ✅'.")
        print("✅ VŠE ÚSPĚŠNĚ ZMIGROVÁNO")
    except subprocess.CalledProcessError as e:
        print("❌ Něco se nepovedlo:", e)

if __name__ == "__main__":
    migrace()
