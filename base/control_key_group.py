class ControlKey:
    def __init__(self):
        # 为了做到按键按一次才切换的效果，在这里设计一个计数器，每次按键触发时增加1
        # 当计数器为2时说明用户完成了一次按键操作
        self.R_ALT_counter = 0
        self.R_ALT = False
        self.Escape_counter = 0
        self.Escape = True
        self.R_counter = 0
        self.R = False

    def state_change(self, key):
        # 每次键按下和弹起的时候都给计数器+1，当计数器为2时，说明完成一次操作，标记一次按键操作
        o_counter = getattr(self, key+'_counter')
        setattr(self, key+'_counter', o_counter + 1)
        self.toggle_state(key)

    def clear_counter(self, key):
        # 每次键弹起时，就将计数器清零，防止出现因为扫描原因造成计数器在按下时初值不为1的问题
        setattr(self, key, 0)

    def toggle_state(self, key):
        if getattr(self, key) == False:
            setattr(self, key, True)
        else:
            setattr(self, key, False)

    def clear_sate(self):
        # 按键信息发送到服务器后，本地的按键数据清零
        self.R_ALT = False
        self.Escape = False
        self.R = False

    def clear_state(self, key):
        setattr(self, key, False)

