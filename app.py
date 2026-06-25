from flask import Flask,jsonify,render_template
from draw_card_game4 import GameState
import json
#把 Flask 这个"工具箱"拿进来
app = Flask(__name__)
# 创建一个 Flask 应用实例（就像你写 game = GameState()
game=GameState()
@app.route('/api/single_draw')
# 告诉 Flask：如果有人访问根路径 /，就执行下面的函数
def single_draw():
    result=game.single_draw()
    if result is None:
        return jsonify({"status": "error", "message": "金币不足，抽卡失败"})
    return jsonify({
        "status": "success",
        "data": {
            "name": result.name,
            "star_rating": result.star_rating,
            "introduction": result.introduction
        }
    })
@app.route('/api/top_up/<int:amount>')
def top_up(amount):
    game.top_up(amount)
    return jsonify({"status": "success", "message": f"充值成功，当前金币{game.coin}"})
@app.route('/api/coin')
def coin():
    return jsonify({"coin": game.coin})
@app.route('/api/ten_draw')
def ten_draw():
    results=game.ten_draw()
    if results is None:
        return jsonify({"status": "error", "message": "金币不足，抽卡失败"})
    data = [{"name": r.name, "star_rating": r.star_rating, "introduction": r.introduction} for r in results]
    return jsonify({"status": "success", "data": data})

#启动服务器，debug=True 表示代码改完自动重启
#json格式，所有抽出来的角色转换为json格式，那转换了之后呢，为什么要转换为json格式，有什么好处
#还有就是你说我这里str拼接不好，但是我是展示在浏览器呀，json格式展示好看吗？应该是有了前端页面搭配json数据更好展示
#单抽，十连，充值，其他功能（金币的存储读取、还有输入逻辑）
#

@app.route('/')
def game_page():
    return render_template('index.html')

#为什么要放在上面这个接口后面
#app.run()作用：启动了一个 Web 服务器，它会一直运行并监听请求，直到你按 Ctrl+C 终止。在它运行期间，程序不会继续执行后面的代码。
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False)

