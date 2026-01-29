from self_typing import MazeBoard
from self_typing.maze import NORTH, SOUTH, EAST, WEST
from src.Cell import Cell
from mlx import Mlx
import ctypes
import time


class MazeRenderer:

    def __init__(self, width: int, height: int):
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        if width > 1920 or height > 1080:
            width = 1920
            height = 1080

        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, width,
                                               height, "A_maze_ing")

        self.width = width
        self.height = height

        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        self._setup_hooks()

        self.running = True
        self.board: MazeBoard | None = None

        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, width, height)

        addr_info = self.mlx.mlx_get_data_addr(self.img_ptr)

        # addr_info es (buffer, bits_per_pixel, size_line, endian)
        # El buffer ya es un objeto memory que podemos usar directamente
        self.img_buffer = (
            ctypes.c_ubyte * (width * height * 4)).from_buffer(addr_info[0])

        # Estados de renderizado
        self.wall_color = 0xFFFFFF
        self.bg_color = 0x000000
        
        self.visited_color = 0x000000

        # Estado de generación
        self.generation_generator = None
        self.generation_complete = False
        self.generation_speed = 0.01
        self.last_generation_time = 0

    def _setup_hooks(self):
        """Configura los hooks de eventos de la ventana."""
        self.mlx.mlx_hook(self.win_ptr, 17, 0, lambda _: self.destroy,
                          None)
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._loop_hook, None)

    def _loop_hook(self, param):
        """Se ejecuta en cada frame del loop."""
        if not self.running:
            return 0

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
                        self._draw_maze()

                except StopIteration:
                    self.generation_complete = True
                    self._draw_maze()  # Redibujar completo al final

                    time.sleep(2)
                    self.mlx.mlx_loop_exit(self.mlx_ptr)

        return 0

    def handle_keypress(self, keycode: int, param):
        """Maneja eventos de teclado."""
        return 0

    def close_window(self, param=None):
        """Cierra la ventana y sale del loop."""
        self.running = False
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def initialize_generation(self, board: MazeBoard, generator):
        """Inicia la generación del laberinto."""
        self.board = board
        self.generation_generator = generator
        self.generation_complete = False
        self.last_generation_time = time.time()

    def set_wall_color(self, color: int):
        """Cambia el color de las paredes."""
        self.wall_color = color
        if self.board:
            self._draw_maze()
            self.sync()

    def set_background_color(self, color: int):
        """Cambia el color de fondo."""
        self.bg_color = color
        if self.board:
            self._draw_maze()
            self.sync()

    def set_visited_color(self, color: int):
        """Cambia el color de celdas visitadas."""
        self.visited_color = color
        if self.board:
            self._draw_maze()
            self.sync()
        if self.board:
            self._draw_maze()

    # ===== MÉTODOS DE DIBUJO (ejecutan en renderer thread) =====

    def _draw_maze(self):
        """Dibuja el laberinto completo usando colores actuales."""
        if not self.board:
            return

        # Sincronizar imagen para escritura
        self.mlx.mlx_sync(self.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, self.img_ptr)

        # Limpiar el buffer de imagen con el color de fondo
        bg_with_alpha = 0xFF000000 | self.bg_color  # Añadir canal alpha
        for i in range(0, len(self.img_buffer), 4):
            self.img_buffer[i:i+4] = bg_with_alpha.to_bytes(4, 'little')

        # Calcular dimensiones de cada celda
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        # Dibujar cada celda
        cells_drawn = 0
        for coord, cell in self.board.items():
            self._draw_cell(cell, cell_width, cell_height)
            cells_drawn += 1

        # Mostrar la imagen en la ventana
        self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                         self.win_ptr,
                                         self.img_ptr, 0, 0)

    def _put_pixel_to_image(self, x: int, y: int, color: int):
        """Dibuja un píxel en el buffer de la imagen."""
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 4  # 4 bytes por píxel
            self.img_buffer[offset:offset+4] = (0xFF000000 | color).to_bytes(4,
                                                                             '\
little')

    def _draw_cells_incremental(self, cells: list):
        """Dibuja solo las celdas especificadas sin limpiar toda la pantalla"""
        if not self.board:
            return

        # Calcular dimensiones
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())

        cell_width = self.width // max_x
        cell_height = self.height // max_y

        # Dibujar solo las celdas modificadas
        for cell in cells:
            # Primero limpiar el área de la celda
            x, y = cell.coord
            px = (x - 1) * cell_width
            py = (y - 1) * cell_height
            self._fill_rect(px, py, cell_width, cell_height, self.bg_color)

            # Luego dibujar la celda actualizada
            self._draw_cell(cell, cell_width, cell_height)

    def _draw_cell(self, cell: Cell, cell_width: int, cell_height: int):
        """Dibuja una celda individual con los colores actuales"""
        x, y = cell.coord

        # Convertir coordenadas del maze (1-indexed) a píxeles
        px = (x - 1) * cell_width
        py = (y - 1) * cell_height

        # Dibujar fondo de la celda
        if cell.visited:
            # Celda visitada con color especial
            self._fill_rect(px + 1, py + 1, cell_width - 2, cell_height - 2,
                            self.visited_color)

        # Dibujar paredes de la celda (has_wall retorna int, no bool)
        wall_thickness = 4

        if cell.has_wall(NORTH):
            self._draw_line(px, py, px + cell_width,
                            py,
                            self.wall_color,
                            wall_thickness)

        if cell.has_wall(SOUTH):
            self._draw_line(px, py + cell_height,
                            px + cell_width, py + cell_height,
                            self.wall_color,
                            wall_thickness)

        if cell.has_wall(WEST):
            self._draw_line(px, py, px, py + cell_height,
                            self.wall_color,
                            wall_thickness)

        if cell.has_wall(EAST):
            self._draw_line(px + cell_width,
                            py, px + cell_width,
                            py + cell_height,
                            self.wall_color,
                            wall_thickness)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int,
                   thickness: int = 1):
        """Dibuja una línea con grosor usando interpolación lineal."""
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

                # Aplicar grosor perpendicular a la dirección de la línea
                if dx > dy:  # Línea más horizontal - grosor vertical
                    py = py + t - thickness // 2
                else:  # Línea más vertical - grosor horizontal
                    px = px + t - thickness // 2

                # Verificar límites y dibujar
                if 0 <= px < self.width and 0 <= py < self.height:
                    self._put_pixel_to_image(px, py, color)

    def _fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        """Dibuja un rectángulo relleno píxel a píxel."""
        x_start = int(x)
        y_start = int(y)
        x_end = int(x + width)
        y_end = int(y + height)

        for py in range(y_start, y_end):
            for px in range(x_start, x_end):
                if 0 <= px < self.width and 0 <= py < self.height:
                    self._put_pixel_to_image(px, py, color)

    # ===== CONTROL DEL LOOP =====

    def sync(self):
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def run(self):
        self.mlx.mlx_loop(self.mlx_ptr)

    def destroy(self):
        self.running = False
        if self.win_ptr:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.win_ptr = None
