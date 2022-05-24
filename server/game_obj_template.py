# 此文件主要保存游戏中需要使用到的各种对象的配置文件

bullet_template = {
    'hostile_bullet': {
        'basic_setting': {
            'x': 0,
            'y': 0,
            # size字段需要自己填写
            'size': None,
            'texture_name': 'YELLOW_SPACE_SHIP'
        },
        'inertia_setting': {
            'max_speed': 5,
        },
        'bullet_setting': {
            'damage': 4,
        }
    }
}

player_template = {
    'player_1': {
        'basic_setting': {
            'x': 0,
            'y': 0,
            # size字段需要自己填写
            'size': None,
            'texture_name': 'YELLOW_SPACE_SHIP'
        },
        'inertia_setting': {
            'max_speed': 8,
        },
        'plane_setting': {

        },
    }
}
