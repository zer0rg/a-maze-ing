from self_typing import MazeBoard
from mlx import Mlx


class MazeRenderer:

    def __init__(self, width: int, height: int):
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, width,
                                               height, "A_maze_ing")
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self.close_window, None)

    def render(self, board: MazeBoard):
        print("MAZE: ", board)

    def close_window(self):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
