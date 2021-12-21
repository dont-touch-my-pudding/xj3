import win32gui
import win32process
import win32api
import ctypes  # C C++语言调用

window_handle = win32gui.FindWindow(None, "PAL3--SOFTSTAR.sh")
process_id = win32process.GetWindowThreadProcessId(window_handle)[1]
# print(process_id)
process_handle = win32api.OpenProcess(0x1F0FFF, False, process_id)
# print(process_handle)  # <PyHANDLE:788>
kernel32 = ctypes.windll.LoadLibrary("C://Windows/System32/kernel32.dll")
data1 = ctypes.c_long()
li = ["人物", "物品"]
names = ["景天", "雪见", "龙葵", "长卿", "紫萱"]


class People:
    # 人物相关类
    def __init__(self, name):
        self.conf = {
            "景天": {
                "经验": 0x00C04684,
                "属性": {
                    "蓝条上限": 0x00C04624,
                    "血量上限": 0x00C0461C,
                    "气条上限": 0x00C04620,
                    "武值": 0x00C04628,
                    "防值": 0X00C0462C,
                    "速值": 0x00C04630,
                    "运值": 0x00C04634,
                    "风属性": 0x00C04640,
                    "火属性": 0x00C0463C,
                    "土属性": 0x00C04648,
                    "水属性": 0x00C04638,
                    "雷属性": 0x00C04644
                },
                "状态": {
                    "蓝条": 0x00C04774,
                    "血条": 0x00C0476C,
                    "气条": 0x00C04770,
                },
                "技能": {
                    "风咒": 0x00C048D0,
                    "炎咒": 0x00C048C0
                }
            },
            "雪见": {
                "经验": 0x00C04C04,
                "属性": {
                    "血量上限": 0x00C04B9C,
                    "气条上限": 0x00C04BA0,
                    "神量上限": 0x00C04BA4,
                    "武值": 0x00C04CC8,
                    "防值": 0x00C04CCC,
                    "速值": 0x00C04CD0,
                    "运值": 0x00C04CD4,
                    "水属性": 0x00C04BBB,
                    "风属性": 0x00C04BC0,
                    "雷属性": 0x00C04BC4,
                    "火属性": 0x00C04BBC,
                    "土属性": 0x00C04BC8
                },
                "状态": {
                    "血量": 0x00C04CEC,
                    "气量": 0x00C04CF0,
                    "神量": 0x00C04CF4
                },
                "技能": {
                    "土咒": 0x00C04E58
                }
            },
            "长卿": {
                "经验": 0x00C04684,
                "属性": {},
                "状态": {},
            },
            "紫萱": {
                "经验": 0x00C05704,
                "属性": {},
                "状态": {}
            },
            "龙葵": {
                "经验": 0x00C05184,
                "属性": {},
                "状态": {}
            }
        }
        self.name = name
        self.choose = self.conf[self.name]
        self.data1 = ctypes.c_long()

    def lv(self):
        functype = "经验"
        local = self.choose[functype]
        while True:
            kernel32.ReadProcessMemory(int(process_handle), local, ctypes.byref(self.data1), 4, None)
            print(f"{self.name}当前{functype}为:", self.data1.value)
            txyl_num = input("输入经验数量,输入的不是数字返回到选则界面")
            if not txyl_num.isdigit():
                print("输入的不是数字,返回到主界面")
                return
            txyl_num = ctypes.c_long(int(txyl_num))
            kernel32.WriteProcessMemory(int(process_handle), local, ctypes.byref(txyl_num), 4, None)
            print(f"{self.name}的{functype}已修改为:", self.data1.value)

    def attribute(self):
        functype = "属性"
        item = self.choose[functype]
        if not item:
            print(f"抱歉!暂时不支持修改{self.name}的{functype}")
            return
        self.motion(item, functype)

    def state(self):
        functype = "状态"
        item = self.choose[functype]
        if not item:
            print(f"抱歉!暂时不支持修改{self.name}的{functype}")
            return
        self.motion(item, functype)

    def skill(self):
        functype = "技能"
        item = self.choose[functype]
        if not item:
            print(f"抱歉!暂时不支持修改{self.name}的{functype}")
            return
        self.motion(item, functype)

    def motion(self, item, functype):
        while True:
            print(item.keys())
            name = input(f"输入要修改得到{functype}:")
            if name not in item.keys():  # 输入人物不在人物列表的时候
                print("属性不存在")
                return
            hex_value = item[name]
            kernel32.ReadProcessMemory(int(process_handle), hex_value, ctypes.byref(self.data1), 4, None)
            print(f"{self.name}当前{name}{functype}", self.data1.value)
            txyl_num = ctypes.c_long(int(input("输入数量")))
            kernel32.WriteProcessMemory(int(process_handle), hex_value, ctypes.byref(txyl_num), 4, None)
            print(f"{self.name}修改后的{name}{functype}", txyl_num)


class Article:
    # 物品相关类
    def __init__(self):
        self.item = {
            "金币": 0x00C05F54
        }
        self.data1 = ctypes.c_long()

    def add_(self):
        print(self.item.keys())
        at_name = input("输入要刷的东西名称")
        local = self.item[at_name]
        self.motion(local, at_name)

    def motion(self, local, at_name):
        while True:
            kernel32.ReadProcessMemory(int(process_handle), local, ctypes.byref(self.data1), 4, None)
            print(f"{at_name}当前数量", self.data1.value)
            number = input("输入数量")
            if not number.isdigit():
                return
            txyl_num = ctypes.c_long(int(number))
            kernel32.WriteProcessMemory(int(process_handle), local, ctypes.byref(txyl_num), 4, None)
            print(f"{at_name}修改后的数量", txyl_num)


print(li)
uindex = int(input("输入人物id"))
if uindex == 0:
    print(names)
    uname = int(input("输入人物id"))
    people = People(names[uname])
    cs = {
        "人物等级": people.lv,
        "人物属性": people.attribute,
        "人物状态": people.state,
        "人物技能": people.skill
    }
    while True:
        print(cs.keys())
        name = input("输入要刷的东西:")
        var = cs[name]
        var()
else:
    article = Article()
    article.add_()
