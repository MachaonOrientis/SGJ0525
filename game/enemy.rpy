init python:
    class Enemy:
        def __init__(self, name, hp, sprite, sprite_pos, anim=None):
            self.name = name
            self.hp = hp
            self.hpmax = hp
            self.sprite = sprite
            self.sprite_pos = sprite_pos  # Горизонтальное смещение в ряду
            self.anim = anim              # Анимация (например, покачивание)
            self.dead = False

default m1 = Enemy("Goblin", 15, "goblin.png", 0, sway)
default m2 = Enemy("Skeleton", 25, "skeleton.png", 250, sway)
default enemies_row1 = [m1,m2]

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

transform sway:
    linear 0.5 xoffset 10
    linear 0.5 xoffset -10
    repeat

transform enter_from_top(y_final):
    ypos -400  # Начальная позиция за верхним краем
    easein 1.0 ypos y_final

screen damage_popup(text):
    # Всплывающее окно с текстом
    zorder 100
    text text:
        xalign 0.5
        yalign 0.2
        color "#FFF"
        outlines [(2, "#000", 0, 0)]
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0
            pause 1.5
            linear 0.5 alpha 0.0

label test:
    $ selected_enemy = None
    $ battle_active = True
    show screen display_enemies

    while battle_active:
        call screen display_enemies
        $ selected_enemy = _return  # Получаем выбранного врага

        if selected_enemy:  # Если враг выбран
            # Пример: нанесение урона врагу
            $ selected_enemy.hp -= 10
            $ int_hp = selected_enemy.hp
            if selected_enemy.hp < 0:
                $ int_hp = 0
            else:
                $ int_hp = selected_enemy.hp
            #"[selected_enemy.name] получил 10 урона! Осталось HP: [int_hp]"

            # Проверка на смерть врага
            if selected_enemy.hp <= 0:
                $ selected_enemy.dead = True
                #"[selected_enemy.name] побеждён!"

            # Проверка условия завершения боя
            if all(enemy.dead for enemy in enemies_row1):
                $ battle_active = False
                "Все враги побеждены!"
        else:
            # Если выбор отменён (например, через кнопку "Назад")
            $ battle_active = False

    return