
default current_player = 1  # Текущий игрок (1 или 2)
default selected_damage = 0 # Выбранный урон
default player_names = {1: "Игрок 1", 2: "Игрок 2"}
default player_turns = {1: 0, 2: 0}          # Счётчик ходов каждого игрока
default attack_cooldowns = {}                 # Формат: {(player, damage): last_used_turn}
default global_turn = 0
default cooldown_values = {
    1: {10: 2, "heal": 3},  # Игрок 1: лечение - 3 хода
    2: {10: 2, "heal": 3}   # Игрок 2: лечение - 3 хода
}

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
        add "player1.jpg":
            zoom 0.3
            xcenter 0.6  
            ycenter 0.75

screen player2():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "player1.jpg":
            zoom 0.3
            xcenter 0.4  
            ycenter 0.75

init python:
    def update_cooldown(player, damage):
        # Обновляем КД только для атак с КД > 0
        if damage in store.cooldown_values.get(player, {}):
            store.attack_cooldowns[(player, damage)] = store.player_turns[player]

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
            # Кнопка 5 урона (без КД)
            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left
                    sensitive True  # Всегда активна
                    action [
                        SetVariable("selected_damage", 5),
                        Return("attack")
                    ]

            # Кнопка 10 урона
            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left(0.3)
                    sensitive ( 
                        (store.player_turns[current_player] - 
                        store.attack_cooldowns.get((current_player, 10), -2)) >= 
                        cooldown_values[current_player].get(10, 0)
                    )
                    action [
                        SetVariable("selected_damage", 10),
                        Function(update_cooldown, current_player, 10),
                        Return("attack")
                    ]
                # Текст перезарядки только если КД > 0
                if cooldown_values[current_player].get(10, 0) > 0:
                    text "[max(0, cooldown_values[current_player][10] - (player_turns[current_player] - attack_cooldowns.get((current_player, 10), -2)))]":
                        at show_with_delay
                        style "cooldown_text"
                        xalign 0.5
                        yalign 0.5

            fixed:
                xysize (300, 100)
                imagebutton:
                    idle "button.png"
                    hover "button_hover.png"
                    xpos -400
                    at slide_from_left(0.6)
                    sensitive ( 
                        (store.player_turns[current_player] - 
                        store.attack_cooldowns.get((current_player, "heal"), -2)) >= 
                        cooldown_values[current_player].get("heal", 0)
                    )
                    action [
                        SetVariable("selected_damage", "heal"),  # Меняем тип действия
                        Function(update_cooldown, current_player, "heal"),
                        Return("attack")
                    ]
                if cooldown_values[current_player].get("heal", 0) > 0:
                    text "[max(0, cooldown_values[current_player]['heal'] - (player_turns[current_player] - attack_cooldowns.get((current_player, 'heal'), -2)))]":
                        at show_with_delay
                        style "cooldown_text"
                        xalign 0.5
                        yalign 0.5
