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

    # 2. Check if inkscape is installed (required for svg package)
    inkscape_path = shutil.which("inkscape")
    if not inkscape_path:

        # Try common Windows paths if not in PATH
        possible_paths = [
            Path(r"C:\Program Files\Inkscape\bin\inkscape.exe"),
            Path(r"C:\Program Files\Inkscape\inkscape.exe"),
        ]
        for path in possible_paths:
            if path.exists():
                inkscape_path = str(path)
                # Add it to the current process PATH so pdflatex can find it
                os.environ["PATH"] += os.pathsep + str(path.parent)
                break

    if not inkscape_path:
        print("Error: 'inkscape' is not installed or not in your PATH.", file=sys.stderr)
        print("Required for SVG image conversion in the LaTeX report.", file=sys.stderr)
        sys.exit(1)

    # 3. Cross-platform path handling
    tex_file = Path("docs/final_raport.tex")
    job_name = "docs/Raport Końcowy"

    if not tex_file.exists():
        print(f"Error: Could not find {tex_file} (run the script from the repo root).", file=sys.stderr)
        sys.exit(1)

    # 3. Run the compilation (twice to resolve references)
    cmd = ["pdflatex", "-shell-escape", f"-jobname={job_name}", str(tex_file)]

    # Ensure we run from the script's root directory
    os.chdir(Path(__file__).parent.resolve())

    print(f"Compiling (Pass 1): {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"Compiling (Pass 2 to resolve references): {' '.join(cmd)}")
        result = subprocess.run(cmd)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
