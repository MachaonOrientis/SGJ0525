init python:
    import copy
    class Enemy:
        def __init__(self, name, hp, sprite, sprite_pos, attack_range, anim=None, has_enhanced_attack=False, has_heal=False):
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

            # Способности
            self.has_enhanced_attack = has_enhanced_attack
            self.has_heal = has_heal
            self.enhanced_attack_cooldown = 2
            self.heal_cooldown = 3
            self.enhanced_attack_multiplier = 2

default fight2 = False
default next_label = None


default enemies_sets = {
    "first_pack": [
        Enemy("First_Boss", 60, "first_boss.png", 300, (8,10), sway, False, False)
    ],
    "bandit_pack": [
        Enemy("Bandit", 35, "bandit.png", 250, (8,10), sway, False, False),
        Enemy("Bandit", 35, "bandit.png", 500, (9,11), sway, False, False)
    ],
    "monk_pack": [
        Enemy("Monk", 95, "monk.png", 300, (18,20), sway, False, True)
    ],
    "boss_pack": [
        Enemy("Boss", 80, "first_boss.png", 300, (13,15), sway, True, False)
    ]
}

default current_enemies_set = "boss_pack"  # набор по умолчанию

default bg_music = {
    "first_pack": "audio/music1.wav",
    "bandit_pack": "audio/music2.wav",
    "monk_pack": "audio/music3.wav",
    "boss_pack": "audio/music4.wav"
}

image bg forest = "fon7-bg.png"

screen enemy_heal(text,x_pos):
    zorder 100
    timer 1.4 action Hide("enemy_heal")
    text text:
        xalign x_pos
        yalign 0.4
        color "#00FF00"
        outlines [(2, "#000", 0, 0)]
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0
            pause 0.5
            linear 0.5 alpha 0.0

screen enhanced_attack_text(text,x_pos):
    zorder 100
    timer 1.4 action Hide("enhanced_attack_text")
    text text:
        xalign x_pos
        yalign 0.4
        color "#FF4500"
        outlines [(2, "#000", 0, 0)]


screen display_enemies():
    fixed:
        # Верхний ряд
        pos (576, 448)
        for enemy in current_enemies:
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

init:
    $ renpy.music.register_channel("bgloop", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True, movie=False, framedrop=True)

init python:
    renpy.music.register_channel(
        "sound_player", # Имя вашего канала
        mixer="sfx",  # Привязка к микшеру (по умолчанию "sfx" для звуков)
        loop=False,   # Отключаем зацикливание для звуковых эффектов
        stop_on_mute=True,
        tight=False,
        buffer_queue=True,
        movie=False
    )
    renpy.music.register_channel(
        "sound_enemy", # Имя вашего канала
        mixer="sfx",  # Привязка к микшеру (по умолчанию "sfx" для звуков)
        loop=False,   # Отключаем зацикливание для звуковых эффектов
        stop_on_mute=True,
        tight=False,
        buffer_queue=True,
        movie=False
    )
    renpy.music.register_channel(
        "bg_music", # Имя вашего канала
        mixer="music",  # Привязка к микшеру (по умолчанию "sfx" для звуков)
        loop=True,
        stop_on_mute=True,
        tight=False,
        buffer_queue=True,
        movie=False, 
        framedrop=True
    )


