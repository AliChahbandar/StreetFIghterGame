import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size =data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0-1 = idle-death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) #player hitbox
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True


    #load images
    def load_images(self, sprite_sheet, animation_steps):
        #extract sprite sheet images
        animation_list = []
        y = 0
        for animation in animation_steps:
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x *self.size, y* self.size, self.size, self.size)#multiple x by self.size so it moves along the next square
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
            y+= 1
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0  #change in x cordinate and y
        dy = 0
        self.running = False
        self.attack_type = 0


        #keypresses
        key = pygame.key.get_pressed()

        #no actions when attacking
        if self.attacking == False and self.alive ==True and round_over ==False:
            #check player 1 controlds
            if self.player == 1:

        
                #movment
                if key[pygame.K_a]: #negative speed = move left and vis versa
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                    
                #jump 
                if key [pygame.K_w] and self.jump == False:
                    self.vel_y = - 30
                    self.jump = True

                #attacks
                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(target)
                    #which attack was used
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[ pygame.K_r]:
                        self.attack_type = 2

            #player 2
            if self.player == 2:

        
                #movment
                if key[pygame.K_LEFT]: #negative speed = move left and vis versa
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                    
                #jump 
                if key [pygame.K_UP] and self.jump == False:
                    self.vel_y = - 30
                    self.jump = True

                #attacks
                if key[pygame.K_j] or key[pygame.K_k]:
                    self.attack(target)
                    #which attack was used
                    if key[pygame.K_j]:
                        self.attack_type = 1
                    if key[ pygame.K_k]:
                        self.attack_type = 2




        #Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y   

        #player stays on screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left #stops at the edge of the screen
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False  #jump resets back to false so you can jump again
            dy = screen_height - 110 - self.rect.bottom

        #players face eachother
        if target.rect.centerx > self.rect.centerx:
            self.flip =False
        else:
            self.flip = True

        #attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        #update player pos
        self.rect.x += dx
        self.rect.y += dy


    #Update animation
    def update(self):
        #check the action the player is preforming
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#death
        elif self.hit == True:
            self.update_action(5)#hit
        elif self.attacking ==True:
            if self.attack_type ==1:
                self.update_action(3)#attack 1
            elif self.attack_type == 2:
                self.update_action(4) #attack 2
        elif self.jump == True:
            self.update_action(2)#jump
        elif self.running ==True:
            self.update_action(1)#run
        else:
            self.update_action(0)#iddle

        animation_cooldown = 60
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if the next update can go through
        if pygame.time.get_ticks()- self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):#if it goes to the end of animation restart it
            #check if player is day then end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #check if attack happened
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
                #check if damage was taken
                if self.action ==5:
                    self.hit = False
                    #if the player was in the middle of the attack then the attack is stopped
                    self.attacking =False
                    self.attack_cooldown = 30


    def attack(self, target):
        if self.attack_cooldown == 0:
            

            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx-(2* self.rect.width*self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)#the attack will span double the players width
            if attacking_rect.colliderect(target.rect): #collision detection
                target.health -=10
                target.hit = True
        
        
       


    def update_action(self, new_action):
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x -(self.offset[0]* self.image_scale), self.rect.y- (self.offset[1]* self.image_scale)))