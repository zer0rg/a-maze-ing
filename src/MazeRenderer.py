from self_typing import MazeBoard
from self_typing.maze import NORTH, SOUTH, EAST, WEST
from mlx import Mlx
import threading
import queue


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
        self.board = None
        
        # Estados que el loop leerá
        self.wall_color = 0xFFFFFF  # Blanco por defecto
        self.bg_color = 0x000000    # Negro por defecto
        self.visited_color = 0x00FF00  # Verde por defecto
        
        # Cola para comandos thread-safe
        self.command_queue = queue.Queue()
        self.render_thread = None
        
        # Estado de animación
        self.animation_generator = None
        self.current_step_info = None
        self.last_update = 0
        self.animation_speed = 0.01

    def _setup_hooks(self):
        """Configura los hooks de eventos de la ventana."""
        self.mlx.mlx_hook(self.win_ptr, 17, 0, self.close_window, None)
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._loop_hook, None)

    def _loop_hook(self, param):
        """Se ejecuta en cada frame del loop."""
        if not self.running:
            return 0
        
        import time
        
        # 1. Procesar comandos de la cola
        try:
            while not self.command_queue.empty():
                command = self.command_queue.get_nowait()
                self._process_command(command)
        except queue.Empty:
            pass
        
        # 2. Actualizar animación si hay
        if self.animation_generator:
            current_time = time.time()
            if current_time - self.last_update >= self.animation_speed:
                self.last_update = current_time
                try:
                    self.current_step_info = next(self.animation_generator)
                    print(self.current_step_info)
                    self._draw_maze()  # Redibujar con colores actuales
                except StopIteration:
                    self.animation_generator = None
                    self._draw_maze()
        
        return 0

    def _process_command(self, command: dict):
        """Procesa comandos del main thread."""
        cmd_type = command.get('type')
        
        if cmd_type == 'render':
            self.board = command.get('board')
            self._draw_maze()
        
        elif cmd_type == 'update_step':
            self.current_step_info = command.get('step_info')
            self._draw_maze()
        
        elif cmd_type == 'set_animation':
            self.animation_generator = command.get('generator')
            import time
            self.last_update = time.time()
        
        elif cmd_type == 'set_color':
            # Cambiar color según el tipo
            color_type = command.get('color_type')
            color_value = command.get('color_value')
            
            if color_type == 'wall':
                self.wall_color = color_value
            elif color_type == 'bg':
                self.bg_color = color_value
            elif color_type == 'visited':
                self.visited_color = color_value
            
            # Redibujar con nuevos colores
            self._draw_maze()
        
        elif cmd_type == 'clear':
            self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

    def handle_keypress(self, keycode: int, param):
        """Maneja eventos de teclado."""
        if keycode == 65307:  # ESC key
            self.close_window()
        return 0

    def close_window(self, param=None):
        """Cierra la ventana y sale del loop."""
        self.running = False
        self.mlx.mlx_loop_end(self.mlx_ptr)
        return 0

    # ===== MÉTODOS PARA LLAMAR DESDE MAIN THREAD =====
    
    def set_wall_color(self, color: int):
        """Cambia el color de las paredes (desde main thread)."""
        self.command_queue.put({
            'type': 'set_color',
            'color_type': 'wall',
            'color_value': color
        })

    def set_background_color(self, color: int):
        """Cambia el color de fondo (desde main thread)."""
        self.command_queue.put({
            'type': 'set_color',
            'color_type': 'bg',
            'color_value': color
        })

    def set_visited_color(self, color: int):
        """Cambia el color de celdas visitadas (desde main thread)."""
        self.command_queue.put({
            'type': 'set_color',
            'color_type': 'visited',
            'color_value': color
        })

    def set_animation(self, generator):
        """Establece un generador para animación."""
        self.command_queue.put({
            'type': 'set_animation',
            'generator': generator
        })

    def render(self, board: MazeBoard):
        """Envía comando de render."""
        self.command_queue.put({
            'type': 'render',
            'board': board
        })

    def update_step(self, step_info: dict):
        """Envía actualización de paso."""
        self.command_queue.put({
            'type': 'update_step',
            'step_info': step_info
        })

    # ===== MÉTODOS DE DIBUJO (ejecutan en renderer thread) =====

    def _draw_maze(self):
        """Dibuja el laberinto completo usando colores actuales."""
        if not self.board:
            return
                
        # Limpiar ventana con color de fondo
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        
        # Calcular dimensiones de cada celda
        # Obtener dimensiones del maze
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())
        
        cell_width = self.width // max_x
        cell_height = self.height // max_y
        
        # Dibujar cada celda
        for coord, cell in self.board.items():
            self._draw_cell(cell, cell_width, cell_height)
        
        # Resaltar paso actual si hay animación
        if self.current_step_info:
            self._highlight_current_step(cell_width, cell_height)

    def _draw_cell(self, cell, cell_width: int, cell_height: int):
        """Dibuja una celda individual con los colores actuales."""
        x, y = cell.coord
        
        # Convertir coordenadas del maze (1-indexed) a píxeles
        px = (x - 1) * cell_width
        py = (y - 1) * cell_height
        
        # Dibujar fondo de la celda
        if cell.visited:
            # Celda visitada con color especial
            self._fill_rect(px + 1, py + 1, cell_width - 2, cell_height - 2, self.visited_color)
        
        # Dibujar paredes de la celda
        wall_thickness = 2
        
        if cell.has_wall(NORTH):
            self._draw_line(px, py, px + cell_width, py, self.wall_color, wall_thickness)
        
        if cell.has_wall(SOUTH):
            self._draw_line(px, py + cell_height, px + cell_width, py + cell_height, 
                          self.wall_color, wall_thickness)
        
        if cell.has_wall(WEST):
            self._draw_line(px, py, px, py + cell_height, self.wall_color, wall_thickness)
        
        if cell.has_wall(EAST):
            self._draw_line(px + cell_width, py, px + cell_width, py + cell_height, 
                          self.wall_color, wall_thickness)

    def _highlight_current_step(self, cell_width: int, cell_height: int):
        """Resalta la celda del paso actual de la animación."""
        if not self.current_step_info:
            return
        
        current_coord = self.current_step_info.get('current')
        if not current_coord:
            return
        
        x, y = current_coord
        px = (x - 1) * cell_width
        py = (y - 1) * cell_height
        
        # Color según acción
        action = self.current_step_info.get('action', '')
        if action == 'visiting':
            color = 0x0000FF  # Azul para visitando
        elif action == 'breaking_wall':
            color = 0xFF0000  # Rojo para rompiendo pared
        elif action == 'backtracking':
            color = 0xFFFF00  # Amarillo para backtracking
        else:
            color = 0xFF00FF  # Magenta por defecto
        
        # Resaltar con un rectángulo más pequeño en el centro
        margin = cell_width // 4
        self._fill_rect(px + margin, py + margin, 
                       cell_width - 2*margin, cell_height - 2*margin, color)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int, thickness: int = 1):
        """Dibuja una línea con grosor."""
        # Calcular puntos intermedios usando interpolación lineal
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy)
        
        if steps == 0:
            for t in range(thickness):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, int(x1), int(y1) + t, color)
            return
        
        x_inc = (x2 - x1) / steps
        y_inc = (y2 - y1) / steps
        
        for i in range(int(steps) + 1):
            x = x1 + x_inc * i
            y = y1 + y_inc * i
            
            # Dibujar con grosor
            for t in range(thickness):
                if dx > dy:  # Línea más horizontal
                    self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, 
                                          int(x), int(y) + t - thickness//2, color)
                else:  # Línea más vertical
                    self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, 
                                          int(x) + t - thickness//2, int(y), color)

    def _fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        """Dibuja un rectángulo relleno."""
        for i in range(int(height)):
            for j in range(int(width)):
                px = int(x + j)
                py = int(y + i)
                # Verificar límites de la ventana
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, px, py, color)

    # ===== CONTROL DEL THREAD =====

    def start_loop(self):
        """Inicia el loop de MLX en un thread separado."""
        def run_mlx_loop():
            self.mlx.mlx_loop(self.mlx_ptr)
        
        self.render_thread = threading.Thread(target=run_mlx_loop, daemon=True)
        self.render_thread.start()


    def wait_until_closed(self):
        """Espera hasta que se cierre la ventana."""
        if self.render_thread:
            self.render_thread.join()

    def destroy(self):
        """Limpia recursos al finalizar."""
        self.running = False
        if self.win_ptr:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.win_ptr = None
