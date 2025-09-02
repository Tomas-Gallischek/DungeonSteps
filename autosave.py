import subprocess

def git_autosave():
    try:
        # Přidání všech změn
        subprocess.run(["git", "add", "."], check=True)

        # Commit se zprávou "autosave"
        subprocess.run(["git", "commit", "-m", "autosave"], check=True)

        # Push do origin (na aktuální větev)
        subprocess.run(["git", "push"], check=True)

        # vymazání konzole
        subprocess.run("cls", shell=True)

        print("✅ Projekt byl úspěšně uložen na GitHub jako 'autosave'.")
    except subprocess.CalledProcessError as e:
        print("❌ Něco se nepovedlo:", e)

if __name__ == "__main__":
    git_autosave()
