# 飞机大战
**作者**:randomCui

**更新日期**:2020/05/16

**状态**:ongoing

**目前可用版本**: v1.0

> 只完成了局域网联机的最基本功能
> 
> 游戏的正经逻辑还没有全部完成
____________________

## 目前已经完成的功能
### 服务端
- 开启一个socket并监听连接请求
- 与连接的客户端进行通信 
- 接受客户端的初始化请求并返回一个玩家对象 
- 接受玩家提出的状态更新通信，并更新游戏对象 
- 返回每次更新之后的游戏对象到客户端 
- 分离游戏更新与网络请求的依赖性
- 分离监听端口线程和服务端主线程
- 接收客户端在自身移动之外的其他状态消息 (例如发射子弹, 使用技能等)

### 游戏逻辑
- 类内自带定时器，保证事件按时触发
- 随机生成敌机
- 敌机类移动，发射子弹
- 两种子弹 (直线飞行子弹, 可瞄准子弹) 的移动和伤害逻辑
- 敌方子弹和己方英雄的碰撞检测 (使用mask使得碰撞更加精确)
- 对于游戏物体出界后的处理
- 逻辑清晰的继承关系
- 抽象成库的贴图对象 (好处是不用每次使用都要初始化)
- 敌方飞机和己方子弹的碰撞检测
- 英雄飞机单发子弹
- 斜向飞行子弹贴图和碰撞箱相应进行旋转
- > |模块类型|
  > |------|
  > |激光近防模块|
- 血条

### 客户端
- 将网络连接抽象成类
- 发送初始化消息到服务器
- 在键鼠操作中 ***非常精美*** 的惯性和阻尼效果
- 接受服务器返回的game对象数据
- 逻辑清晰的渲染管线
- 将不含贴图的游戏对象经过init_texture后渲染出来
- 主菜单+配置飞船菜单
- 向服务器发送不同消息请求的格式
- 暂停选单

____________________________________
## 计划添加的功能
### 服务器
- 处理游戏暂停时的逻辑 (例如暂停游戏更新线程的运行)
- 更好的处理stop信息

### 游戏逻辑
- 各种动画效果 (背景动画, 子弹动画, 爆炸动画等)
- 英雄飞机发射子弹效果 (不同的发射模式，比如散射...)
- 道具的随机生成 移动 捡拾 生效
- 不同英雄飞机的技能
>|英雄类型|技能类型|
> |------|------|
> |坦克|护盾增幅|
> |射手|以降低速度的代价齐射导弹
> |支援|给己方的飞船加血
- 飞机装备的不同模块及其效果
> |~~闪现模块 (带有动画)~~|
- 护盾

### 客户端
- 背景音乐的播放
