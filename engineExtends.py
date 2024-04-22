#basics.py
import pygame
import json
import time
import functools
from numba import njit
import math

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.target = None

    def set_target(self, target):
        self.target = target
    
    def update(self):
        if self.target:
            target_rect = self.target.get_rect()
            self.x = target_rect.centerx - self.width / 2 
            #self.y = target_rect.centery - self.height / 1.2

    def apply(self, rect):
        scaled_x = (rect.x - self.x) * self.zoom
        scaled_y = (rect.y - self.y) * self.zoom

        return pygame.Rect(scaled_x, scaled_y, rect.width * self.zoom, rect.height * self.zoom)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  
            self.zoom *= 1.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: 
            self.zoom /= 1.1

class FreeCamera(Camera):
    def update(self):
        keys = pygame.key.get_pressed()
        speed = 5

        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  
                self.zoom *= 1.1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  
                self.zoom /= 1.1
    def apply(self, rect):
        scaled_x = (rect.x - self.x) * self.zoom
        scaled_y = (rect.y - self.y) * self.zoom
        return pygame.Rect(scaled_x, scaled_y, rect.width * self.zoom, rect.height * self.zoom)
class Render():
    def draw(self, screen,camera_rect=None):
        dx, dy = (-camera_rect.x, -camera_rect.y) if camera_rect else (0, 0)
        if self.color:
            screen.blit(self.surface, self.rect.move(dx, dy))
        elif self.texture:
            screen.blit(self.texture, self.rect.move(dx, dy))
    def set_animations(self, frame_dict, animation_name):
        self.animations[animation_name] = frame_dict
    def start_animation(self, animation_name):
        """
        Inicia una animación específica.
        """
        if animation_name in self.animations:
            self.current_animation = animation_name
        else:
            print(f"La animación '{animation_name}' no existe.")

class UIElement:
    def __init__(self, x, y, width, height, element_id, json_file, draggable=False, type=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_dragging = False
        self.element_id = element_id
        self.json_file = json_file
        self.load_positions_from_json()
        self.draggable = draggable
        self.herarchy = type

    def draw(self, screen):
        pass

    def handle_mouse_event(self, event):
        if self.draggable:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_click(event.pos)
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                self.move_with_mouse(event.rel)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_dragging = False
                self.save_positions_to_json()

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_dragging = True

    def move_with_mouse(self, rel):
        if self.is_dragging:
            self.rect.move_ip(rel)

    def save_positions_to_json(self):
        positions_data = {}
        try:
            with open(self.json_file, 'r') as json_file:
                positions_data = json.load(json_file)
        except FileNotFoundError:
            print("No se especifica archivo")

        positions_data[self.element_id] = {
            "x": self.rect.x,
            "y": self.rect.y
        }

        with open(self.json_file, 'w') as json_file:
            json.dump(positions_data, json_file)

    def load_positions_from_json(self):
        try:
            if self.json_file:
                with open(self.json_file, 'r') as json_file:
                    positions_data = json.load(json_file)
                    element_data = positions_data.get(self.element_id, {})
                    self.rect.x = element_data.get("x", self.rect.x)
                    self.rect.y = element_data.get("y", self.rect.y)
        except FileNotFoundError:
            print("ads")

class TextBlock(UIElement):
    def __init__(self, x, y, width, height, text="", font_size=20, font_color=(255, 255, 255), max_chars=None, draw_background=True, element_id=None, json_file=None, draggable=False, type=None):
        super().__init__(x, y, width, height, element_id, json_file, draggable, type)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.max_chars = max_chars
        self.draw_background = draw_background  
        self.font = pygame.font.Font(None, self.font_size)
        self.lines = []
        self.images = []
        self.update_content()
        
    def handle_event(self, event):
        super().handle_mouse_event(event)  
    def update(self, text):
        self.text = text
        self.update_content()
        
    def update_content(self):
        self.lines = []

        if self.max_chars is not None and len(self.text) > self.max_chars:
            words = self.text.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) <= self.max_chars:
                    current_line += word + " "
                else:
                    self.lines.append(current_line.rstrip())
                    current_line = word + " "
            self.lines.append(current_line.rstrip())
        else:
            self.lines.append(self.text)

        # Si hay demasiadas líneas, elimina las primeras líneas hasta que quepan
        while len(self.lines) * self.font_size > self.rect.height:
            self.lines.pop(0)

        self.rendered_lines = [self.font.render(line, True, self.font_color) for line in self.lines]
        self.adjust_position()

    def add_line(self, new_line):
        # Agrega la nueva línea al principio del texto
        self.text = new_line + "\n" + self.text
        self.update_content()

    def add_image(self, image_path, opacity=255, size=None):
        image = pygame.image.load(image_path).convert_alpha()
        if size is not None:
            image = pygame.transform.scale(image, size)
        image.set_alpha(opacity)
        self.images.append(image)
        self.adjust_position()

    def adjust_position(self):
        total_height = sum(line.get_rect().height for line in self.rendered_lines)
        for image in self.images:
            total_height += image.get_rect().height

        if total_height > self.rect.height:
            self.rect.height = total_height

    def draw(self, screen):
        if self.draw_background:  
            pygame.draw.rect(screen, (0, 0, 0), self.rect)  

        current_y = self.rect.y
        for rendered_line in self.rendered_lines:
            screen.blit(rendered_line, (self.rect.x, current_y))
            current_y += rendered_line.get_rect().height

        for image in self.images:
            screen.blit(image, (self.rect.x, current_y))
            current_y += image.get_rect().height

