import random
import json
import os
from db import GameDataRepository

# ================== 角色定义 ==================
class Role:
    def __init__(self, name, star_rating, introduction, gender, age, decomposition_material_value, grade=1):
        self.name = name
        self.star_rating = star_rating
        self.introduction = introduction
        self.gender = gender
        self.age = age
        self.decomposition_material_value = decomposition_material_value
        self.grade = grade

# 创建所有角色实例（数据层）
roles_data = [
    # 草帽团
    Role("路飞", 5, "草帽团船长，橡胶果实能力者，梦想成为海贼王，性格单纯热血。", "男", 18, 50),
    Role("佐罗", 3, "草帽团剑士，三刀流，梦想成为世界第一大剑豪，路痴严重。", "男", 21, 30),
    Role("山治", 4, "草帽团厨师，踢技强悍，好色，文斯莫克家三子。", "男", 21, 40),
    # 和之国武士
    Role("锦卫门", 3, "和之国武士，服服果实能力者，赤鞘九侠之一，忠心耿耿。", "男", 36, 30),
    Role("小菊", 3, "和之国武士，赤鞘九侠之一，实际是男性，剑术高超。", "男", 22, 30),
    Role("御田", 5, "和之国前任将军，罗杰和白胡子的船员，豪杰中的豪杰。", "男", 39, 50),
    Role("桃之助", 3, "和之国光月家少主，人造龙果实能力者，梦想开国。", "男", 8, 30),
    # 凯多团
    Role("凯多", 5, "四皇之一，鱼鱼果实幻兽种，最强生物，和之国篇最终BOSS。", "男", 59, 50),
    Role("烬", 5, "凯多心腹，无齿翼龙果实能力者，三大灾害之首'火灾'。", "男", 47, 50),
    Role("奎因", 5, "凯多心腹，腕龙果实能力者，三大灾害'疫灾'，爱好发明。", "男", 56, 50),
    # 大妈团
    Role("佩罗斯佩罗", 3, "夏洛特家长子，舔舔果实能力者，擅长用糖果制造陷阱。", "男", 50, 30),
    # 七武海
    Role("多弗朗明哥", 5, "原王下七武海，线线果实能力者，德雷斯罗萨国王。", "男", 41, 50),
    Role("大熊", 5, "原王下七武海，肉球果实能力者，实际是革命军干部，性格温和。", "男", 47, 50),
    # 其他
    Role("艾斯", 5, "路飞义兄，烧烧果实能力者，白胡子二队长，已战死。", "男", 20, 50),
    Role("佩罗娜", 3, "恐怖三桅船干部，幽灵果实能力者，消极幽灵让人绝望。", "女", 25, 30),
    # 世界政府
    Role("CP9", 3, "世界政府直属秘密谍报机关，掌握六式，曾潜伏水之都。", "男", 30, 50),
    Role("路奇", 2, "CP9最强成员，豹果实能力者，冷酷无情的暗杀天才。", "男", 28, 20),
    Role("卡古", 3, "CP9成员，长颈鹿果实能力者，原水之都船工，擅长伪装。", "男", 25, 30),
    # 海军
    Role("塔希米", 2, "海军上校，佐罗的旧识，梦想收集所有名刀。", "女", 23, 20),
    Role("烟鬼", 1, "海军中将，烟雾果实能力者，多次追捕路飞。", "男", 36, 10),
]

# 对应权重
weights = [2, 40, 20, 30, 20, 2, 25, 2, 2, 2, 20, 2, 2, 10, 30, 40, 40, 20, 30, 40]

# ================== 游戏状态类 ==================
class GameState:
    def __init__(self):
        self.roles = roles_data
        self.weights = weights
        self.coin = 0
        # 确定存档路径（与脚本同目录下的 save.json）
        # self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.json")
        # self.load()  # 启动时读取存档
        self.repo = GameDataRepository() # 数据持久化层
        self.coin = self.repo.load_coin()  # 从数据库加载 coin
        print(f"✅ 读取存档成功，当前硬币：{self.coin}")

    # def load(self):
    #     """从 JSON 文件读取存档，若文件不存在则初始化 coin = 0"""
    #     try:
    #         with open(self.save_path, "r", encoding="utf-8") as f:
    #             data = json.load(f)
    #         self.coin = data.get("coin", 0)
    #         print(f"✅ 读取存档成功，当前硬币：{self.coin}")
    #     except FileNotFoundError:
    #         print("🆕 未找到存档，初始化为新游戏（硬币：0）")
    #         self.coin = 0

    # def save(self):
    #     """将当前状态保存到 JSON 文件"""
    #     data = {"coin": self.coin}
    #     with open(self.save_path, "w", encoding="utf-8") as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)
    def _save(self):
        """内部保存方法：将当前 coin 写入数据库"""
        self.repo.save_coin(self.coin)

    # ---------- 硬币相关 ----------
    def has_enough(self, cost):
        """检查硬币是否足够"""
        if self.coin < cost:
            print("❌ 金币不足，请充值！")
            return False
        return True

    def deduct_coin(self, cost):
        """扣减硬币（调用前需确保足够）"""
        self.coin -= cost
        self._save()  # 自动存盘

    # ---------- 抽卡 ----------
    def single_draw(self):
        if not self.has_enough(1):
            return
        self.deduct_coin(1)
        result = random.choices(self.roles, weights=self.weights, k=1)[0]
        print(f"🎴 单抽获得：{result.name} ｜ {result.introduction}")
        return result

    def ten_draw(self):
        if not self.has_enough(10):
            return
        self.deduct_coin(10)
        results = random.choices(self.roles, weights=self.weights, k=10)
        print("🎴 十连结果：")
        for idx, r in enumerate(results, 1):
            print(f"  {idx}. {r.name} ｜ {r.introduction}")
        return results

    # ---------- 充值 ----------
    def top_up(self, amount):
        """纯充值逻辑（无输入交互）"""
        self.coin += amount
        self._save()
        print(f"✅ 充值成功！获得 {amount} 硬币")
        print(f"💰 当前总硬币数：{self.coin}")

    def top_up_wrapper(self):
        """带输入交互的充值包装器（用于命令行菜单）"""
        MAX_RECHARGE = 10000
        while True:
            try:
                youpay = int(input("请输入整数充值金额（0取消）："))
                if youpay == 0:
                    print("已取消充值")
                    return
                if youpay < 0:
                    print("❌ 充值金额不能为负数！")
                    continue
                if youpay > MAX_RECHARGE:
                    print(f"❌ 单次充值不能超过 {MAX_RECHARGE} 硬币！")
                    continue
                if self.coin + youpay > 999999999:
                    print("❌ 硬币数已达上限！")
                    continue
                break
            except ValueError:
                print("❌ 请输入有效的整数！")
                continue
        self.top_up(youpay)

# ================== 主菜单 ==================
def main():
    game = GameState()
    menu = {
        1: game.single_draw,
        2: game.ten_draw,
        3: game.top_up_wrapper,
    }
    while True:
        print("\n" + "=" * 43)
        print("1. 单抽     2. 十连     3. 充值     4. 退出")
        try:
            choice = int(input("请选择："))
        except ValueError:
            print("❌ 请输入数字选项！")
            continue

        if choice == 4:
            print("👋 感谢游玩，再见！")
            break
        elif choice in menu:
            menu[choice]()
        else:
            print("❌ 无效选项，请重新选择")

if __name__ == "__main__":
    main()
#定义main是为了在调用该文件代码时不携带运行其他东西
#