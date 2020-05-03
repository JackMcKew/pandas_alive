OUTPUT_TYPE: str = "file"
OUTPUT_FILENAME: str = ""


def output_file(filename: str) -> None:

    if len(filename) <= 0:
        raise ValueError("Specify filename")

    if (
        isinstance(filename, str)
        and "." not in filename
        or len(filename.split(".")[1]) <= 0
    ):
        raise ValueError("`filename` must be provided & have an extension")

    global OUTPUT_TYPE
    global OUTPUT_FILENAME
    OUTPUT_TYPE = "file"
    OUTPUT_FILENAME = filename


def output_html():

    global OUTPUT_TYPE
    OUTPUT_TYPE = "html"
