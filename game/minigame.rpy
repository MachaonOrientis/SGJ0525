
define player1_cr = Character(name="Персонаж 1",color="#7CFC00")
define player2_cr = Character(name="Персонаж 2",color="#1900fc")

default health1_int = 36
default health2_int = 23

transform slide_from_bottom(start_y=1.1, end_y=0.9, delay=0.0):
    ycenter start_y  # Начальная позиция
    pause delay
    easeout 0.5 ycenter end_y  # Плавное движение к конечной позиции
    on hide:  # Анимация при скрытии
        easeout 0.5 ycenter start_y

transform slide_from_top(start_y=1.1, end_y=0.9, delay=0.0):
    pass

screen health1():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "health_img.png":
            at slide_from_bottom(1.1,0.9,0.3)
            zoom 0.2
            xcenter 0.4  
            ycenter 0.9

        # Текст
        text "Здоровье: [health1_int]":
            at slide_from_bottom(1.1,0.95,0.6)
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
            at slide_from_bottom(1.1,0.9,0.3)
            zoom 0.2
            xcenter 0.6  
            ycenter 0.9

        # Текст
        text "Здоровье: [health2_int]":
            at slide_from_bottom(1.1,0.95,0.6)
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
            at slide_from_bottom(1.1,0.75)
            zoom 0.3
            xcenter 0.6  
            ycenter 0.75

screen player2():
    fixed:
        xalign 1
        yalign 1 


        # Изображение
        add "player1.jpg":
            at slide_from_bottom(1.1,0.75)
            zoom 0.3
            xcenter 0.4  
            ycenter 0.75

init python:
    def play_button_sound():
        renpy.play("audio/button_spawn.mp3")  # Путь к звуку

transform slide_from_left(delay=0.0): 
    xysize(300,100)
    pause delay
    xpos -400  # Начальная позиция за левым краем экрана
    easeout 0.5 xpos 20  # Плавное движение к конечной позиции
    on hide:  # Анимация при скрытии
        easeout 0.5 xpos -500

screen bottom_left_buttons:
    # Основной контейнер для позиционирования
    fixed:
        xalign 0.0    # Прижимаем к левому краю
        yalign 1.0    # Прижимаем к нижнему краю
        xoffset 40  # Отступы от края
        yoffset -200
        xysize (300,250)

        # Вертикальный контейнер для кнопок (снизу вверх)
        vbox:
            spacing 1  # Расстояние между кнопками
            imagebutton:
                
                idle "button.png"
                hover "button_hover.png"
                xpos -400
                at slide_from_left
                action Return("button1")
            
            imagebutton:
                idle "button.png"
                hover "button_hover.png"
                xpos -400
                at slide_from_left(0.3)
                action Return("button2")
            
            imagebutton:
                idle "button.png"
                hover "button_hover.png"
                xpos -400
                at slide_from_left(0.6)
                action Return("button3")

label game:

    "Это новая сцена из другого файла."
    player1_cr "Некая фраза"

    window hide

    show screen health1
    show screen health2
    show screen player1
    show screen player2
    $ renpy.notify("123")
    show screen bottom_left_buttons

    pause

    return