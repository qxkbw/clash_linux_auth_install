# clash_linux_auth_install
clash linux自动安装
# 支持系统
+ 已测试`centos7`和`centos8`
# 支持Python版本
+ 已测试`Python2.7.5`和`Python3.6.8`
+ 理论上3.x版本都支持
# 下载
+ 1：`git clone git@github.com:qxkbw/clash_linux_auth_install.git`
+ 2: 在github.com上直接下载zip包，并且解压后使用
+ 3: 单独下载`start.py`文件也可以使用
# 启动脚本
+ `python starrt.py` 或 `python3 start.py`
# 配置
+ 1：输入`Clash下载地址` 或 `本机绝对路径` 或 输入`1`，1代表下载默认的地址
    - 提示：本机绝对路径 意思是自己下载了Clash文件，未解压文件，这样不用等待下载
+ 2：Clash配置文件，输入`http订阅地址` 或 `本机上的配置文件的绝对路径`
    - 以上2个选项完成，会在脚本目录里创建一个`clash_linux_auto_install_config.conf`的配置文件
+ 3：配置选项
    - 1: 默认配置。默认创建`Clash systemctl服务`, 默认启动clash服务用户: `root`，默认开启`git代理`
    - 2：关闭创建Clash Systemctl服务
    - 3：关闭修改Git代理配置
    - 4: 修改启动systemctl Clash服务用户，默认root
    - 5: 完成配置，开始程序！
    - d: 清空配置文件，重新配置
# 配置选项完成！等待脚本完成
+ 当提示：`git代理配置成功！` 和 `所有配置完成，退出！`表示完成【下载，安装，配置】，感谢使用！