class TextInput(UIElement):
    def __init__(self, text="", position=(0, 0), font_size=30, width=200, height=40, color=(255, 255, 255), background_color=(0, 0, 0), element_id=None, json_file=None, draggable=False, type=None):
        super().__init__(position[0], position[1], width, height, element_id, json_file, draggable, type)
        self.text = text
        self.position = position
        self.font_size = font_size
        self.width = width
        self.height = height
        self.color = color
        self.background_color = background_color
        self.font = pygame.font.Font(None, self.font_size)
        self.is_active = False
        self.developer_mode= draggable

    def handle_event(self, event, game):
        super().handle_mouse_event(event)  
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.rect.x < x < self.rect.x + self.width and self.rect.y < y < self.rect.y + self.height: 
                self.is_active = True
            else:
                self.is_active = False
        elif event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                self.is_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        if event.type == pygame.KEYDOWN and self.developer_mode:
            if event.key == pygame.K_RETURN: 
                if self.text.startswith('-'):
                    try:
                        exec(self.text.lstrip('-'))
                        game.ui_elements[2].add_line("Accion realizada.")
                        self.text = ''
                    except Exception as e:
                        print(f"Failed to set target for {e.args}")
                        game.popup.activate(f"Failed to set target for {e.args}")

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, (self.rect.x, self.rect.y, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.width, self.height), 2)

        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class PopUp():
    def __init__(self):
        self.isactive = False
        self.activation_time = None
        self.text = ''

    def draw_popup(self, screen):
        rect_width = screen.get_width() * 0.50  # 50% del ancho de la pantalla
        rect_height = screen.get_height() * 0.2  # 20% del alto de la pantalla

        font_size = int(min(rect_width, rect_height) * 0.15)  # Ajusta el tamaño de la fuente al 4% del menor entre el ancho y el alto del rectángulo
        font = pygame.font.Font(None, font_size)

        text = font.render(f"{self.text}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(rect_width, rect_height))
        screen.blit(text, text_rect)

    def activate(self, text):
        self.text = text
        self.isactive = True
        self.activation_time = time.time()

    def update(self):
        if self.isactive and time.time() - self.activation_time > 5:
            self.isactive = False
class Button(UIElement):
    def __init__(self, x, y, width, height, element_id, json_file, color=(255, 255, 255), opacity=127, image=None, font=None, font_size=32, text_position='center', action=None, text='', text_color=(0,0,0), draggable=False, type=None):
        super().__init__(x, y, width, height, element_id, json_file, draggable, type)
        self.color = color
        self.opacity = opacity
        self.image = pygame.image.load(image) if image else None
        self.font = pygame.font.Font(None, font_size)
        self.text_position = text_position
        self.action = action
        self.text = text 
        self.text_color = text_color

        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        if self.image:
            screen.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), self.rect)
        else:
            s = pygame.Surface((self.rect.width, self.rect.height)) 
            s.set_alpha(self.opacity)  
            s.fill(self.color) 
            screen.blit(s, (self.rect.x, self.rect.y))  

        if self.text: 
            text = self.font.render(self.text, True, self.text_color) 
            text_rect = text.get_rect()

            if self.text_position == 'center':
                text_rect.center = self.rect.center
            elif self.text_position == 'top_left':
                text_rect.topleft = self.rect.topleft
            elif self.text_position == 'top_right':
                text_rect.topright = self.rect.topright
            elif self.text_position == 'bottom_left':
                text_rect.bottomleft = self.rect.bottomleft
            elif self.text_position == 'bottom_right':
                text_rect.bottomright = self.rect.bottomright
            elif self.text_position == 'left':
                text_rect.midleft = self.rect.midleft
            elif self.text_position == 'right':
                text_rect.midright = self.rect.midright
            elif self.text_position == 'top':
                text_rect.midtop = self.rect.midtop
            elif self.text_position == 'bottom':
                text_rect.midbottom = self.rect.midbottom

            screen.blit(text, text_rect)

    def handle_event(self, event):
        super().handle_mouse_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.rect.collidepoint(pos):
                if self.action:
                    self.action()

