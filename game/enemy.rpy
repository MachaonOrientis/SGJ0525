init python:
    class Enemy:
        def __init__(self, name, hp, sprite, sprite_pos, attack_range, anim=None):
            self.attack_range = attack_range
            self.name = name
            self.hp = hp
            self.hpmax = hp
            self.sprite = sprite
            self.sprite_pos = sprite_pos  # Горизонтальное смещение в ряду
            self.anim = anim              # Анимация (например, покачивание)
            self.dead = False
            self.damage_text = None  # Текст урона
            self.damage_time = 0.0   # Время отображения
        

default m1 = Enemy("Goblin", 15, "goblin.png", 0, (3, 7), sway)
default m2 = Enemy("Skeleton", 25, "skeleton.png", 250, (5, 10), sway)
default enemies_row1 = [m1,m2]
image bg forest = "bg.png"


screen display_enemies():
    fixed:
        # Верхний ряд
        pos (576, 448)
        for enemy in enemies_row1:
            if not enemy.dead:
                imagebutton:
                    idle enemy.sprite
                    xpos enemy.sprite_pos
                    anchor (0.5, 1.0)
                    action Return(enemy)  # Для выбора цели
                    at enemy.anim  # Анимация, если есть
                bar:
                    style "bar_mhp"
                    value AnimatedValue(enemy.hp, enemy.hpmax, delay=0.25)
                    xpos enemy.sprite_pos - 70
                # Текст урона
            if enemy.damage_text and (renpy.get_game_runtime() - enemy.damage_time < 1.5):
                text enemy.damage_text:
                    xpos enemy.sprite_pos + 50  # Смещение от спрайта
                    ypos -200
                    color "#FF0000"
                    at damage_animation

transform sway:
    linear 0.5 xoffset 10
    linear 0.5 xoffset -10
    repeat

transform damage_animation:
    alpha 0.0
    linear 0.3 alpha 1.0 yoffset 0
    linear 0.7 alpha 0.0 yoffset -50

transform enter_from_top(y_final):
    ypos -400  # Начальная позиция за верхним краем
    easein 1.0 ypos y_final

transform move_anim(old_y,new_y):
    linear 1.0 ypos new_y
    linear 0.5 ypos old_y



screen damage_player1(text):
    # Всплывающее окно с текстом
    zorder 100
    timer 2.0 action Hide("damage_player1")
    text text:
        xalign 0.4
        yalign 0.8
        color "#cc3a3a"
        outlines [(2, "#000", 0, 0)]
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0
            pause 0.5
            linear 0.5 alpha 0.0

screen heal_player(text,x_pos):
    zorder 100
    timer 2.0 action Hide("heal_player")
    text text:
        xalign x_pos
        yalign 0.8
        color "#00FF00"
        outlines [(2, "#000", 0, 0)]
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0
            pause 0.5
            linear 0.5 alpha 0.0

screen damage_player2(text):
    # Всплывающее окно с текстом
    zorder 100
    timer 2.0 action Hide("damage_player2")
    text text:
        xalign 0.6
        yalign 0.8
        color "#cc3a3a"
        outlines [(2, "#000", 0, 0)]
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0
            pause 0.5
            linear 0.5 alpha 0.0

label test:
    scene bg forest
    $ selected_enemy = None
    $ battle_active = True
    $ players_turn = True
    $ current_player = 1

    while battle_active:
        if players_turn:
            # Ход игроков
            window hide
            show screen health1
            show screen health2
            show screen display_enemies
            show screen player1
            show screen player2
            show screen display_enemies
        
            

            call screen bottom_left_buttons
            if _return == "attack":
                if selected_damage == "heal":
                    # Лечение
                    if current_player == 1:
                        $ health1_int = min(100, health1_int + 20)
                        $ renpy.show_screen("heal_player", "+20",0.4)
                    else:
                        $ health2_int = min(100, health2_int + 20)
                        $ renpy.show_screen("heal_player", "+20",0.6)
                    # Сбрасываем выбранное действие
                    $ selected_damage = 0
                    $ renpy.pause(1,hard=True)
                else:
                    # Атака
                    call screen display_enemies
                    $ selected_enemy = _return

                if selected_enemy:  # Если враг выбран
                    # Преобразуем урон в число
                    $ damage = int(selected_damage)
                    $ selected_enemy.hp -= selected_damage
                    $ selected_enemy.hp = max(0, selected_enemy.hp)
                    $ selected_enemy.damage_text = f"-{selected_damage}"
                    $ selected_enemy.damage_time = renpy.get_game_runtime()

                    $ selected_enemy.damage_text = f"-{selected_damage}"
                    $ selected_enemy.damage_time = renpy.get_game_runtime()

                    # Проверка смерти врага
                    if selected_enemy.hp <= 0:
                        $ selected_enemy.dead = True
                        $ selected_enemy.damage_text = "ПОБЕЖДЁН"


                    # Увеличиваем счётчик ходов текущего игрока
                    $ player_turns[current_player] += 1
                    
                    # Передача хода другому игроку или врагам
                    if current_player == 2:
                        # Оба игрока сходили — передаём ход врагам
                        $ players_turn = False
                        $ current_player = 1
                    else:
                        # Передаём ход второму игроку
                        $ current_player = 2
            
            

        else:
            show screen display_enemies
            # Ход врагов
            python:
                for enemy in enemies_row1:
                    if not enemy.dead and renpy.random.random() < 0.8:
                        enemy.anim = move_anim(0,100)

                        # Логика атаки
                        damage = renpy.random.randint(*enemy.attack_range)
                        target = renpy.random.choice([1, 2])
                        
                        if target == 1:
                            store.last_health1 = store.health1_int
                            store.health1_int = max(0, store.health1_int - damage)
                            renpy.show_screen("damage_player1", f"-{damage}")
                        else:
                            store.last_health2 = store.health2_int
                            store.health2_int = max(0, store.health2_int - damage)
                            renpy.show_screen("damage_player2", f"-{damage}")
                        
                        renpy.pause(2, hard=True)
                        enemy.anim = sway
                    else:
                        renpy.pause(0.2, hard=True)
                renpy.store.global_turn += 1
            
            # Проверка смерти игроков
            if health1_int <= 0 or health2_int <= 0:
                jump battle_lost
                
            $ players_turn = True
        
        # Проверка победы
        if all(enemy.dead for enemy in enemies_row1):
            jump battle_won
                
    return

label battle_lost:
    "Ваша команда пала в бою!"
    return

label battle_won:
    "Все враги повержены!"
    return