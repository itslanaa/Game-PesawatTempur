from ursina import *
import random

batas_kiri = -15
batas_kanan = 15
batas_bawah = -10
batas_atas = 8

def update():
    global musuhnya, peluruh, skor
    if not game_started:
        return
    
    # Batasi gerakan pesawat dalam layar
    if pswt.x > batas_kanan:
        pswt.x = batas_kanan
    elif pswt.x < batas_kiri:
        pswt.x = batas_kiri
    
    if pswt.y > batas_atas:
        pswt.y = batas_atas
    elif pswt.y < batas_bawah:
        pswt.y = batas_bawah

    for musuh in musuhnya:
        musuh.x -= 0.1
        if musuh.x < -30:
            musuhnya.remove(musuh)
            destroy(musuh)
            create_musuh()

    for peluru in peluruh[:]:
        if not peluru:  
            peluruh.remove(peluru)
            continue
        peluru.x += 0.2
        for musuh in musuhnya[:]:
            if abs(musuh.x - peluru.x) < 1.5 and abs(musuh.y - peluru.y) < 1.5:
                musuhnya.remove(musuh)
                destroy(musuh)
                peluruh.remove(peluru)
                destroy(peluru)
                create_musuh()
                skor += 1  # Update skor ketika musuh terbunuh
                skor_text.text = f'Skor: {skor}'  # Tampilkan skor di layar
                break

    # Update posisi pesawat dengan kontrol
    pswt.y += held_keys['w'] * 6 * time.dt
    pswt.y -= held_keys['s'] * 6 * time.dt
    pswt.x += held_keys['d'] * 6 * time.dt
    pswt.x -= held_keys['a'] * 6 * time.dt

    # Update rotasi pesawat
    a = held_keys['w'] * -20
    b = held_keys['s'] * 20
    if a != 0:
        pswt.rotation_z = a
    else:
        pswt.rotation_z = b

    # Cek tabrakan antara pesawat dan musuh
    for musuh in musuhnya:
        if pswt.intersects(musuh).hit:
            game_over()

def input(key):
    if not game_started:
        return

    if key == 'space':
        peluru = Entity(
            y=pswt.y,
            x=pswt.x + 2,
            model='cube',
            texture='assets/peluru',
            collider='box'
        )
        peluruh.append(peluru)
        Audio('assets/suara-tembakan.mp3') 
        invoke(destroy, peluru, delay=2)

def start_game():
    global game_started, skor
    game_started = True

    # Hilangkan elemen-elemen menu
    bgmenu.enabled = False  
    title.enabled = False
    start_button.enabled = False

    if menu_music:
        menu_music.stop()

    # Inisialisasi elemen-elemen game
    global pswt, musuhnya, peluruh, skor, skor_text

    bg = Entity(
        model='quad',
        texture='assets/Background.png',
        scale=36,
        z=1
    )

    pswt = Animation(
        'assets/pesawat',
        collider='box',
        scale=6,
        y=5
    )

    Sky()
    camera.orthographic = True
    camera.fov = 20

    musuhnya = []
    peluruh = []
    skor = 0  # Inisialisasi skor awal

    # Tambahkan teks skor di layar
    skor_text = Text('Skor: 0', scale=2, y=0.4, x=-0.8, origin=(0,0))

    for _ in range(10):
        create_musuh()

def create_musuh():
    musuh = Entity(
        model='sphere',  # sphere cube
        texture='test_tileset',  #test_tileset
        collider='box',
        scale=2,
        x=random.randint(10, 30),
        y=random.randint(-15, 5)
    )
    musuhnya.append(musuh)

def game_over():
    global game_started
    game_started = False

    # Hapus semua musuh dan peluru
    for musuh in musuhnya:
        destroy(musuh)
    musuhnya.clear()

    for peluru in peluruh:
        destroy(peluru)
    peluruh.clear()

    # Tampilkan pesan game over
    game_over_text.enabled = True
    restart_button.enabled = True

def restart_game():
    global game_started
    game_started = False

    # Hapus pesawat lama jika ada
    if 'pswt' in globals():
        destroy(pswt)

    # Hapus semua musuh dan peluru
    for musuh in musuhnya:
        destroy(musuh)
    musuhnya.clear()

    for peluru in peluruh:
        destroy(peluru)
    peluruh.clear()

    # Hapus teks skor
    destroy(skor_text)

    # Sembunyikan pesan game over dan tombol restart
    game_over_text.enabled = False
    restart_button.enabled = False

    # Mulai permainan baru
    start_game()

app = Ursina()

# Inisialisasi status game
game_started = False

# Membuat background untuk elemen menu
bgmenu= Entity(
    model='quad',
    texture='assets/bgmenu1.png',
    scale=(15, 9),
)
title = Text('Game Pesawat Tempur', scale=4.1, y=0.2, color=color.black, origin=(0,0), alpha=0.8)  
start_button = Button('Start Game', scale=(0.25, 0.1), y=-0.1, color=color.azure, on_click=start_game)  # Menambah lebar tombol

# Membuat elemen game over
game_over_text = Text('Game Over', scale=2, y=0, origin=(0,0), enabled=False)
restart_button = Button('Restart', scale=(0.25, 0.1), y=-0.1, color=color.red, on_click=restart_game, enabled=False)

menu_music = Audio('the-war-184745.mp3', autoplay=True, loop=True)

app.run()
