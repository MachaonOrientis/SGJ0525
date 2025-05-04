
default current_player = 1  # Текущий игрок (1 или 2)
default selected_damage = 0 # Выбранный урон
default player_names = {1: "Игрок 1", 2: "Игрок 2"}
default player_turns = {1: 0, 2: 0}          # Счётчик ходов каждого игрока
default attack_cooldowns = {}                 # Формат: {(player, damage): last_used_turn}
default global_turn = 0
default cooldown_values = {
    1: {10: 0, 20: 2, "heal": 3},  # Игрок 1: 10 (без КД), 20 (КД 1), хил 20 (КД 2)
    2: {10: 0, 20: 2, "heal": 3}   # Игрок 2: 10 (без КД), 20 (КД 1), хил 10 (КД 2)
}

default player2_sprites = {
    1: "player2.png",
    2: "player3.png"
}


default player_sets = {
    "set1": {
        1: {"health": 40, "heal_power": 10, "cooldowns": {10: 0, 20: 2, "heal": 3}},
        2: {"health": 30, "heal_power": 10, "cooldowns": {10: 0, 20: 2, "heal": 3}}
    },
    "set2": {
        1: {"health": 50, "heal_power": 20, "cooldowns": {10: 0, 20: 2, "heal": 3}},
        2: {"health": 30, "heal_power": 10, "cooldowns": {10: 0, 20: 2, "heal": 3}}
    },
    "set3": {
        1: {"health": 60, "heal_power": 20, "cooldowns": {10: 0, 20: 2, "heal": 3}},
        2: {"health": 30, "heal_power": 10, "cooldowns": {10: 0, 20: 2, "heal": 3}}
    },
    "set4": {
        1: {"health": 70, "heal_power": 20, "cooldowns": {10: 0, 20: 2, "heal": 0}},
        2: {"health": 50, "heal_power": 20, "cooldowns": {10: 0, 20: 2, "heal": 0}}
    }
}

default current_player_set = "set4"


style cooldown_text:
    size 24
    color "#FFFFFF"
    outlines [(2, "#000000", 0, 0)]
    bold True

screen player_turn_label():
    zorder 300
    fixed:
        xalign 0.0
        yalign 1.0
        xoffset 40
        yoffset -70  # Позиция над кнопками
        
        text "[player_names[current_player]] ходит":
            color "#FFF"
            size 32

default health1_int = 36
default health2_int = 23

transform slide_from_bottom(start_y=1.1, end_y=0.9, delay=0.0):
    ycenter start_y  # Начальная позиция
    pause delay
    easeout 0.5 ycenter end_y  # Плавное движение к конечной позиции
    on hide:  # Анимация при скрытии
        easeout 0.5 ycenter start_y

transform player_damage_anim:
    linear 0.1 xoffset 10
    linear 0.1 xoffset -10
    linear 0.1 xoffset 0

transform Empty:
    pass

transform slide_from_top(start_y=1.1, end_y=0.9, delay=0.0):
    pass

default last_health1 = 36  # Добавляем переменную для отслеживания здоровья
default last_health2 = 23

screen health1():
    zorder 100
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "health_img.png":
            zoom 0.2
            xcenter 0.4  
            ycenter 0.9

        # Текст
        text "Здоровье: [health1_int]":
            xcenter 0.4  
            ycenter 0.95
            color "#ffffff"
            size 24

screen health2():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "health_img.png":
            zoom 0.2
            xcenter 0.6  
            ycenter 0.9

        # Текст
        text "Здоровье: [health2_int]":
            xcenter 0.6  
            ycenter 0.95
            color "#ffffff"
            size 24


screen player1():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add player2_sprites[current_player2_sprites]:
            zoom 0.4
            xcenter 0.6  
            ycenter 0.73

screen player2():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "player1.jpg":
            zoom 0.4
            xcenter 0.4  
            ycenter 0.73

init python:
    def update_cooldown(player, damage):
        store.attack_cooldowns[(player, damage)] = store.global_turn

transform slide_from_left(delay=0.0): 
    xysize(300,100)
    pause delay
    xpos -400  # Начальная позиция за левым краем экрана
    easeout 0.5 xpos 20  # Плавное движение к конечной позиции
    on hide:  # Анимация при скрытии
        easeout 0.5 xpos -500

transform show_with_delay():
    alpha 0.0
    pause(1)
    linear 0.5 alpha 1.0

screen bottom_left_buttons:
    # Основной контейнер для позиционирования
    fixed:
        xalign 0.0    # Прижимаем к левому краю
        yalign 1.0    # Прижимаем к нижнему краю
        xoffset 40  # Отступы от края
        yoffset -200
        xysize (300,250)

        use player_turn_label

        # Вертикальный контейнер для кнопок (снизу вверх)
        vbox:
            spacing 1
            # Кнопка 1
            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left
                    sensitive True  # Всегда активна
                    action [
                        SetVariable("selected_damage", 10),
                        Return("attack")
                    ]
                # Текст для кнопки 1
                text "Урон 10":
                    at show_with_delay
                    xalign 0.5
                    yalign 0.5
                    style "cooldown_text"
                    color "#ffffff"

            # Кнопка 2
            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left(0.3)
                    sensitive ( 
                        (store.global_turn - store.attack_cooldowns.get((current_player, 20), -999)) 
                        > cooldown_values[current_player].get(20, 0)
                    )
                    action [
                        SetVariable("selected_damage", 20),
                        Function(update_cooldown, current_player, 20),
                        Return("attack")
                    ]
                # Текст для кнопки 2
                text "Урон 20":
                    at show_with_delay
                    xalign 0.5
                    yalign 0.5
                    style "cooldown_text"
                    color "#ffffff"

            # Кнопка 3
            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left(0.6)
                    sensitive ( 
                        (store.global_turn - store.attack_cooldowns.get((current_player, "heal"), -999)) 
                        >= cooldown_values[current_player].get("heal", 0)
                    )
                    action [
                        SetVariable("selected_damage", "heal"),  # Меняем тип действия
                        Function(update_cooldown, current_player, "heal"),
                        Return("attack")
                    ]
                # Текст для кнопки 3 с динамическим значением
                text "Хил [heal_power[current_player]]":
                    at show_with_delay
                    xalign 0.5
                    yalign 0.5
                    style "cooldown_text"
                    color "#ffffff"

