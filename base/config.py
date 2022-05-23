import os

window_width = 600
window_height = 750

frame_rate = 60

ip = 'localhost'
port = 11452

sensitivity = 2

setting = {
    'easy': {
        'enemy_spawn_time': 2,
        'enemy_health': {
            'enemy_1': 3,
            'enemy_2': 5,
        },

        'boss_spawn_time': 100,
        'boss_health': {
            'boss_1': 60,
        },
        'prop_spawn_time': 5,
    }
}

client_specific = {

}

music_path = {
    'BGM': os.path.join("..", "audio", "BGM1.wav"),
    'death': os.path.join("..", "audio", "explosion.wav"),
    'get_prop': os.path.join("..", "audio", "getToolKit.wav"),
    'player_shoot': os.path.join("..", "audio", "heroShoot.wav"),
}