label test:
    scene bg forest
    stop music fadeout 1.0
    $ music_name = f"{bg_music[current_enemies_set]}"
    $ renpy.music.play(music_name, channel="bg_music", loop=True, fadein=1.0)

    $ selected_enemy = None
    $ battle_active = True
    $ players_turn = True
    $ current_player = 1

    # Применяем настройки игроков
    python:
        # Здоровье
        health1_int = player_sets[current_player_set][1]["health"]
        health2_int = player_sets[current_player_set][2]["health"]
        
        # Коэффициенты лечения
        store.heal_power = {
            1: player_sets[current_player_set][1]["heal_power"],
            2: player_sets[current_player_set][2]["heal_power"]
        }
        
        # Кулдауны
        cooldown_values.clear()
        cooldown_values.update({
            1: player_sets[current_player_set][1]["cooldowns"],
            2: player_sets[current_player_set][2]["cooldowns"]
        })

    # Создаем копию врагов из выбранного набора
    $ current_enemies = [copy.copy(e) for e in enemies_sets[renpy.store.current_enemies_set]]

    python:
        for enemy in current_enemies:
            enemy.dead = False
            enemy.hp = enemy.hpmax

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
                    if current_player == 1:
                        $ health1_int = min(100, health1_int + heal_power[1])
                        $ renpy.show_screen("heal_player", f"+{heal_power[1]}",0.4)
                        $ renpy.play("audio/heal.wav", channel="sound_player")
                    else:
                        $ health2_int = min(100, health2_int + heal_power[2])
                        $ renpy.show_screen("heal_player", f"+{heal_power[2]}",0.6)
                        $ renpy.play("audio/heal.wav", channel="sound_player")
                    # Сбрасываем выбранное действие
                    $ selected_damage = 0
                    $ renpy.pause(1,hard=True)
                else:
                    # Атака
                    call screen display_enemies
                    $ selected_enemy = _return

                # Обновление счётчика ходов и передача очереди
                $ player_turns[current_player] += 1
                if current_player == 2:
                    $ players_turn = False
                    $ current_player = 1
                else:
                    $ current_player = 2

                if selected_enemy:  # Если враг выбран
                    # Преобразуем урон в число
                    $ damage = int(selected_damage)
                    $ selected_enemy.hp -= selected_damage
                    $ selected_enemy.hp = max(0, selected_enemy.hp)
                    $ selected_enemy.damage_text = f"-{selected_damage}"
                    $ renpy.play("audio/attack.wav", channel="sound_player")
                    $ renpy.play("audio/damage.wav", channel="sound_enemy")
                    $ selected_enemy.damage_time = renpy.get_game_runtime()

                    $ selected_enemy.damage_text = f"-{selected_damage}"
                    $ selected_enemy.damage_time = renpy.get_game_runtime()

                    # Проверка смерти врага
                    if selected_enemy.hp <= 0:
                        $ selected_enemy.dead = True
                        $ selected_enemy.damage_text = "ПОБЕЖДЁН"

        else:
            show screen display_enemies
            $ renpy.pause(1.5,hard=True)
            # Ход врагов
            python:
                x_pos = 0.3
                for enemy in current_enemies:
                    if not enemy.dead:
                        enemy.enhanced_attack_cooldown = max(0, enemy.enhanced_attack_cooldown - 1)
                        enemy.heal_cooldown = max(0, enemy.heal_cooldown - 1)
                        

                        action_performed = False

                        # Лечение
                        if enemy.has_heal and enemy.heal_cooldown <= 0:
                            enemy.hp = min(enemy.hpmax, enemy.hp + 15)
                            enemy.heal_cooldown = 3
                            renpy.show_screen("enemy_heal", "+15", x_pos)
                            renpy.play("audio/heal.wav", channel="sound_enemy")
                            action_performed = True
                            enemy.anim = move_anim(0,-100)
                            renpy.pause(2, hard=True)

                            # Усиленная атака
                        enhanced_damage = None
                        if enemy.has_enhanced_attack and enemy.enhanced_attack_cooldown <= 0 and not action_performed:
                            enhanced_damage = int(renpy.random.randint(*enemy.attack_range) * enemy.enhanced_attack_multiplier)
                            enemy.enhanced_attack_cooldown = 2
                            renpy.show_screen("enhanced_attack_text", "УСИЛЕННАЯ АТАКА!",x_pos)
                            target = renpy.random.choice([1, 2])
                            if target == 1:
                                store.health1_int = max(0, store.health1_int - enhanced_damage)
                                renpy.show_screen("damage_player1", f"-{enhanced_damage}")
                                renpy.play("audio/damage.wav", channel="sound_player")
                                renpy.play("audio/attack.wav", channel="sound_enemy")
                            else:
                                store.health2_int = max(0, store.health2_int - enhanced_damage)
                                renpy.show_screen("damage_player2", f"-{enhanced_damage}")
                                renpy.play("audio/damage.wav", channel="sound_player")
                                renpy.play("audio/attack.wav", channel="sound_enemy")
                            action_performed = True
                            enemy.anim = move_anim(0,150)
                            renpy.pause(2, hard=True)

                        # Логика атаки
                        if not action_performed:
                            enemy.anim = move_anim(0,100)
                            damage = renpy.random.randint(*enemy.attack_range)
                            target = renpy.random.choice([1, 2])
                            
                            if target == 1:
                                store.health1_int = max(0, store.health1_int - damage)
                                renpy.show_screen("damage_player1", f"-{damage}")
                                renpy.play("audio/attack.wav", channel="sound_enemy")
                                renpy.play("audio/damage.wav", channel="sound_player")
                            else:
                                store.health2_int = max(0, store.health2_int - damage)
                                renpy.show_screen("damage_player2", f"-{damage}")
                                renpy.play("audio/attack.wav", channel="sound_enemy")
                                renpy.play("audio/damage.wav", channel="sound_player")
                                
                            renpy.pause(2, hard=True)
                        
                        x_pos += 0.13
                        enemy.anim = sway
                        action_performed = True
                    else:
                        renpy.pause(0.2, hard=True)
                renpy.store.global_turn += 1
            
            # Проверка смерти игроков
            if health1_int <= 0 or health2_int <= 0:
                jump battle_lost
                
            $ players_turn = True   
        
        # Проверка победы
        if all(enemy.dead for enemy in current_enemies):
            jump battle_won
                
    return

label battle_lost:
    stop music fadeout 1.0
    "Ваша команда пала в бою!"
    $ fight2 = False
    hide screen health1
    hide screen health2
    hide screen display_enemies
    hide screen player1
    hide screen player2
    hide screen display_enemies
    $ renpy.music.stop(channel="bg_music", fadeout=1.0)
    $ renpy.jump(next_label)
    return

label battle_won:
    stop music fadeout 1.0
    "Все враги повержены!"
    $ fight2 = True
    hide screen health1
    hide screen health2
    hide screen display_enemies
    hide screen player1
    hide screen player2
    hide screen display_enemies
    $ renpy.music.stop(channel="bg_music", fadeout=1.0)
    $ renpy.jump(next_label)
    return