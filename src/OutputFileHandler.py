from self_typing.maze import MazeBoard


class OutputFileHandler:

    @staticmethod
    def save_file(file_name: str, maze: MazeBoard):
        with open(file_name, "w") as file:
            file.write("Output bitch")
