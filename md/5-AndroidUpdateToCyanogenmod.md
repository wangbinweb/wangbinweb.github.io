#### 20140510
## 安卓 android 系统升级到 cyanogenmod ( CM ) 最新版本

最近对CyanogenMod很感兴趣，把自己的手机(Samsung N7000 三星NOTE 1)升级到了CM最新版，安卓4.4.2系统，希望本文对喜欢CM的用家有所帮助。

==========

介绍：

[CyanogenMod][1]是一个基于Android系统深度优化、定制、开发的第三方手机操作系统。CM提供了一些原生Android系统或某些手机厂商定制系统中没有的功能，也是第一个使用BFS作任务管理器的手机操作系统。

升级步骤：

1. 备份系统资料

这一步其实很简单，因为一般来讲，需要备份的数据很少。推荐使用[钛备份][2]，主要备份一些没有同步到云端的数据，如短信，私人日记等，其他大部分应用不需要备份，系统安装后可以再重新下载安装。

2. 把以下程序下载到手机内存卡里

CyanogenMod 系统程序。程序下载地址在[这里][3]，请按自己的手机品牌型号选择最新版本，版本有nightly、milestone、snapshot、rc、stable，依次越来越稳定，最近据CM博客消息说以后可能每两周只更新M版本，不再放stable版本了。

Gapps 谷歌内核服务框架。程序下载地址在[这里][4]，请按自己安装的CM版本下载对应的Gapps版本，否则将刷机失败。

适合安卓版本的 Recovery 版本。程序下载地址在[这里][5]，请按自己的手机品牌型号点击进入相应链接，尽量选择日期较近的版本，否则将刷机失败。这个文件要在手机内存卡里和电脑里各放一份。

3. 下载以下程序

为安全起见，还需要下载一个兼容性好的第三方Recovery，这个请自行搜索寻找，网上有很多，根据自己的手机品牌型号找一个能成功刷入的Recovery即可。

Odin 线刷软件。程序下载地址在[这里][6]。不一定会用到，但为了安全起见，先下载好线刷软件 Odin 并预先安装到电脑里备用。

4. 现在准备工作已完成，开始刷机。

+ 第一步：手机关机，开机进入线刷模式 
+ 第二步：用数据线连接电脑，使用Odin软件刷入“适合安卓版本的Recovery版本”，如果这一步成功，则跳过第三步和第四步直接进入第五步 
+ 第三步：如果第二步不成功，不要慌，那就用Odin软件先刷入“兼容性好的第三方Recovery”，这个第三方Recovery的特点是肯定能刷入自己的手机，所以准备工作要做好。 
+ 第四步：重新开机进入Recovery卡刷模式，使用 install update from zip file 菜单进入选择“适合安卓版本的Recovery版本”刷入手机。 
+ 第五步：重新开机，进入新安装的Recovery版本卡刷模式，先安装CM程序文件，再安装Gapps谷歌内核服务框架，最后别忘了双清操作，即 Wipe Data / Wipe Cache .
+ 第六步：重新开机，这时你应该已经看到了CM的开机画面了。刷机成功。

[1]:http://www.cyanogenmod.org/ (cyanogenmod)
[2]:http://www.wandoujia.com/apps/com.keramidas.TitaniumBackup (钛备份)
[3]:http://download.cyanogenmod.org/ (download cyanogenmod)
[4]:http://www.teamandroid.com/gapps/ (Google Gapps)
[5]:http://goo.im/devs/philz_touch/CWM_Advanced_Edition (PhilZ Touch Recovery)
[6]:http://odin.website (Download Odin)
