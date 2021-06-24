# coding=utf-8
# start
import os
import sys
import threading
from time import sleep
if sys.version_info.major == 3:
    input = input
else:
    input = eval('raw_input')
os.system("systemctl stop systemd-resolved")
os.system("systemctl disable systemd-resolved")#这里会导致53端口占用，所以直接默认关闭
# 配置 -------------
# clash下载地址 # 可指定clash包文件 绝对路径，我发现下载太慢了，所以添加自己下载clash包，指定文件名路径
clash_download = "https://github.com/Dreamacro/clash/releases/download/v1.3.0/clash-linux-amd64-v1.3.0.gz"
systemctl_status = True #True:创建，False：不创建。是否创建systemctl配置文件，并且从systemctl启动clash
systemctl_user = "root" #启动systemctl的指定用户
git_status = True #是否修改git的代理 True:修改，False:不修改
#创建systemctl服务内容
systemctl_conent = """
[Unit]
Description=A rule based proxy in Go for %i.
After=network.target

[Service]
Type=simple
User=%i
Restart=on-abort
ExecStart=/usr/bin/clash

[Install]
WantedBy=multi-user.target
"""
Confi_Yaml = "" #clash代理配置文件，不用修改
clash_download_status = False
try:
    
    with open("clash_linux_auto_install_config.conf", "r") as data:
        def delete():
            print("你的脚本配置文件有错误，我们已经删除，请重新执行")
            os.remove(os.path.join(os.getcwd(), "clash_linux_auto_install_config.conf"))
            sys.exit(0)
        clash_download_select=data.readline()[:-1]
        if not clash_download_select:
            delete()
        Confi_Yaml=data.readline()[:-1]
        if not Confi_Yaml:
            delete()
        clash_download_status=data.readline()[:-1]
        
except Exception:

    print("默认下载地址："+clash_download)
    print("------------------------------")
    print("提示：没有代理这里下载有点慢，推荐先自己下载，在下面指定文件目录")
    print("------------------------------------------------------------")
    clash_download_select = input("输入clash下载地址或者自己下载clash文件的路径, 默认输入1：")



    print("""
    1: CLash服务区提供商 提供的http订阅地址\n
    2：提供本系统目录上的一个文件：config.yaml（名字必须是这个, 绝对路径）
    """)
    while True:
        select = input("输入你的选择: ")
        if select == '1' or select == '2':
            
            hint = {select:"输入url地址："}.get(1,"输入config.yaml文件路径：")
            url = input(hint)
            if url:
                Confi_Yaml = url
                break
            else:
                print("输入为空，在次输入！")
            
        else:
            print("输入不正确，退出程序")
            sys.exit(0)

    with open("clash_linux_auto_install_config.conf", "w+") as data:
        data.write(clash_download_select+"\n"+Confi_Yaml+"\n")

while True:
    #选择配置
    print("""
1: 默认配置。默认创建Clash systemctl服务, 默认启动clash服务用户: root，默认修改git代理
2：关闭创建Clash Systemctl服务
3：关闭修改Git代理配置
4: 修改启动systemctl Clash服务用户，默认root
5: 完成配置，开始程序！
d: 清空配置文件，重新配置
""")
    select = input("请输入选项: ")
    if select == "1":
        break
    elif select == '2':
        systemctl_status = not systemctl_status
        print({systemctl_status:"开启systemctl配置"}.get(True, "关闭systemctl配置"))
    elif select == '3': 
        git_status = not git_status
        print({git_status:"开启git代理配置"}.get(True, "关闭git代理配置"))
    elif select == '4':
        user = input("输入启动服务用户：")
        if not user:
            print("输入空")
        else:
            systemctl_user = user
    elif select == "d":
        os.remove(os.path.join(os.getcwd(), "clash_linux_auto_install_config.conf"))
        print("请重新执行脚本")
        sys.exit(1)
    else:
        break    

if clash_download_select[:4] == "http" or clash_download_select == "1":
    if not clash_download_status:
        #下载文件
        status = os.system("wget "+clash_download)
        if status != 0:
            print("下载失败")
            sys.exit(0)
        
        with open("clash_linux_auto_install_config.conf", "a") as data:
            data.write("clahs=1\n")

else:#路径
    clash_download = clash_download_select
    if not os.path.isfile(os.path.join(os.getcwd(), clash_download.split("/")[-1])):
        if os.system("mv "+clash_download+" "+os.getcwd()) != 0:
            print("移动clash文件失败，请检查提示信息")
            sys.exit(0)

