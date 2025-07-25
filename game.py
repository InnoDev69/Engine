import pygame
import traceback
import inspect
from object import *
from sound_manager import SoundManager
from engineExtends import *

class Game:
    def __init__(self):
        try:
            self.init_window()
            self.init_state()
            self.init_ui()
            self.init_cameras()
            self.sound = SoundManager()
            self.engine_physics = PhysicsEngine()
        except Exception as e:
            self.handle_exception("constructor", e)

    def init_window(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE, pygame.SCALED)
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.BLACK = (0, 0, 0)

    def init_state(self):
        self.refresh_rate = 60
        self.pause = False
        self.developer_mode = True
        self.popup = PopUp()
        self.objects = []
        self.entitys = [GameObject(self.screen_width/2, 0, 51, 51, (0,255,0), None, "Block", 5)]
        self.others = []
        self.camera_x = 0
        self.fullscreen = False
        self.show_menu = False
        self.show_fps = False
        self.hitboxes = False
        self.variable2 = False

    def init_ui(self):
        self.ui_elements = [
            TextInput(
                text="",
                position=(50, 50),
                font_size=20,
                width=200,
                height=40,
                color=(255, 255, 255),
                background_color=(0, 0, 0),
                element_id="text_input_1",  # Un identificador único para este elemento
                json_file="data/positions.json",
                draggable=self.developer_mode,
                type="menu"
            ),
            TextBlock(
                        x=20,
                        y=20,
                        width=200,
                        height=50,
                        text=f"{self.clock.get_fps()}",
                        font_size=24,
                        font_color=(255,255,255),
                        draw_background=False,
                        element_id="fps_text",  
                        json_file="data/positions.json",
                        draggable=self.developer_mode,
                        type="menu"
                    ),
            TextBlock(
                        x=20,
                        y=20,
                        width=200,
                        height=50,
                        text=f"",
                        font_size=24,
                        font_color=(255,255,255),
                        draw_background=False,
                        element_id="chat_text",  
                        json_file="data/positions.json",
                        draggable=self.developer_mode,
                        type="menu"
                    ),
            TextBlock(
                        x=20,
                        y=20,
                        width=200,
                        height=50,
                        text=f"",
                        font_size=24,
                        font_color=(255,255,255),
                        draw_background=False,
                        element_id="info",  
                        json_file="data/positions.json",
                        draggable=self.developer_mode,
                        type="menu"
                    ),
            Button(50,50,100,50,"boton","data/positions.json", opacity=255,text="Hola", text_color=(0,0,0), action=lambda:self.popup.activate("a"),draggable=self.developer_mode,type="menu")
        ]

    def init_cameras(self):
        self.camera = Camera(self.screen_width, self.screen_height)
        self.free_camera = FreeCamera(self.screen_width, self.screen_height)
        self.current_camera = self.camera
        self.free_camera_mode = False

    def handle_exception(self, context, e):
        l = traceback.format_exc()
        print(f"Error in {context}: {e} {l}")
        self.popup.activate(f"Error en {context}: {e} {l}")

    def method_requires_argument(self,method, arg_name):
        sig = inspect.signature(method)
        return arg_name in sig.parameters
    
    def on_toggle_f3(self):
        self.free_camera_mode = not self.free_camera_mode
        if self.free_camera_mode:
            print("Modo de cámara libre habilitado. Usa las flechas del teclado para mover la cámara.")
            self.current_camera = self.free_camera
        else:
            print("Modo de cámara libre deshabilitado. La cámara seguirá al jugador.")
            self.current_camera = self.camera
            try:
                self.current_camera.set_target(self.entitys[0])
            except Exception as e:
                print(f"Failed to set target for {e.args}")
                self.popup.activate(f"Failed to set target for {e.args}")
               
    def handle_menu_click(self, evt):
        try:
            if self.show_menu:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.width - 150 <= mouse_x <= self.width and 0 <= mouse_y <= 120:
                    self.hitboxes = not self.hitboxes
                elif self.width - 150 <= mouse_x <= self.width and 150 <= mouse_y <= 270:
                    self.variable2 = not self.variable2
                elif self.width - 150 <= mouse_x <= self.width and 300 <= mouse_y <= 420:
                    self.show_fps = not self.show_fps
        except Exception as e:
            self.handle_exception("run", e)
                        
    def can_view(self, x, y, object_width, object_height):
        try:
            w,h=self.screen.get_size()
            object_left = x - self.current_camera.x
            object_right = x + object_width - self.current_camera.x
            object_top = y - 0  
            object_bottom = y + object_height - 0  

            return (object_right > 0 and object_left < w and
                    object_bottom > 0 and object_top < h)
        except Exception as e:
            self.handle_exception("run", e)
    def toggle_free_camera(self):
        try:
            if isinstance(self.current_camera, FreeCamera):
                self.current_camera = self.camera
                self.current_camera.set_target(self.player)
            else:
                self.current_camera = self.free_camera
                self.current_camera.set_target(None)
        except Exception as e:
            self.handle_exception("run", e)

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                row = 0
                for line in file:
                    col = 0
                    for char in line.strip():
                        if char == ' ':
                            block_type = 0
                            collidable = False
                        elif char == '1':
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, True, texture="textures/bricks.png", color=None,
                                        kill=False, typeObj="Block")
                            self.objects.append(block)
                        elif char == '2':
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, True, texture=None, color=None, kill=True, typeObj="Block")
                            self.objects.append(block)
                        elif char == '3':
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, True, texture="textures/floor.png", color=None,
                                        kill=False, typeObj="Block")
                            self.objects.append(block)
                        else:
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, False, texture=None, color=None, kill=False, typeObj="Block")
                        col += 1
                    row += 1
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'load_map' func, more details:{e} {l}")
            print(f"{e}{l}")
    
    def set_background(self, background_image):
        try:
            self.background_images = [
                pygame.image.load("textures/background/background_layer1.png").convert(),
                pygame.image.load("textures/background/background_layer2.png").convert()
            ]
            self.background = pygame.transform.scale(self.background_images[0], (self.screen_width, self.screen_height))
        except Exception as e:
            self.handle_exception("run", e)
            
    def reescale(self)->None:
        try:
            scale_x = self.screen_width / 1360
            scale_y = self.screen_height / 720
            for object in self.objects:
                object.x *= scale_x
                object.y *= scale_y
                object.rect.x *= scale_x
                object.rect.y *= scale_y
                object.rect.width = round(object.rect.width * scale_x)
                object.rect.height = round(object.rect.height * scale_y)
                object.width *= scale_x
                object.height *= scale_y
                object.texture = pygame.transform.scale(object.texture, (object.width, object.height))
            for entity in self.entitys:

                entity.rect.x *= scale_x
                entity.rect.y *= scale_y
                entity.rect.width = round(entity.rect.width * scale_x)
                entity.rect.height = round(entity.rect.height * scale_y)
                entity.width *= scale_x
                entity.height *= scale_y
                if entity.texture:entity.texture = pygame.transform.scale(entity.texture, (entity.width, entity.height))
                else:                    
                    entity.surface = pygame.Surface((entity.width, entity.height))
                    entity.surface.fill(entity.color)
            for element in self.ui_elements:

                element.rect.x *= scale_x
                element.rect.y *= scale_y
                element.rect.width *= scale_x
                element.rect.height *= scale_y

        except Exception as e:
            self.handle_exception("run", e)
    def donwscale(self)->None:
        try:
            scale_x = self.screen_width / 1360
            scale_y = self.screen_height / 720
            for object in self.objects:
                
                object.rect.x /= scale_x
                object.rect.y /= scale_y
                object.rect.width = round(object.rect.width / scale_x)
                object.rect.height = round(object.rect.height / scale_y)

                object.x /= scale_x
                object.y /= scale_y
                object.width /= scale_x
                object.height /= scale_y
                if object.texture:object.texture = pygame.transform.scale(object.texture, (object.width, object.height))
                else:                    
                    object.surface = pygame.Surface((object.width, object.height))
                    entity.surface.fill(object.color)
            for entity in self.entitys:

                entity.rect.x /= scale_x
                entity.rect.y /= scale_y
                entity.rect.width = round(entity.rect.width / scale_x)
                entity.rect.height = round(entity.rect.height / scale_y)

                entity.width /= scale_x
                entity.height /= scale_y
                if entity.texture:entity.texture = pygame.transform.scale(entity.texture, (entity.width, entity.height))
                else:                    
                    entity.surface = pygame.Surface((entity.width, entity.height))
                    entity.surface.fill(entity.color)
            for element in self.ui_elements:

                element.rect.x /= scale_x
                element.rect.y /= scale_y
                element.rect.width /= scale_x
                element.rect.height /= scale_y

        except Exception as e:
            self.handle_exception("run", e)
    def handle_events(self, event)->None:
        try:
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                if width <= self.screen_width and height <= self.screen_height:
                    self.reescale()
                else:
                    self.donwscale()
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
            if event.type == pygame.QUIT:
                self.exit = True
            if self.developer_mode:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:self.on_toggle_f3()  
                    elif event.key == pygame.K_F4:self.show_menu = not self.show_menu
                    elif event.key == pygame.K_ESCAPE:self.pause = not self.pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_menu_click(event)
                elif self.free_camera_mode:self.current_camera.handle_event(event)
                if self.show_menu:
                    for element in self.ui_elements:
                        if self.method_requires_argument(getattr(element, 'handle_event'), 'game'):
                            element.handle_event(event, game)
                        else:
                            element.handle_event(event)
        except Exception as e:
            self.handle_exception("run", e)
    def draw_menu(self)->None:
        try:
            self.width, self.height = self.screen.get_size()  # Actualiza las dimensiones de la ventana

            pygame.draw.rect(self.screen, (200, 200, 200), (self.width - 150, 0, 150, self.height))

            checkbox1_rect = pygame.Rect(self.width - 140, 20, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox1_rect, 2)
            if self.hitboxes:
                pygame.draw.rect(self.screen, self.BLACK, checkbox1_rect)

            checkbox2_rect = pygame.Rect(self.width - 140, 170, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox2_rect, 2)
            if self.variable2:
                pygame.draw.rect(self.screen, self.BLACK, checkbox2_rect)

            checkbox_fps_rect = pygame.Rect(self.width - 140, 320, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox_fps_rect, 2)
            if self.show_fps:
                pygame.draw.rect(self.screen, self.BLACK, checkbox_fps_rect)

            # Render FPS text
            fps_text = self.font.render("Show FPS", True, self.BLACK)
            self.screen.blit(fps_text, (self.width - 140, 290))
        except Exception as e:
            self.handle_exception("run", e)
    def run(self):
        try:
            self.reescale()
            running = True
            while running:
                dt = self.clock.tick(60) / 1000
                self.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    self.handle_events(event)
                keys = pygame.key.get_pressed()
                #self.fore.update(keys) nose porque da un error
                if not self.pause:
                    self.update(keys, event)
                self.clock.tick(self.refresh_rate)
            pygame.quit()
        except Exception as e:
            self.handle_exception("run", e)

    def draw_rects_and_lines(self,screen, obj, camera):
        color = (255, 255, 255) 

        adjusted_rect = obj.rect.move(-camera.x, -camera.y)

        pygame.draw.rect(screen, color, adjusted_rect, 2)

    def draw_objects(self):
        try:
            chunk_size = 100

            start_index = max(0, int(self.current_camera.x / 50) - chunk_size)
            end_index = min(len(self.objects), int((self.current_camera.x + self.screen_width) / 50) + chunk_size)

            for object in self.objects[start_index:end_index]:
                if self.can_view(object.x, object.y, object.width, object.height):
                    #object.update()
                    object.draw(self.screen, self.current_camera)
                    if self.hitboxes:self.draw_rects_and_lines(self.screen, object, self.current_camera)
            for entity in self.entitys[start_index:end_index]:
                entity.draw(self.screen, self.current_camera)
                if self.hitboxes:self.draw_rects_and_lines(self.screen, entity, self.current_camera)

        except Exception as e:
            self.handle_exception("run", e)
    def update_visuals(self):
        try:

            self.draw_objects()
            if self.show_menu:
                self.draw_menu()            
            # Display FPS if enabled
            for element in self.ui_elements:
                if element.element_id == "fps_text" and self.show_fps:
                    element.update_content()
                    element.update(f"{self.clock.get_fps()}")
                    element.draw(self.screen)

                elif self.show_menu and not element.element_id == "fps_text":
                    element.draw(self.screen)
                elif not element.herarchy=="menu":
                    element.draw(self.screen)

            if self.popup.isactive:
                self.popup.draw_popup(self.screen)
                self.popup.update()
            for other in self.others:
                other.draw(self.screen)
            pygame.display.update()
        except Exception as e:
            self.handle_exception("run", e)

    def update(self, keys, event):
        try:
            self.engine_physics.handle_collisions(self.entitys,self.objects)
            for entity in self.entitys:
                entity.update()
            for obj in self.objects:
                obj.update() 
            self.current_camera.update()
            if self.current_camera.y >= -105:
                self.current_camera.y = -105
        except Exception as e:
            self.handle_exception("run", e)
    def render(self):
        try:
            self.screen.fill((0,0,0))
            self.update_visuals()
            pygame.display.flip()
        except Exception as e:
            self.handle_exception("run", e)
if __name__ == "__main__":
    game = Game()
    game.load_map("sources/map.txt")
    game.run()