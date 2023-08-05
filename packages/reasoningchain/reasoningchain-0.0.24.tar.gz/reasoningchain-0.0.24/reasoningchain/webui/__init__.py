
import os
import sys
import click

@click.command()
@click.option("--port", "-p", "port", type=int, default=8501, required=False)
def main(port:int) -> int:
    import signal
    import subprocess

    def signal_handler(signum, frame):
        print(f"Received signal {signum}. Terminating child process...")
        os.kill(os.getpid(), signal.SIGTERM)

    signal.signal(signal.SIGINT, signal_handler)

    uipath = os.path.join(os.path.abspath(__file__ + '/..'), "stui.py")

    try:
        p = subprocess.Popen(["streamlit", "run", uipath, "--server.port", str(port)])
        print("Web UI process:", p, file=sys.stderr)
        while p.poll() is None:
            p.wait()
        print(f"WebUI process exited with code:{p.returncode}", file=sys.stderr)
        return p.returncode
    except KeyboardInterrupt:
        print("\nMain process interrupted. Terminating...", file=sys.stderr)
        os.kill(p.pid, signal.SIGTERM) 
        return -1

if __name__ == '__main__':
    main()

