# MyZelda

这是一个使用Python和Pygame构建的2D俯视视角冒险游戏，灵感来源于塞尔达传说系列。该项目展示了多个系统协同工作的完整游戏开发实现。

**小组成员** :  20232489张凯博
                20232488叶谌超
## 游戏特性

- **探索**: 在包含草地、水域和障碍物的俯视视角世界中自由探索
- **战斗系统**: 使用武器和魔法与各种敌人战斗，具有不同的攻击类型
- **角色成长**: 通过获得经验值来升级角色属性，通过技能菜单提升能力
- **多种武器**: 可以切换使用不同武器（剑、长矛、斧头、刺剑、双刃），每种武器具有独特的冷却时间和伤害值
- **魔法系统**: 施放治疗和火焰攻击等法术，消耗法力值
- **多样敌人**: 面对不同怪物（乌贼、浣熊、幽灵、竹子），具有独特的行为、属性和攻击模式
- **互动环境**: 可以砍草产生粒子效果，与物体互动
- **UI系统**: 生命值/能量条、武器/魔法选择、经验值显示和升级菜单
- **升级菜单**: 按'M'键访问角色升级界面，提升生命、能量、攻击、魔法和速度属性
- **死亡重生**: 死亡后按'R'键重新开始，恢复满血状态

## 核心系统

