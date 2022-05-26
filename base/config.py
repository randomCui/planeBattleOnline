# 游戏屏幕宽高
window_width = 600
window_height = 750

# 游戏帧率
frame_rate = 60

# 服务器的初始化数据
ip = 'localhost'
port = 11451

# 游戏操控的灵敏度
sensitivity = 2

# 保存游戏各项设置的字典
setting = {
    'easy': {
        'enemy_spawn_time': 2,
        'enemy_health': {
            'enemy_1': 3,
            'enemy_2': 5,
        },
        'total_enemy': 60,

        'boss_spawn_time': 100,

        'boss_health': {
            'boss_1': 60,
        },
        'prop_spawn_time': 5,
    },
    'hard': {
        'enemy_spawn_time': 1.3,
        'enemy_health': {
            'enemy_1': 6,
            'enemy_2': 10,
        },
        'total_enemy': 80,

        'boss_spawn_time': 120,
        'boss_health': {
            'boss_1': 120,
        },
        'prop_spawn_time': 10,
    }
}
