"""Renderer module for maze visualization using MLX library."""

from typing import Any
from custom_typing import MazeBoard
from custom_typing.maze import NORTH, SOUTH, EAST, WEST
from src.Config import Config
from src.Cell import Cell
from src.Generator import Generator
from mlx import Mlx
import ctypes
import time


class Renderer:
    """Handles maze rendering and visualization."""

    def __init__(self, config: Config, generator: Generator):
        """Initialize the renderer with configuration and generator."""
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.screen_size = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        self.config = config
        self.width, self.height = self.get_window_size()

        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, self.width,
                                               self.height, "A_maze_ing")

        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._setup_hooks()

        self.running = True

        self.generator: Generator = generator
        self.board: MazeBoard | None = generator.maze

        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.width,
                                              self.height)
        addr_info = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.img_buffer = (
            ctypes.c_ubyte * (self.width * self.height * 4)).from_buffer(
                addr_info[0])

        # Estados de renderizado
        self.wall_thickness = 2
        self.wall_color = 0xFFFFFF
        self.bg_color = 0x000000
        self.visited_color = 0x000000
        self.start_color = 0x00FF00
        self.end_color = 0xFE00000

        # Estado de generación
        self.generation_generator: Any = None
        self.generation_complete = False
        self.generation_speed = 0.01
        self.last_generation_time: float = 0.0

        # Estado de solución
        self.solving_generator: Any = None
        self.solving_complete = False
        self.solving_speed = 0.001
        self.last_solving_time: float = 0.0

        # Colores para el solver
        self.exploring_start_color = 0x0000FF  # Azul
        self.exploring_goal_color = 0xFFFF00   # Amarillo
        self.visiting_start_color = 0x4444FF   # Azul claro
        self.visiting_goal_color = 0xFFFF44    # Amarillo claro
        self.solution_path_color = 0xFF00FF    # Magenta
        self.draw_maze()
        self.sync()

    def initialize_rendered_generation(self) -> None:
        """Initialize the maze generation with animation."""
        self.generation_complete = False
        self.last_generation_time = time.time()
        self.generation_generator = self.generator.generate_step_by_step()
        self.draw_maze()

    def initialize_rendered_solving(self, solver: Any) -> None:
        """Initialize the maze solving with animation."""
        self.solving_complete = False
        self.last_solving_time = time.time()
        self.solving_generator = solver
        self.draw_maze()

    def _setup_hooks(self) -> None:
        """Set up window event hooks."""
        self.mlx.mlx_hook(self.win_ptr, 17, 0, lambda _: self.destroy,
                          None)
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self._handle_keypress, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._loop_hook, None)

    def draw_solution(self, solution: list[Cell]) -> None:
        """Draw the complete solution path without animation."""
        if not self.board:
            return
        # Sincronizar imagen para escritura
        self.mlx.mlx_sync(self.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, self.img_ptr)

        # Calcular dimensiones
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        for cell in solution:
            x, y = cell.coord
            px = (x - 1) * cell_width
            py = (y - 1) * cell_height

            if cell.is_start:
                self._fill_rect(px + 1, py + 1,
                                cell_width - 2,
                                cell_height - 2,
                                self.start_color)
            elif cell.is_exit:
                self._fill_rect(px + 1, py + 1,
                                cell_width - 2,
                                cell_height - 2,
                                self.end_color)
            else:
                self._fill_rect(px + 1, py + 1,
                                cell_width - 2,
                                cell_height - 2,
                                self.solution_path_color)

        # Mostrar la imagen en la ventana
        self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                         self.win_ptr,
                                         self.img_ptr, 0, 0)

    def _loop_hook(self, param: Any) -> int:
        """Execute on each frame of the main loop."""
        if not self.running:
            return 0

        # Si no hay ni generación ni solving activos, terminar el loop
        if not self.generation_generator and not self.solving_generator:
            self._end_loop()

        # Procesar generación paso a paso
        if self.generation_generator and not self.generation_complete:
            import time
            current_time = time.time()

            if current_time - self.last_generation_time >= \
               self.generation_speed:
                self.last_generation_time = current_time

                try:
                    step_info = next(self.generation_generator)
                    modified_cells = step_info.get('modified_cells', [])

                    if modified_cells:
                        self._draw_cells_incremental(modified_cells)

                except StopIteration:
                    self.generation_complete = True
                    self._end_loop()

        # Procesar solución paso a paso
        if self.solving_generator and not self.solving_complete:
            import time
            current_time = time.time()

            if current_time - self.last_solving_time >= self.solving_speed:
                self.last_solving_time = current_time

                try:
                    step_info = next(self.solving_generator)
                    action = step_info.get('action', '')
                    modified_cells = step_info.get('modified_cells', [])

                    if modified_cells:
                        self._draw_cells_solving(modified_cells, action)

                except StopIteration:
                    self.solving_complete = True
                    self.mlx.mlx_loop_exit(self.mlx_ptr)

        return 0

    def _handle_keypress(self, keycode: int, param: Any) -> None:
        """Handle keyboard input."""
        if keycode == 113:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
            self.generator.initialize_board()
            self.draw_maze()
            self.sync()
            self.generation_complete = False

    def _close_window(self, param: Any = None) -> int:
        """Close the window and stop the main loop."""
        self.running = False
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def set_wall_color(self, color: int) -> None:
        """Set the wall color."""
        self.wall_color = color
        if self.board:
            self.draw_maze()

    def set_background_color(self, color: int) -> None:
        """Set the background color."""
        self.bg_color = color
        if self.board:
            self.draw_maze()

    def set_visited_color(self, color: int) -> None:
        """Set the visited cell color."""
        self.visited_color = color
        if self.board:
            self.draw_maze()
        if self.board:
            self.draw_maze()

    def draw_maze(self) -> None:
        """Draw the complete maze."""
        if not self.board:
            return

        # Sincronizar imagen para escritura
        self.mlx.mlx_sync(self.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, self.img_ptr)

        # Clear image buffer with background color
        bg_with_alpha = 0xFF000000 | self.bg_color  # Add alpha channel
        for i in range(0, len(self.img_buffer), 4):
            self.img_buffer[i:i+4] = list(bg_with_alpha.to_bytes(4, 'little'))

        # Calculate dimensions of a Cell
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        # Draw each cell
        for coord, cell in self.board.items():
            self._draw_cell(cell, cell_width, cell_height)

        # Display image in window
        self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                         self.win_ptr,
                                         self.img_ptr, 0, 0)

    def _put_pixel_to_image(self, x: int, y: int, color: int) -> None:
        """Draw a pixel in the image buffer."""
        if 0 <= x < self.width and 0 <= y < self.height:
            offset: int = (y * self.width + x) * 4  # 4 bytes por píxel
            self.img_buffer[offset:offset+4] = list(
                (0xFF000000 | color).to_bytes(4, 'little'))

    def _draw_cells_incremental(self, cells: list[Cell]) -> None:
        """Draw only the specified cells without clearing the entire screen."""
        if not self.board:
            return

        # Sincronizar imagen para escritura
        self.mlx.mlx_sync(self.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, self.img_ptr)

        # Calcular dimensiones
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        for cell in cells:
            # First clear the cell area
            x, y = cell.coord
            px = (x - 1) * cell_width
            py = (y - 1) * cell_height
            self._fill_rect(px, py, cell_width, cell_height, self.bg_color)

            # Then draw the updated cell
            self._draw_cell(cell, cell_width, cell_height)

        # Display image in window
        self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                         self.win_ptr,
                                         self.img_ptr, 0, 0)

    def _draw_cells_solving(self, cells: list[Cell], action: str) -> None:
        """Draw cells during the solving process."""
        if not self.board:
            return

        # Sincronizar imagen para escritura
        self.mlx.mlx_sync(self.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, self.img_ptr)

        # Calcular dimensiones
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        # Determinar el color según la acción
        color = self.bg_color
        if action in ['init_start', 'exploring_start']:
            color = self.exploring_start_color
        elif action in ['init_goal', 'exploring_goal']:
            color = self.exploring_goal_color
        elif action == 'visiting_start':
            color = self.visiting_start_color
        elif action == 'visiting_goal':
            color = self.visiting_goal_color
        elif action == 'solution_found':
            color = self.solution_path_color
        elif action in ['backtracking_start', 'backtracking_goal',
                        'clear_visited']:
            color = self.bg_color  # Return to black background

        for cell in cells:
            x, y = cell.coord
            px = (x - 1) * cell_width
            py = (y - 1) * cell_height

            # If solution_found, don't clear entire cell, just paint interior
            # to keep wall-less spaces as they were
            if action == 'solution_found':
                # Only paint interior (where there are no walls)
                if not cell.is_start and not cell.is_exit and (
                        not cell.is_fixed):
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2,
                                    cell_height - 2,
                                    color)
                # Keep special colors for start/exit/fixed
                if cell.is_start:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2,
                                    cell_height - 2,
                                    self.start_color)
                elif cell.is_exit:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2,
                                    cell_height - 2,
                                    self.end_color)
                elif cell.is_fixed:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2,
                                    cell_height - 2,
                                    self.start_color)
            else:
                # For all other actions, clear and redraw
                self._fill_rect(px, py, cell_width, cell_height, self.bg_color)

                # Paint cell interior with appropriate color
                if color != self.bg_color:
                    # Draw colored background for non-special cells
                    if not cell.is_start and not cell.is_exit and (
                            not cell.is_fixed):
                        self._fill_rect(px + 1, py + 1,
                                        cell_width - 2, cell_height - 2,
                                        color)

                # Keep special colors for start/exit/fixed always
                if cell.is_start:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2, cell_height - 2,
                                    self.start_color)
                elif cell.is_exit:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2, cell_height - 2,
                                    self.end_color)
                elif cell.is_fixed:
                    self._fill_rect(px + 1, py + 1,
                                    cell_width - 2, cell_height - 2,
                                    self.start_color)

                # Dibujar las paredes siempre
                if cell.has_wall(NORTH):
                    self._draw_line(px, py,
                                    px + cell_width, py, self.wall_color,
                                    self.wall_thickness)
                if cell.has_wall(SOUTH):
                    self._draw_line(px, py + cell_height,
                                    px + cell_width, py + cell_height,
                                    self.wall_color,
                                    self.wall_thickness)
                if cell.has_wall(WEST):
                    self._draw_line(px, py, px, py + cell_height,
                                    self.wall_color, self.wall_thickness)
                if cell.has_wall(EAST):
                    self._draw_line(px + cell_width, py, px + cell_width,
                                    py + cell_height, self.wall_color,
                                    self.wall_thickness)

        # Mostrar la imagen en la ventana
        self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                         self.win_ptr,
                                         self.img_ptr, 0, 0)

    def _draw_cell(self, cell: Cell, cell_width: int,
                   cell_height: int) -> None:
        """Draw a single cell with current colors."""
        x, y = cell.coord

        # Convertir coordenadas del maze (inician DESDE 1) a pixeles
        px = (x - 1) * cell_width
        py = (y - 1) * cell_height

        # Dibujar fondo de la celda de color si son entrada y salida
        if cell.is_start:
            self._fill_rect(px + 1, py + 1, cell_width - 2, cell_height - 2,
                            self.start_color)
        if cell.is_exit:
            self._fill_rect(px + 1, py + 1, cell_width - 2, cell_height - 2,
                            self.end_color)
        # Si forma parte del logo central de 42
        if cell.is_fixed:
            self._fill_rect(px + 1, py + 1, cell_width - 2, cell_height - 2,
                            self.start_color)
        # Dibujar paredes de la celda
        if cell.has_wall(NORTH):
            self._draw_line(px, py, px + cell_width,
                            py,
                            self.wall_color,
                            self.wall_thickness)

        if cell.has_wall(SOUTH):
            self._draw_line(px, py + cell_height,
                            px + cell_width, py + cell_height,
                            self.wall_color,
                            self.wall_thickness)

        if cell.has_wall(WEST):
            self._draw_line(px, py, px, py + cell_height,
                            self.wall_color,
                            self.wall_thickness)

        if cell.has_wall(EAST):
            self._draw_line(px + cell_width,
                            py, px + cell_width,
                            py + cell_height,
                            self.wall_color,
                            self.wall_thickness)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int,
                   thickness: int = 1) -> None:
        """Draw a line with thickness using linear interpolation."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy)

        # Caso especial: un solo punto
        if steps == 0:
            for t in range(thickness):
                if 0 <= x1 < self.width and 0 <= y1 + t < self.height:
                    self._put_pixel_to_image(int(x1), int(y1) + t, color)
            return

        # Calcular incrementos
        x_inc = (x2 - x1) / steps
        y_inc = (y2 - y1) / steps

        # Dibujar la línea píxel a píxel
        for i in range(int(steps) + 1):
            x = x1 + x_inc * i
            y = y1 + y_inc * i

            # Aplicar grosor
            for t in range(thickness):
                px, py = int(x), int(y)

                # Aplicar grosor perpendicular a la direccion de la línea
                if dx > dy:
                    py = py + t - thickness // 2
                else:
                    px = px + t - thickness // 2

                # Verificar límites y dibujar
                if 0 <= px < self.width and 0 <= py < self.height:
                    self._put_pixel_to_image(px, py, color)

    def _fill_rect(self, x: int, y: int, width: int, height: int,
                   color: int) -> None:
        """Draw a filled rectangle pixel by pixel."""
        x_start = int(x)
        y_start = int(y)
        x_end = int(x + width)
        y_end = int(y + height)

        for py in range(y_start, y_end):
            for px in range(x_start, x_end):
                if 0 <= px < self.width and 0 <= py < self.height:
                    self._put_pixel_to_image(px, py, color)

    def get_window_size(self) -> tuple[int, int]:
        """Calculate window size based on maze dimensions."""
        cell_size_x = 1920 // self.config.width
        cell_size_y = 1080 // self.config.height

        # Use smaller size to maintain proportions
        cell_size = max(10, min(cell_size_x, cell_size_y, 20))

        # Calculate final window dimensions
        window_width = min(self.config.width * cell_size, 1920)
        window_height = min(self.config.height * cell_size, 1080)

        return window_width, window_height

    # ===== LOOP CONTROL =====

    def sync(self) -> None:
        """Synchronous rendering of current buffer."""
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def run(self, static: bool = False) -> None:
        """Start MLX main loop."""
        self.mlx.mlx_loop(self.mlx_ptr)
        if static:
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _end_loop(self) -> None:
        """End the MLX loop."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def destroy(self) -> None:
        """Release MLX resources."""
        self._close_window()
        if self.win_ptr:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
            self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.win_ptr = None
