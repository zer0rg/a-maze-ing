class MazeConfig:

    def __init__(self):
        try:
            self.parse_file()
            self.check_config()
        except Exception as e:
            print(f"Config File Error: {e}")


    def parse_file(self) -> None:
        with open("config.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                self.line_processor(key, value)


    def check_config(self) -> None:
        if not hasattr(self, 'width') or not self.width:
            raise Exception("Value WIDTH is needed!")
        if not hasattr(self, 'height') or not self.height:
            raise Exception("Value HEIGHT is needed!")
        if not hasattr(self, 'entry') or not isinstance(self.entry, dict):
            raise Exception("Value ENTRY is needed and must be a valid coordinate pair!")
        if not hasattr(self, 'exit') or not isinstance(self.exit, dict):
            raise Exception("Value EXIT is needed and must be a valid coordinate pair!")
        if not hasattr(self, 'perfect'):
            raise Exception("Value PERFECT is needed!")
        if not hasattr(self, 'output_file') or not self.output_file:
            raise Exception("Value OUTPUT_FILE is needed!")


    def line_processor(self, key : str, value : str) -> None:
        try:
            if key == "WIDTH":
                self.width = int(value)
            elif key == "HEIGHT":
                self.height = int(value)
            elif key == "ENTRY":
                x, y = value.split(",")
                self.entry : dict = {
                    x : int(x),
                    y : int(y)
                }
            elif key == "EXIT":
                x, y = value.split(",")
                self.exit : dict = {
                    x : int(x),
                    y : int(y)
                }
            elif key == "PERFECT":
                self.perfect = value == "True"
            elif key == "OUTPUT_FILE":
                self.output_file = value
            else:
                raise ValueError(f"Unknown configuration key: {key}")
        except Exception as e:
            raise Exception(f"Error processing key '{key}': {e}")