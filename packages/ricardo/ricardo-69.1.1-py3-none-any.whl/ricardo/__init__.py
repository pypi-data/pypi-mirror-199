import io
import pathlib


def get_a_ricardo() -> io.BytesIO:
    return io.BytesIO(pathlib.Path(__file__, "..", "assets", "ricardo.jpg").resolve().read_bytes())
