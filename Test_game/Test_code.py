from Scene.Scene_player1 import Scene_player1


# 加载第一关地形
def test1():
    accomplish = True
    for i in range(35):
        scene_player1 = Scene_player1(i)
        if not scene_player1.event_loop():
            accomplish = False
            break
    if accomplish:
        print("闯关成功")
    else:
        print("闯关失败")


if __name__ == '__main__':
    test1()
