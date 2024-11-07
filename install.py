import subprocess

def run_vscode_task():
    """Ejecuta la tarea de VSCode"""
    print("Ejecutando tarea de VSCode...")
    subprocess.run(["code", "--task", "tasks.json"])

if __name__ == "__main__":
    run_vscode_task()