### 玩家系统
[Player](file://D:\20232489张凯博\MyZelda\code\Player.py#L0-L275) 类处理所有玩家相关功能：
- 使用方向键通过 [input](file://D:\20232489张凯博\MyZelda\code\Player.py#L88-L148) 方法进行移动
- 通过 [animate](file://D:\20232489张凯博\MyZelda\code\Enemy.py#L99-L115) 方法进行动画处理，包含方向性精灵图
- 通过 [create_attack](file://D:\20232489张凯博\MyZelda\code\Level.py#L99-L100) 和 [create_magic](file://D:\20232489张凯博\MyZelda\code\Level.py#L101-L106) 方法实现攻击系统
- 管理生命值、能量和经验值等状态
- 通过继承自 [Entity](file://D:\20232489张凯博\MyZelda\code\entity.py#L3-L44) 类的 [move](file://D:\20232489张凯博\MyZelda\code\entity.py#L10-L18) 和 [collision](file://D:\20232489张凯博\MyZelda\code\entity.py#L21-L36) 方法实现碰撞检测

### 战斗系统
- 使用 [Weapon](file://D:\20232489张凯博\MyZelda\code\Weapon.py#L0-L20) 类创建方向性武器精灵实现武器攻击
- 通过 [MagicPlayer](file://D:\20232489张凯博\MyZelda\code\magic.py#L4-L43) 类实现治疗和火焰法术的魔法系统
- 使用 [Enemy](file://D:\20232489张凯博\MyZelda\code\Enemy.py#L0-L159) 类实现敌人战斗，包含攻击行为
- 在 [get_full_weapon_damage](file://D:\20232489张凯博\MyZelda\code\Player.py#L245-L248) 和 [get_full_magic_damage](file://D:\20232489张凯博\MyZelda\code\Player.py#L250-L253) 方法中计算伤害值

### 敌人AI
[Enemy](file://D:\20232489张凯博\MyZelda\code\Enemy.py#L0-L159) 类实现了：
- 通过 [get_player_distance_direction](file://D:\20232489张凯博\MyZelda\code\Enemy.py#L65-L75) 方法追踪距离
- 通过 [get_status](file://D:\20232489张凯博\MyZelda\code\Enemy.py#L77-L87) 方法管理状态（空闲、移动、攻击）
- 在 [monster_data](file://D:\20232489张凯博\MyZelda\code\Setting.py#L39-L43) 中定义具有独特属性的不同怪物类型
- 攻击行为和冷却机制
- 死亡粒子效果和经验值奖励

### 关卡和地图系统
- 从CSV文件加载基于瓦片的地图（[map_FloorBlocks.csv](file://D:\20232489张凯博\MyZelda\Map\map_FloorBlocks.csv), [map_Grass.csv](file://D:\20232489张凯博\MyZelda\Map\map_Grass.csv), [map_Objects.csv](file://D:\20232489张凯博\MyZelda\Map\map_Objects.csv), [map_Entities.csv](file://D:\20232489张凯博\MyZelda\Map\map_Entities.csv)）
- 使用 [Tile](file://D:\20232489张凯博\MyZelda\code\Tile.py#L0-L13) 类创建边界瓦片用于碰撞检测
- 随机变化的对象和草地图块放置
- 包含玩家起始位置和敌人生成点的实体放置

### 视觉效果
- 通过 [AnimationPlayer](file://D:\20232489张凯博\MyZelda\code\particles.py#L4-L57) 类实现粒子系统
- 草地图块切割效果，产生叶片粒子
- 攻击和魔法效果动画
- 敌人死亡动画

### UI系统
[UI](file://D:\20232489张凯博\MyZelda\code\ui.py#L3-L81) 类管理：
- 生命值和能量条显示
- 武器和魔法选择框
- 经验值计数器
- 使用 [Upgrade](file://D:\20232489张凯博\MyZelda\code\upgrade.py#L3-L75) 类实现角色升级系统以改进属性

### 相机系统
- 在 [CameraGroup](file://D:\20232489张凯博\MyZelda\code\Level.py#L184-L215) 类中实现自定义相机
- 相机跟随玩家，带有偏移计算
- 基于Y位置的正确精灵渲染顺序

## 控制方式

- **移动**: 方向键（上、下、左、右）
- **攻击**: 空格键（根据当前方向创建武器）
- **魔法**: 左控制键（CTRL）（施放当前魔法咒语）
- **切换武器**: Q键（在可用武器间循环）
- **切换魔法**: E键（在可用法术间循环）
- **暂停/升级菜单**: M键（打开属性升级菜单）
- **重生**: R键（死亡时，恢复满血状态）

## 安装说明

1. 安装Python 3.7或更高版本
2. 安装Pygame: `pip install pygame`
3. 克隆或下载此代码库
4. 运行游戏: `python code/main.py`

## 项目结构

```
MyZelda/
├── code/                  # 游戏源代码
│   ├── main.py           # 入口点，初始化游戏循环
│   ├── Level.py          # 关卡管理和精灵组
│   ├── Player.py         # 玩家角色实现
│   ├── Enemy.py          # 敌人AI和行为
│   ├── Weapon.py         # 武器可视化
│   ├── Tile.py           # 地图瓦片和障碍物
│   ├── ui.py             # 用户界面元素
│   ├── upgrade.py        # 角色升级系统
│   ├── magic.py          # 魔法咒语实现
│   ├── particles.py      # 粒子效果系统
│   ├── death_screen.py   # 死亡屏幕显示
│   ├── Setting.py        # 游戏常量和配置
│   ├── Support.py        # 实用函数
│   ├── entity.py         # 基础实体类
│   └── debug.py          # 调试工具
├── Graphics/             # 游戏资源（精灵图、UI元素）
├── audio/                # 音效和音乐
├── Map/                  # 关卡数据（CSV文件和瓦片地图）
│   ├── map_FloorBlocks.csv  # 边界/碰撞地图
│   ├── map_Grass.csv        # 草地放置地图
│   ├── map_Objects.csv      # 对象放置地图
│   ├── map_Entities.csv     # 实体放置地图
│   └── ground.png           # 基础地面纹理
└── README.md             # 说明文件
```


## 技术细节

- 使用Python和Pygame构建
- 使用基于精灵图的图形系统，通过 [import_folder](file://D:\20232489张凯博\MyZelda\code\Support.py#L16-L25) 函数实现动画系统
- 为玩家和敌人实现碰撞检测，使用 `inflate` 方法处理碰撞箱
- 在 [CameraGroup](file://D:\20232489张凯博\MyZelda\code\Level.py#L184-L215) 类中实现跟随玩家的自定义相机系统
- 使用CSV文件进行关卡布局的数据驱动方法，通过 [import_csv_layout](file://D:\20232489张凯博\MyZelda\code\Support.py#L6-L12) 函数加载
- 为游戏实体提供独立类的模块化设计
- 使用 [Entity](file://D:\20232489张凯博\MyZelda\code\entity.py#L3-L44) 基础类实现共享功能的实体组件系统
- 使用精灵组进行高效的渲染和碰撞检测
- 为玩家和敌人动画实现状态管理

## 游戏数据配置

游戏参数在 [Setting.py](file://D:\20232489张凯博\MyZelda\code\Setting.py) 中配置：
- 屏幕尺寸和游戏设置
- 包含冷却时间和伤害值的武器数据
- 具有强度和消耗值的魔法咒语数据
- 敌人属性和行为
- UI元素尺寸和颜色
- 不同实体类型的碰撞箱偏移量

## 版权信息

此项目是作为游戏开发课程的一部分创建的。所有资源和代码均为教育目的而开发。