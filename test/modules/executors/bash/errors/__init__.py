import pathlib

curr_path = pathlib.Path(__file__).parent.resolve()  # Get current file's dir

files = tuple(curr_path.glob("*.sh"))  # Get all .sh scripts in current dir
