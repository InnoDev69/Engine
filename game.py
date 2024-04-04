import pygame
import time
import traceback
import inspect
from sound_manager import SoundManager
from animation import Animation
from block import Block
from particle import *
from emitter import *
from basics import *    
class Game:
    def __init__(self):
        try:
            pygame.init()
            self.screen_width = 800
            self.screen_height = 600
            self.width = self.screen_width
            self.height = self.screen_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            self.start_time = pygame.time.get_ticks()
            pygame.display.set_caption("Game")
            self.refresh_rate = 60
            self.pause = False
            self.developer_mode = True
            self.popup=False
            self.popup = PopUp()
            
            self.objects=[]
            self.entitys=[GameObject(800/2, 600/2, 50, 50, (0,255,0), None,5),GameObject(800/2, 600/2-300, 50, 50, (0,255,0), None,5),]
            self.others = [Ray((400, 300), math.pi / 4, 200)]

            self.camera_x = 0
            self.white = (255, 255, 255)
            self.clock = pygame.time.Clock()

            self.sound = SoundManager()
            
            self.textures = {}
            self.initialize_textures()
            
            self.camera = Camera(self.screen_width, self.screen_height)
            self.free_camera = FreeCamera(self.screen_width, self.screen_height)
            self.current_camera = self.camera
            self.free_camera_mode = False

            #global
            self.show_menu = False
            self.show_fps = False
            self.variable1 = False
            self.variable2 = False
            self.font = pygame.font.Font(None, 36)
            self.fullscreen = False
            #colors
            self.BLACK = (0,0,0)
            self.images=("textures\\background\\background_layer1.png","textures\\background\\background_layer1.png")
            self.fore = Parallax(self.images, self.screen)
            #asd
            self.ui_elements=[TextInput(
                text="",
                position=(50, 50),
                font_size=20,
                width=200,
                height=40,
                color=(255, 255, 255),
                background_color=(0, 0, 0),
                element_id="text_input_1",  # Un identificador único para este elemento
                json_file="data/positions.json",
                draggable=self.developer_mode # El archivo JSON donde se guardarán las posiciones
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
                        draggable=self.developer_mode
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
                        draggable=self.developer_mode
                    ),
            Button(50,50,100,50,"boton","data/positions.json", opacity=255,text="Hola", text_color=(0,0,0), action=lambda:self.popup.activate("a"),draggable=self.developer_mode)]
            
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error en constructor:{e.args} {l}")

            
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
                self.current_camera.set_target(self.player)
            except Exception as e:
                print(f"Failed to set target for {e.args}")
                self.popup.activate(f"Failed to set target for {e.args}")
               
    def handle_menu_click(self, evt):
        try:
            if self.show_menu:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.width - 150 <= mouse_x <= self.width and 0 <= mouse_y <= 120:
                    self.variable1 = not self.variable1
                elif self.width - 150 <= mouse_x <= self.width and 150 <= mouse_y <= 270:
                    self.variable2 = not self.variable2
                elif self.width - 150 <= mouse_x <= self.width and 300 <= mouse_y <= 420:
                    self.show_fps = not self.show_fps
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'handle_menu_click' func, more details:{e} {l}")
                        
    def initialize_textures(self):
        try:
            for object in self.objects:
                if object.texture and object.texture not in self.textures:
                    image = pygame.image.load(object.texture)
                    if image:
                        image = pygame.transform.scale(image, (object.width, object.height))
                        self.textures[object.texture] = image
                    else:
                        self.textures[object.texture] = object.color 
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'initialize_textures' func, more details:{e} {l}")
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
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'can_view' func, more details:{e} {l}")
    def toggle_free_camera(self):
        try:
            if isinstance(self.current_camera, FreeCamera):
                self.current_camera = self.camera
                self.current_camera.set_target(self.player)
            else:
                self.current_camera = self.free_camera
                self.current_camera.set_target(None)
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'run' func, more details:{e} {l}")

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
                                        kill=False)
                            self.objects.append(block)
                        elif char == '2':
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, True, texture=None, color=None, kill=True)
                            self.objects.append(block)
                        elif char == '3':
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, True, texture="textures/floor.png", color=None,
                                        kill=False)
                            self.objects.append(block)
                        else:
                            block_type = int(char)
                            block = Block(col * 50, row * 50, block_type, False, texture=None, color=None, kill=False)
                        col += 1
                    row += 1
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'run' func, more details:{e} {l}")
    def set_background(self, background_image):
        try:
            self.background_images = [
                pygame.image.load("textures/background/background_layer1.png").convert(),
                pygame.image.load("textures/background/background_layer2.png").convert()
            ]
            self.background = pygame.transform.scale(self.background_images[0], (self.screen_width, self.screen_height))
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'run' func, more details:{e} {l}")
    def BoxCollider(self, object_list, entity_list):
        for obj in object_list:
            for entity in entity_list:
                if obj.rect.colliderect(entity.rect):
                
                    dx = entity.rect.centerx - obj.rect.centerx 
                    dy = entity.rect.centery - obj.rect.centery 

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            entity.x = entity.rect.right
                            entity.velocity = 0
                        else:
                            entity.x = entity.rect.left - obj.width
                            entity.velocity = 0
                    else:
                        if dy > 0:
                            entity.y = obj.rect.bottom
                            entity.velocity = 0
                        else:
                            entity.y = obj.rect.top - entity.height
                            entity.velocity = 0

                else:
                    entity.velocity = entity.fvel
                    
        if False:
            for i in range(len(entity_list)):
                for j in range(i+1, len(entity_list)):
                    if entity_list[i].rect.colliderect(entity_list[j].rect):
                   
                        dx = entity_list[j].rect.centerx - entity_list[i].rect.centerx
                        dy = entity_list[j].rect.centery - entity_list[i].rect.centery

                        if abs(dx) > abs(dy):
                            if dx > 0:
                                entity_list[i].x = entity_list[j].rect.right
                                entity_list[i].velocity = 0
                            else:
                                entity_list[i].x = entity_list[j].rect.left - entity_list[i].width
                                entity_list[i].velocity = 0
                        else:
                            if dy > 0:
                                entity_list[i].y = entity_list[j].rect.bottom
                                entity_list[i].velocity = 0
                            else:
                                entity_list[i].y = entity_list[j].rect.top - entity_list[i].height
                                entity_list[i].velocity = 0
                        entity_list[i].velocity = 0  # Establecer la velocidad de la entidad a 0
    def run(self):
        try:
            running = True
            self.initialize_textures()
            chat = ""
            print(len(self.objects))
            while running:
                self.render()
                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - self.start_time) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.VIDEORESIZE:
                        width, height = event.w, event.h
                        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                        for object in self.objects:
                            scale_x = self.screen_width / 800
                            scale_y = self.screen_height / 600

                            object.x *= scale_x
                            object.y *= scale_y
                            object.width *= scale_x
                            object.height *= scale_y
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            toggle_fullscreen()
                    if event.type == pygame.QUIT:
                        self.exit = True
                        running = False
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
                keys = pygame.key.get_pressed()
                self.fore.update(keys)
                if not self.pause:
                    self.update(keys, event)
                    #######################
                    # Todo codigo aqui, la logica principal debe ir aqui
                self.clock.tick(self.refresh_rate)

            pygame.quit()
            sys.exit()
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'run' func, more details:{e} {l}")
    def draw_objects(self):
        try:
            chunk_size = 60

            start_index = max(0, int(self.current_camera.x / 50) - chunk_size)
            end_index = min(len(self.objects), int((self.current_camera.x + self.screen_width) / 50) + chunk_size)

            for object in self.objects[start_index:end_index]:
                if self.can_view(object.x, object.y, object.width, object.height):
                    object.update()
                    object_rect = self.current_camera.apply(pygame.Rect(object.x, object.y, object.width, object.height))
                    texture = self.textures.get(object.texture)
                    if texture:
                        self.screen.blit(texture, object_rect)
                    else:
                        pygame.draw.rect(self.screen, object.color, object_rect)
            for entity in self.entitys:
                entity.draw(self.screen, self.current_camera)
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'draw_objects' func, more details:{e} {l}")
    def update_visuals(self):
        try:
            self.fore.draw(self.screen)
            self.draw_objects()
            if self.show_menu:
                self.width, self.height = self.screen.get_size()  # Actualiza las dimensiones de la ventana

                pygame.draw.rect(self.screen, (200, 200, 200), (self.width - 150, 0, 150, self.height))

                checkbox1_rect = pygame.Rect(self.width - 140, 20, 20, 20)
                pygame.draw.rect(self.screen, self.BLACK, checkbox1_rect, 2)
                if self.variable1:
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
                
            # Display FPS if enabled
            for element in self.ui_elements:
                if element.element_id == "fps_text" and self.show_fps:
                    element.update_content()
                    element.update(f"{self.clock.get_fps()}")
                    element.draw(self.screen)
                if self.show_menu and not element.element_id == "fps_text":
                    element.draw(self.screen)
            if self.popup.isactive:
                self.popup.draw_popup(self.screen)
                self.popup.update()
            for other in self.others:
                other.draw(self.screen)
                other.angle +=1 / 60 
            pygame.display.update()
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'update_visuals' func, more details:{e} {l}")

    def update(self, keys, event):
        try:
            for entity in self.entitys:
                entity.update()
            self.BoxCollider(self.objects, self.entitys)
            self.current_camera.update()
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'update' func, more details:{e} {l}")
    def render(self):
        try:
            self.screen.fill((0,0,0))
            self.update_visuals()
            pygame.display.flip()
        except Exception as e:
            l=traceback.format_exc()
            self.popup.activate(f"Error in 'render' func., more details:{e} {l}")
        #crear la consola con un text input habilitado para eso sin capacidad de moverlo
if __name__ == "__main__":
    game = Game()
    game.load_map("sources/map.txt")
    game.run()