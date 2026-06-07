import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():

    # 1. Check if pdflatex is installed
    if not shutil.which("pdflatex"):
        print("Error: 'pdflatex' is not installed or not in your PATH.", file=sys.stderr)
        sys.exit(1)

    # 2. Cross-platform path handling (Python and TeX handle '/' everywhere)
    tex_file = Path("docs/final_raport.tex")
    job_name = "docs/Final Raport"

    if not tex_file.exists():
        print(f"Error: Could not find {tex_file} (run the script from the repo root).", file=sys.stderr)
        sys.exit(1)

    # 3. Run the compilation
    cmd = ["pdflatex", f"-jobname={job_name}", str(tex_file)]
    print(f"Compiling: {' '.join(cmd)}")

    # Ensure we run from the script's root directory
    os.chdir(Path(__file__).parent.resolve())

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
