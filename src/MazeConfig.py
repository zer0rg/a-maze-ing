class MazeConfig:

    def __init__(self):
        try:
            self.parse_file()
        except Exception as e:
            print(f"Config File Error: {e}")

    def parse_file(self):
        with open("config.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                self.line_processor(key, value)

    def line_processor(self, key, value):
        try:
            if key == "WIDTH":
                self.width = int(value)
            elif key == "HEIGHT":
                self.height = int(value)
            elif key == "ENTRY":
                self.entry = float(value)
            elif key == "EXIT":
                self.exit = float(value)
            elif key == "PERFECT":
                self.perfect = value == "True"
            elif key == "OUTPUT_FILE":
                self.output_file = value
            else:
                raise ValueError(f"Unknown configuration key: {key}")
        except Exception as e:
            raise Exception(f"Error processing key '{key}': {e}")