file_name = clash_download.split("/")[-1]#或者文件名
clash_path = os.path.join(os.getcwd(),file_name)
# os.system("cp "+clash_download+" /back_"+file_name))
status = os.system("gunzip -c "+clash_path + " > clash")
if status != 0:
    with open("clash_linux_auto_install_config.conf", "w+") as data:#删除已下载文件的状态
        content = data.read()
        content = content.replace("clash=1\n","")
        data.write(content)
    print("解压失败")
    sys.exit(0)

os.system("chmod +x clash")#添加执行权限
os.system("mv clash /usr/bin/clash")#更改名称
os.system("mkdir ~/.config")#创建配置目录
os.system("mkdir ~/.config/clash")#创建配置目录

#有这个文件就不下载了，没有才下
if not os.path.isfile(os.path.join(os.path.expanduser("~"), ".config/clash/Country.mmdb")):
    if os.system("wget -c 'https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb' -O ~/.config/clash/Country.mmdb") != 0:
        print("下载Country.mmdb文件失败！可以手动下载到~/.config/clash目录里\n链接: https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb")
        sys.exit(0)

print("开始配置config.yaml文件")#config.yaml
if os.path.exists(Confi_Yaml):#绝对路径
    if os.system("cp "+Confi_Yaml+ "~/.config/clash/") != 0:
        print("复制config.yaml文件失败，请确认路径正确？请根据提示信息重新运行！")
        sys.exit(0)

else:#url
    if not os.path.isfile(os.path.join(os.path.expanduser("~"),".config/clash/config.yaml")):#判断是否有这个文件
        if os.system("wget -c '"+Confi_Yaml+"' -O ~/.config/clash/config.yaml") != 0:
            print("下载config.yaml文件失败，你可以尝试手动下载，并移动到~/.config/clash/ 目录下")
            sys.exit(0)


#systemctl
if not systemctl_status:
    sys.exit(1)
# os.system("touch /lib/systemd/system/clash\@"+systemctl_user+".service")
# print("echo "+systemctl_conent+" > /lib/systemd/system/clash@"+systemctl_user+".service")
os.system("echo '"+systemctl_conent+"' > /lib/systemd/system/clash@"+systemctl_user+".service")
os.system("systemctl daemon-reload")
if os.system("systemctl start clash@"+systemctl_user) != 0:
    print("从systemctl启动clash失败")

if os.system("systemctl enable clash@"+systemctl_user)!=0:
    print("启动clash服务失败")
    sys.exit(0)

print("启动clash服务成功啦...提示：如果你的Country.mmdb不完整，会自动下载，等待下载完毕后自动启动服务端口")
sleep(1)
size = 0
count = 0
load_count = 0
while True:
    f = os.popen("netstat -ntl")
    if f.read().find("7890") != -1:
        print("Country.mmdb文件下载完成！")
        print("clash端口服务已经正常运行了！")
        break
    else:
        now_size = os.path.getsize(os.path.join(os.path.expanduser("~"), ".config/clash/Country.mmdb"))
        if now_size > size:
            size = now_size
            count = 0#重置0
            print("正在下载...,检测次数："+ str(load_count)+"次")
            sleep(5)
            load_count += 1
            
        else:
            if count == 4:
                print("发现Country.mmdb文件没有下载，并且clash服务也启动")
                print("1：请你查看网络")
                print("2：请查看脚本运行状态") 
                print("解决办法：请重新运行脚本")
                os.system("systemctl stop clash@"+systemctl_user)
                sys.exit(0)
            count += 1
            print("第"+count+"次等待")
if not git_status:
    sys.exit(1)
os.system("mkdir ~/.ssh")
if os.system("git config --global https.proxy http://127.0.0.1:7890") != 0:
    print("设置git代理失败，错误步骤1")
    sys.exit(0)
if os.system("git config --global https.proxy https://127.0.0.1:7890") != 0:
    print("设置git代理失败，错误步骤2")
    sys.exit(0)
if os.system("echo 'ProxyCommand connect -S 127.0.0.1:7890 %h %p' > ~/.ssh/config") != 0:
    print("设置git代理失败，错误步骤3")
    sys.exit(0)
print("git代理配置成功！")
print("所有配置完成，退出！")