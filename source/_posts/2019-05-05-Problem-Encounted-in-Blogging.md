---
title: Problem Encounted in Blogging
date: 2019-05-05 15:35:25
tags: ["study"]
categories: study
description: 今天是第一次写自己的 Blog ，使用Github + Hexo 期间遇到两个问题记录。 Quick Start : Reference1.初次搭建Blog：GitHub + Hexo2.github官方教程-changeing a remote’s url3.git 官方教程4.yilia 主题 问题1：以前的remote repository与现有的仓库提交上有冲突
---
# Problem Encounted in Blogging

Problem Encounted in Blogging
[2019-05-05](/2019/05/05/Problem-Encounted-in-Blogging/)
2019-05-05

今天是第一次写自己的 Blog ，使用Github + Hexo 期间遇到两个问题记录。

今天是第一次写自己的
[Blog](https://Noeverer.github.io/)
Blog
，使用Github + Hexo 期间遇到两个问题记录。

## Quick Start : Reference

Quick Start : Reference

1.初次搭建Blog：GitHub + Hexo2.github官方教程-changeing a remote’s url3.git 官方教程4.yilia 主题

1.
[初次搭建Blog：GitHub + Hexo](https://www.cnblogs.com/liuxianan/p/build-blog-website-by-hexo-github.html#%E4%B8%8A%E4%BC%A0%E5%88%B0github)
初次搭建Blog：GitHub + Hexo
2.
[github官方教程-changeing a remote’s url](https://help.github.com/en/articles/changing-a-remotes-url)
github官方教程-changeing a remote’s url
3.
[git 官方教程](https://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5)
git 官方教程
4.
[yilia 主题](https://github.com/litten/hexo-theme-yilia)
yilia 主题

### 问题1：以前的remote repository与现有的仓库提交上有冲突

问题1：以前的remote repository与现有的仓库提交上有冲突

1.产生：在本地加载好主题，可以实现在hexo s 开启本地预览，打开浏览器访问 http://localhost:4000 是正常的。

1.产生：在本地加载好主题，可以实现在
`hexo s`
hexo s
开启本地预览，打开浏览器访问
[http://localhost:4000](http://localhost:4000)
http://localhost:4000
是正常的。

2.现象：准备使用 hexo deploy 将本地仓库推送到github上面出现如下报错：123456nothing to coommit,working tree cleanEnter passpharse for key '/c/Users/RobotLiu/.ssh/id_rsa':ERROR:Repository not foundfatal:Could not read from remote repository.please make sure you have the correct access rights and the repository exists.

2.现象：准备使用
`hexo deploy`
hexo deploy
将本地仓库推送到github上面出现如下报错：
![](/img/error_remote_repo.png)

```123456```

1
2
3
4
5
6

```nothing to coommit,working tree cleanEnter passpharse for key '/c/Users/RobotLiu/.ssh/id_rsa':ERROR:Repository not foundfatal:Could not read from remote repository.please make sure you have the correct access rights and the repository exists.```

nothing to coommit,working tree clean
Enter passpharse for key '/c/Users/RobotLiu/.ssh/id_rsa':
ERROR:Repository not found
fatal:Could not read from remote repository.
please make sure you have the correct access rights and the repository exists.

3.查找原因：

3.查找原因：
- 远程仓库出错，怀疑和之前我使用Git提交仓库时，进行全局设置提交到git@github.com:robotliu327/test_website.git这个仓库，但是我在F:\Git\hexo_config.yml设置时deploy>>repository: git@github.com:robotliu327/robotliu327.github.io.git 是这个仓库，所以二者起了冲突

使用git命令查看当前配置下我提交到仓库的urlconfig 配置有system级别 global（用户级别） 和local（当前仓库）三个参考:git config命令git config --local  --list`remote.origin.url=git@github.com:robotliu327/test_website.git`
- 改变git local 下面的远程提交的到仓库的url

参考：Changing a remote’s URl

先删除本地的origin的url— git remote rm origin 可以使用git config --local  --list查看git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]

远程仓库出错，怀疑和之前我使用Git提交仓库时，进行全局设置提交到git@github.com:robotliu327/test_website.git这个仓库，但是我在F:\Git\hexo_config.yml设置时deploy>>repository: git@github.com:robotliu327/robotliu327.github.io.git 是这个仓库，所以二者起了冲突

远程仓库出错，怀疑和之前我使用Git提交仓库时，进行全局设置提交到
[git@github.com](mailto:git@github.com)
git@github.com
:robotliu327/test_website.git这个仓库，但是我在F:\Git\hexo_config.yml设置时deploy>>repository:
[git@github.com](mailto:git@github.com)
git@github.com
:robotliu327/robotliu327.github.io.git 是这个仓库，所以二者起了冲突
> 使用git命令查看当前配置下我提交到仓库的urlconfig 配置有system级别 global（用户级别） 和local（当前仓库）三个参考:git config命令git config --local  --list`remote.origin.url=git@github.com:robotliu327/test_website.git`

使用git命令查看当前配置下我提交到仓库的urlconfig 配置有system级别 global（用户级别） 和local（当前仓库）三个参考:git config命令git config --local  --list`remote.origin.url=git@github.com:robotliu327/test_website.git`

使用git命令查看当前配置下我提交到仓库的url
config 配置有system级别 global（用户级别） 和local（当前仓库）三个
[参考:git config命令](https://www.cnblogs.com/merray/p/6006411.html)
参考:git config命令
`git config --local  --list`
git config --local  --list
[`remote.origin.url=git@github.com](mailto:`remote.origin.url=git@github.com)
`remote.origin.url=git@github.com
:robotliu327/test_website.git`

改变git local 下面的远程提交的到仓库的url

改变git local 下面的远程提交的到仓库的url
> 参考：Changing a remote’s URl

先删除本地的origin的url— git remote rm origin 可以使用git config --local  --list查看git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]

参考：Changing a remote’s URl

[参考：Changing a remote’s URl](https://help.github.com/en/articles/changing-a-remotes-url)
参考：Changing a remote’s URl
> 先删除本地的origin的url— git remote rm origin 可以使用git config --local  --list查看git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]

先删除本地的origin的url— git remote rm origin 可以使用git config --local  --list查看git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]

先删除本地的origin的url—
`git remote rm origin`
git remote rm origin
可以使用
`git config --local  --list`
git config --local  --list
查看
`git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]`
git remote set-url [old remote name: "origin" means old remote repository url] [A new URL for the remote url]

4.相关经验：

4.相关经验：

### 问题2：Github上面SSH Key加密传输协议

问题2：Github上面SSH Key加密传输协议

总结：所以一般一台主机链接一个github账户只需要生成一个ssh key即可，代表这台电脑被github接受，但是github上面可以生产多个SSh key 意味着一个github账户可以接受多台主机的认证，这样你可以使用不同的电脑上使用加密传输众所周知ssh key是加密传输。加密传输的算法有好多，git使用rsa，rsa要解决的一个核心问题是，如何使用一对特定的数字，使其中一个数字可以用来加密，而另外一个数字可以用来解密。这两个数字就是你在使用git和github的时候所遇到的public key也就是公钥以及private key私钥。其中，公钥就是那个用来加密的数字，这也就是为什么你在本机生成了公钥之后，要上传到github的原因。从github发回来的，用那公钥加密过的数据，可以用你本地的私钥来还原。如果你的key丢失了，不管是公钥还是私钥，丢失一个都不能用了，解决方法也很简单，重新再生成一次，然后在http://github.com里再设置一次就行

**总结：所以一般一台主机链接一个github账户只需要生成一个ssh key即可，代表这台电脑被github接受，但是github上面可以生产多个SSh key 意味着一个github账户可以接受多台主机的认证，这样你可以使用不同的电脑上使用加密传输**
总结：所以一般一台主机链接一个github账户只需要生成一个ssh key即可，代表这台电脑被github接受，但是github上面可以生产多个SSh key 意味着一个github账户可以接受多台主机的认证，这样你可以使用不同的电脑上使用加密传输
众所周知ssh key是加密传输。加密传输的算法有好多，git使用rsa，rsa要解决的一个核心问题是，如何使用一对特定的数字，使其中一个数字可以用来加密，而另外一个数字可以用来解密。这两个数字就是你在使用git和github的时候所遇到的public key也就是公钥以及private key私钥。
其中，公钥就是那个用来加密的数字，这也就是为什么你在本机生成了公钥之后，要上传到github的原因。从github发回来的，用那公钥加密过的数据，可以用你本地的私钥来还原。
如果你的key丢失了，不管是公钥还是私钥，丢失一个都不能用了，解决方法也很简单，重新再生成一次，然后在
[http://github.com里再设置一次就行](http://github.com里再设置一次就行)
http://github.com里再设置一次就行
[赏
            

谢谢你来看我

支付宝

微信](javascript:;)
赏

谢谢你来看我

谢谢你来看我
![](/img/alipay.png)
支付宝
![](/img/wechat.png)
微信
- study
[study](javascript:void(0))
study