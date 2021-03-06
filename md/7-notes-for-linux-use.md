#### 20150304
## Linux 系统使用手记

> 2015年3月4日

今天在telegram中听说有一个叫cutegram的软件不错，所以晚上回家就在ubuntu中安装了一下，结果发现虽然一切都好，但唯独不能切换输入法，从而无法输入中文。最后只能卸载了事。

不过，在此过程中，安装了一个叫Gdebi的安装包，以后安装Deb包只要一句命令sudo gdebi package.deb 即可。

> 2015年3月6日

当我在使用VIM的时候，其实有一个困惑，就是一行字中遇到空格时，如果这一行字数很多，那么 vim 会在空格处自动换行并新起一行，并将空格后的文字放到下一行。这样问题就来了，有时候不管是写代码还是写文章，都会有一些英文或者字母，而我喜欢在这些英文字母两边都空一格，可这样做的结果是一行字写下来，vim 会自动换成几行字，让人烦恼。

网上查了下，发现是 vimrc 中的设置问题。

在我的 vimrc 中有一个选项叫做 set textwidth=80，问题就出在这一句上。当文字宽度达到80个字符时，VIM 会在遇到空格时自动换新行。

哈，就是这么回事，所以只要改一下，set textwidth=0，这样就等于关闭了这个选项，问题解决。

> 2015年3月8日 
> 天气：雨

继续使用 Vim ，又发现一个问题，就是无法将一个文件中的复制内容粘贴到另一个文件中，只能在同一个 Vim 中操作，这有时候是个大问题。

最后才查到，原来是因为我系统中没有安装 GVIM 程序的缘故，只有安装了 GVIM ，才能使用系统剪切板，唉，知道原因后解决是很简单的事。

我先安装了 vim-gnome ，可惜这个版本跟我用的 ubuntu 14.04 居然有冲突，每次打开 gvim 时都会冒出三行警告信息，虽然不影响操作，但看着不爽。

然后就安装了 Vim-gtk 版本，结果一切顺利，系统剪切板也可用了。

> 2015年3月12日淩晨 
> 晴朗

最近在 linux 上安装了cutegram，这是 telegram 在 linux 系统中的一个客户端，界面相对比较漂亮，但一直有一个问题困扰我，那就是只能输入英文，在输入框中无法切换输入法。而且在交流中知道碰到这种现象的有很多人。所以大家一直都以为是 cutegram 的程序问题。

另一个网络中挺热的 IM 程序，叫 tox ，点对点传输，号称是世界上最安全地聊天工具之一，今天在 IRC 的 #linuxba 频道中不停地宣传，我忍不住就试用了一下。

但噩梦从此开始。先是 qtox 更新源被墙，装到一半就断了。于是又学习设置系统全局代理，捣鼓了半天原来在网络设置中有专门的界面可以设置。然后继续更新源，下了半天，主要是代理慢吧，终于安装成功了，但竟然也遇到了与 cutegram 同样的问题，只能输入英文，中文输入法无法切换。这真是一个蛋疼的结果。

正在我灰心丧气的时候，IRC 中的 quininer 提醒我系统需要安装 fcitx-frontend-qt4 与 fcitx-frontend-qt5。这是我原先不知道的，所以赶紧上网查找资料，安装与设置步骤如下：
        
        sudo add-apt-repository ppa:fcitx-team/nightly
        sudo apt-get update
        sudo apt-get dist-upgrade

其实这样就已经安装好了 fcitx-frontend-qt4 和 fcitx-frontend-qt5，如果没有安装，可以执行：

        sudo apt-get install fcitx-frontend-qt4 
        sudo apt-get install fcitx-frontend-qt5 
        
最后很关键的一步是把 libfcitxplatforminputcontextplugin.so 复制到相关软件中去。libfcitxplatforminputcontextplugin.so 这个文件一般在 qt5 的插件文件夹内。比如我的 ubuntu 32位系统就在: /usr/lib/i386-linux-gnu/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so。

Cutegram：把上面的这个文件复制到 /opt/cutegram/qtplugins/platforminputcontexts/ 内。注意这个路径可能会因系统不同而不一样，但你可以使用 dkpg -L cutegram 来查找 cutegram 的安装文件夹在哪里。

如果还是不行，可以试试增加如下操作：在终端中打开编辑文件 sudo vim /etc/profile，然后在文件的最后添加：

        export XIM_PROGRAM=fcitx
        export XIM=fcitx
        export GTK_IM_MODULE=fcitx
        export QT_IM_MODULE=fcitx
        export XMODIFIERS="@im=fcitx"

然后注销系统，重新登录一下应该就可以了。

而 qtox 我发现不用任何多余设置就可以切换中文输入了。
