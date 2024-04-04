import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Definir constantes
TILE_SIZE = 64
GRID_WIDTH = 10
GRID_HEIGHT = 10
ZOOM_SPEED = 1.1

# Inicializar Pygame
pygame.init()

# Función para redimensionar la imagen a 64x64
def resize_image(image_path):
    img = Image.open(image_path)
    img = img.resize((TILE_SIZE, TILE_SIZE), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

# Clase TilemapEditor
class TilemapEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tilemap Editor")

        # Variables
        self.tile_images = {}  # Almacena las imágenes de los bloques
        self.tilemap = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Representa el tilemap como una matriz
        self.zoom_level = 1.0  # Nivel de zoom inicial
        self.camera_x = 0
        self.camera_y = 0

        # Configuración de Pygame
        self.screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
        pygame.display.set_caption("Tilemap Editor")

        # Configuración de Tkinter
        self.canvas = tk.Canvas(self.root, width=GRID_WIDTH * TILE_SIZE, height=GRID_HEIGHT * TILE_SIZE)
        self.canvas.pack()

        # Botón para cargar texturas
        load_button = tk.Button(self.root, text="Cargar Texturas", command=self.load_textures)
        load_button.pack()

        # Botón para guardar el tilemap
        save_button = tk.Button(self.root, text="Guardar Tilemap", command=self.save_tilemap)
        save_button.pack()

        # Crear la interfaz de usuario para el tilemap
        self.create_tilemap_ui()

        # Eventos de teclado y ratón
        self.root.bind("<Up>", lambda event: self.move_camera(0, -1))
        self.root.bind("<Down>", lambda event: self.move_camera(0, 1))
        self.root.bind("<Left>", lambda event: self.move_camera(-1, 0))
        self.root.bind("<Right>", lambda event: self.move_camera(1, 0))
        self.root.bind("<MouseWheel>", self.zoom)

        # Iniciar el bucle principal
        self.root.mainloop()

    # Función para cargar texturas
    def load_textures(self):
        file_paths = filedialog.askopenfilenames(title="Seleccionar Texturas", filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        for file_path in file_paths:
            image = resize_image(file_path)
            self.tile_images[file_path] = image

    # Función para crear la interfaz de usuario para el tilemap
    def create_tilemap_ui(self):
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                tile_frame = tk.Frame(self.root, width=TILE_SIZE, height=TILE_SIZE, borderwidth=1, relief="solid")
                tile_frame.grid(row=row, column=col)  # Utilizamos solo grid aquí

                # Evento clic derecho para abrir el menú contextual
                tile_frame.bind("<Button-3>", lambda event, row=row, col=col: self.show_context_menu(event, row, col))


    # Función para colocar un bloque en el tilemap
    def place_tile(self, row, col):
        selected_texture = self.select_texture()
        if selected_texture:
            self.tilemap[row][col] = {"texture": selected_texture, "collidable": False}
            self.draw_tilemap()

    # Función para seleccionar la textura
    def select_texture(self):
        texture_path = filedialog.askopenfilename(title="Seleccionar Textura", filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        if texture_path:
            return texture_path

    # Función para dibujar el tilemap
    def draw_tilemap(self):
        self.canvas.delete("all")
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                tile_data = self.tilemap[row][col]
                texture_path = tile_data["texture"]
                if texture_path in self.tile_images:
                    image = self.tile_images[texture_path]
                    x = col * TILE_SIZE - self.camera_x
                    y = row * TILE_SIZE - self.camera_y
                    self.canvas.create_image(x, y, anchor=tk.NW, image=image)

    # Función para guardar el tilemap
    def save_tilemap(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for row in self.tilemap:
                    file.write(" ".join(str(tile["texture"]) for tile in row) + "\n")

    # Función para mover la cámara
    def move_camera(self, dx, dy):
        self.camera_x += dx * TILE_SIZE
        self.camera_y += dy * TILE_SIZE
        self.draw_tilemap()

    # Función para hacer zoom
    def zoom(self, event):
        if event.delta > 0:  # Rueda hacia arriba
            self.zoom_level *= ZOOM_SPEED
        else:  # Rueda hacia abajo
            self.zoom_level /= ZOOM_SPEED

        self.canvas.scale("all", 0, 0, self.zoom_level, self.zoom_level)
        self.draw_tilemap()

    # Función para mostrar el menú de propiedades al hacer clic derecho
    def show_properties_menu(self, event, row, col):
        tile_data = self.tilemap[row][col]
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Colisionable", command=lambda: self.toggle_collidable(row, col))
        menu.post(event.x_root, event.y_root)

    # Función para activar/desactivar la propiedad de colisión
    def toggle_collidable(self, row, col):
        self.tilemap[row][col]["collidable"] = not self.tilemap[row][col]["collidable"]
        self.draw_tilemap()

# Iniciar el editor de Tilemap
editor = TilemapEditor()