class Parallax:
    def __init__(self, images, screen):
        self.dx = 0
        self.dy = 0
        self.bg = []
        self.images = images
        self.screen = screen
        self.screen_size = self.screen.get_size()  
        self.update_images()

    def update_images(self):
        self.bg = []
        for image in self.images:
            back = pygame.image.load(image).convert_alpha()
            back = pygame.transform.scale(back, (back.get_width(), self.screen.get_height())) 
            self.bg.append(back)
        self.width = self.bg[0].get_width()
        self.height = self.screen.get_height() - self.bg[0].get_height()

    def draw(self, screen):
        for i, layer in enumerate(self.bg):
            speed = 1 + i * 0.8
            x = ((-self.dx * speed) % self.width) - self.width
            while x < self.screen.get_width():
                screen.blit(layer, (x, self.height + self.dy * speed))
                x += self.width

    def update(self, keys):
        if keys[pygame.K_LEFT] == True and self.dx > -3 * self.width:
            self.dx -= 2
        if keys[pygame.K_RIGHT] == True:
            self.dx += 2
        if keys[pygame.K_UP] == True and self.dy < self.screen.get_height():
            self.dy += 2
        elif keys[pygame.K_DOWN] == True and self.dy > 0:
            self.dy -= 2

        # Verifica si el tamaño de la pantalla ha cambiado
        if self.screen.get_size() != self.screen_size:
            self.screen_size = self.screen.get_size()
            self.update_images()

class Ray:
    def __init__(self, origin, angle, max_distance, color=(255, 255, 255)):
        self.origin = origin
        self.angle = angle % (2 * math.pi)
        self.max_distance = max_distance
        self.color = color
        
    def draw(self, screen):
        end = [self.origin[0] + self.max_distance * math.cos(self.angle), 
               self.origin[1] + self.max_distance * math.sin(self.angle)]
        pygame.draw.line(screen, self.color, self.origin, end)

    def collides_with(self, obstacles):
        end = [self.origin[0] + self.max_distance * math.cos(self.angle), 
               self.origin[1] + self.max_distance * math.sin(self.angle)]
        for obstacle in obstacles:
            if pygame.Rect(obstacle).colliderect(pygame.Rect(self.origin[0], self.origin[1], end[0], end[1])):
                return True
        return False
"""
    Beta test ver 1.2
"""
class Matrix2D:
    def __init__(self, rows, cols, x, y, width, height):
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.background_color = None
        self.cell_backgrounds = [[None for _ in range(cols)] for _ in range(rows)]

    def set_background_color(self, color):
        self.background_color = color

    def set_cell_background(self, row, col, background):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cell_backgrounds[row][col] = background

    def add_element(self, row, col, element):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = element

    def remove_element(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = None

    def draw(self, screen):
        # Draw background color
        if self.background_color is not None:
            screen.fill(self.background_color, (self.x, self.y, self.width, self.height))
        # Draw cell backgrounds
        cell_width = self.width / self.cols
        cell_height = self.height / self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cell_backgrounds[row][col] is not None:
                    pygame.draw.rect(screen, self.cell_backgrounds[row][col],
                                     (self.x + col * cell_width, self.y + row * cell_height, cell_width, cell_height))
        # Draw grid elements
        for row in range(self.rows):
            for col in range(self.cols):
                element = self.grid[row][col]
                if element is not None:
                    if isinstance(element, pygame.Surface):  # Check if element is an image
                        scaled_image = pygame.transform.scale(element, (int(cell_width), int(cell_height)))
                        screen.blit(scaled_image, (self.x + col * cell_width, self.y + row * cell_height))
                    elif isinstance(element, tuple) and len(element) == 3:  # Check if element is a color tuple
                        pygame.draw.rect(screen, element,
                                         (self.x + col * cell_width, self.y + row * cell_height, cell_width, cell_height))

    def get_clicked_cell(self, mouse_pos):
        x, y = mouse_pos
        col = (x - self.x) // (self.width / self.cols)
        row = (y - self.y) // (self.height / self.rows)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        else:
            return None

class PhysicsEngine:
    def __init__(self):
        pass

    def check_collision(self, obj1, obj2):
        # Verificar si hay colisión entre dos objetos
        return obj1.rect.colliderect(obj2.rect)

    def handle_collisions(self, objects_list1, objects_list2):
        # Manejar colisiones entre las dos listas de objetos
        for obj1 in objects_list1:
            for obj2 in objects_list2:
                if self.check_collision(obj1, obj2):
                    #print("Colisión detectada entre", obj1, "y", obj2)
                    self.resolve_collision(obj1, obj2)

    def resolve_collision(self, obj1, obj2):
        # Manejar la resolución de colisiones entre dos objetos
        dx = obj1.rect.x - obj2.rect.x
        dy = obj1.rect.y - obj2.rect.y

        if abs(dx) > abs(dy):
            # Colisión horizontal
            if dx > 0:
                # obj1 chocó con el lado derecho de obj2
                obj1.rect.x = obj2.rect.x + obj2.rect.width
            else:
                # obj1 chocó con el lado izquierdo de obj2
                obj1.rect.x = obj2.rect.x - obj1.rect.width
        else:
            # Colisión vertical
            if dy > 0:
                # obj1 chocó con la parte inferior de obj2
                obj1.rect.y = obj2.rect.y + obj2.rect.height
            else:
                # obj1 chocó con la parte superior de obj2
                obj1.rect.y = obj2.rect.y - obj1.rect.height
