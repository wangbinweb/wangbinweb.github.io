18-archlinux-install-wireless-network-card
==========
#### 20160803
## archlinux 系统安装无线网卡

为了摆脱有线的束缚，我在淘宝买了块无线网卡，型号是 Intel 8260AC PCI-E 无线网卡。在 Windows 系统中安装驾轻就熟，只要上网搜索并安装驱动即可。不过这里备注一下，因为 Intel 8260AC 比较新，我在网上搜寻时只看到支持 Win7 以上，不知道 WinXP 能否安装。

令我提心吊胆的是我的 Archlinux 系统，以前从没在Arch中单独安装过驱动，一直都是系统自动检测自动完成加载的。程序安装我目前只会用 pacman 命令，自动化安装的确很爽。而手动编译想想就让我忐忑。

进入 Archlinux 后首先使用命令 sudo wifi-menu 测试，先是跳过一条无法读取设备的文字信息，然后竟然可以搜寻 wifi 热点，选择热点后输入密码按回车，oh!系统果然发出三行错误文字信息，网络连接失败。

Archlinux 出现问题时第一时间想到的就是去查询 WIKI，按照说明，我安装了 wpa_supplicant、iw、ip 模块。这些程序可能电脑上以前就有，反正我又更新了库列表，全部安装一遍以保持最新。

接下来是不断地对照调试，很奇怪的是通过调试我发现 Archlinux 默认可以加载无线网卡，这说明网卡的驱动并没有问题，但当我加载并启用无线网卡后，使用 wpa_supplicant 来连接热点时总是不成功，提示找不到网卡或者无法读取网卡之类，而且网卡接口名称很奇怪地加上了 p2p-dev- 的前缀。

按照 [WIKI][1] 说明，知道无线热点如果无加密或使用WEP加密是不需要 wpa_supplicant 工具的，直接使用 iw 命令就可以连接网络。但如果使用WPA或WPA2 PSK加密就必须使用wpa_supplicant模块工具。

为了验证网卡驱动没有问题，我先将家里的无线密码删除，更改为完全开放状态。然后加载开启无线网卡，使用 iw 命令连接网络，再使用 dhcpcd 命令分配动态IP，结果无线网络成功连接。

这让我感到欣喜，至少说明无线网卡的驱动没有问题。问题应该出在wpa_supplicant上，百思不得其解。上网遍寻资料时偶然找到一则有用的[信息][2]，说是wpa_supplicant 1:2.5-1 版本有一个BUG，此BUG对有些网卡会得到如下错误信息： 

    Could not read interface p2p-dev-wlp3s0 flags: No such device

抱着姑且试一试的想法，我下载了[i686-patch版本][3]，下载后是一个pkg.tar.xz文件，我使用pacman -U 直接安装后，再重试wpa_supplicant连接无线热点，结果竟然连上了，众里寻它千百度，原来只是一个小小的BUG问题。这里我也将[x86_64-patch版本][4]备份一下，等到wp-supplicant升级到2.3后就不需要这些patch版本了，因为此BUG在新版本中已经被修复。

下面是一些用到的命令：

    lspci -k // 检查驱动状态
    ip link
    iw dev // 以上三种方法都能列出网卡接口名称，如果未列出，说明驱动有问题。

    dmesg | grep firmware
    dmesg | grep iwlwifi // 这两种方法是在驱动有问题时，可以用来检查和寻找问题。

    iw dev wlp3s0 link // 用来检查网卡是否连接，其中 wlp3s0 是网卡接口名称

    ip link set dev wlp3s0 up // 用来将无线网卡接口启用

    iw dev wlp3s0 scan // 用来扫描周围的无线热点

    iw dev wlp3s0 connect "your_essid" // 此命令可以直接连接没有加密的热点
    iw dev wlp3s0 connect "your_essid" key 0:your_key // 用来连接WEP加密的热点

    wpa_supplicant -D nl80211,wext -B -i wlp3s0 -c /etc/wpa_supplicant/wpa_supplicant.conf // 这是 wpa_supplicant 连接WPA/WPA2的命令格式

    dhcpcd wlp3s0 // 给无线网卡分配动态IP




[1]: https://wiki.archlinux.org/index.php/Wireless_network_configuration
(ArchLinux无线网卡设置)
[2]: https://growworkinghard.com/2016/03/23/wpa_supplicant-could-not-read-interface-p2p-dev-wlp3s0-flags/
(wpa_supplicant 1:2.5-1 bug)
[3]: http://pan.baidu.com/s/1b8T9Iu (wpa_supplicant i686-patch版本)
[4]: http://pan.baidu.com/s/1o83vCIQ (wpa_supplicant x86_64-patch版本)
