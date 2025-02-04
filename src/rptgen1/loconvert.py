import platform
import subprocess


class LORuntimeException(Exception):
    pass


def loconvert(file_path: str, output_dir: str):
    def soffice(*args):
        exec_bin = (
            "/Applications/LibreOffice.app/Contents/MacOS/soffice"
            if platform.system() == "Darwin"
            else "soffice"
        )
        process = subprocess.run(
            [exec_bin, *args],
            check=False,
            capture_output=True,
        )
        if process.returncode != 0:
            raise LORuntimeException(process.stderr.decode())

    soffice(
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        output_dir,
        file_path,
    )
