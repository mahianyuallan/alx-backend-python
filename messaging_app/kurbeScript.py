#!/usr/bin/env python3
import subprocess
import sys
import shutil
import platform

def run_command(cmd, check=True):
    """Run a shell command and print output."""
    try:
        result = subprocess.run(cmd, shell=True, text=True,
                                capture_output=True, check=check)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        if check:
            sys.exit(1)

def ensure_minikube_installed():
    """Check and guide installation of Minikube."""
    print("=== Checking if Minikube is installed ===")
    if shutil.which("minikube"):
        print("Minikube is already installed.")
        return

    os_type = platform.system()
    if os_type == "Windows":
        print("Minikube not found.")
        print("Install it with Chocolatey (recommended):")
        print("    choco install minikube")
        print("Or download from: https://minikube.sigs.k8s.io/docs/start/")
        sys.exit(1)
    else:
        print("This script currently only guides Windows installation.")
        sys.exit(1)

def ensure_kubectl_installed():
    """Check and guide kubectl installation."""
    print("=== Checking if kubectl is installed ===")
    if shutil.which("kubectl"):
        print("kubectl is already installed.")
        return

    print("kubectl not found.")
    print("Install it with Chocolatey (recommended):")
    print("    choco install kubernetes-cli")
    print("Or download from: https://kubernetes.io/docs/tasks/tools/")
    sys.exit(1)

def start_cluster():
    print("=== Starting Minikube cluster ===")
    run_command("minikube start")

def verify_cluster():
    print("=== Verifying cluster with kubectl cluster-info ===")
    run_command("kubectl cluster-info")

def list_pods():
    print("=== Listing all pods in all namespaces ===")
    run_command("kubectl get pods -A")

def main():
    ensure_minikube_installed()
    ensure_kubectl_installed()
    start_cluster()
    verify_cluster()
    list_pods()

if __name__ == "__main__":
    main()
