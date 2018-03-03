# Chapter2 Activity


## question

1. 什么是context，context对象有哪些？

2. 有了显式Intent，为什么还要设计隐式Intent？隐式Intent在哪些场合中更适用？

3. Uri是什么？「使用隐式Intent来启动其它程序内的活动」中，通过匹配data来实现功能的原理是什么？

4. (已解决) 2.3.5返回数据给上一个活动（P51），为什么在重写onBackPressde()后，onActivityResult()中接收到的resultCode为0、Intent为null？

   - 原因1：[启动模式设置为singleTask了](http://blog.csdn.net/hp910315/article/details/51398008)

     解决方法：启动模式改为在同一个返回栈的模式

   - 原因2：[复写onBackPressed()的时候，把自己的代码放在super.onBackPressed()下面了](http://www.cnblogs.com/liyiran/p/5250823.html)

     解决方法：自己的代码放在super.onBackPressed()前面

5. 2.6.3 启动活动的最佳写法（P74），能不能将actionStart（）方法写在BaseActivity中，然后通过继承来达到通用的效果？

   - 目前想法：1.将data参数改为Bundle；2.SecondActivity.class这个自己写的活动名，通过类似于this效果的一些方法来自动获取当前活动名。

## concrete contents

### 创建活动

### 启动活动 

#### 1.使用显式Intent

#### 2.使用隐式Intent

### 在活动之间传递数据

#### 1.A2B

#### 2.B2A

### 活动的生命周期

> 3个活动状态、7个回调方法、3个生存期

#### 1.Back Stack

Android是通过任务（Task）管理活动，一个任务就是一组存储在Stack中的活动的集合，这个Stack被称为Back Stack。

##### 出栈的方法：

- 按下Back键
- 调用活动的finish()

#### 2.State

决定活动状态的两个因素：在返回栈中的位置、活动是否可见。

- 运行状态：活动处于栈顶。
- 暂停状态：活动不处于栈顶，但仍旧可见。**即一个未占满整个屏幕的活动A入栈，而活动B从栈顶下移一位。**
- 停止状态：活动不处于栈顶，并完全不可见。为这种活动保存相应的状态和成员变量
- 销毁状态：活动出栈。

#### 3.回调方法

> 除了onRestart()，其它两两对应。

- onCreate()：第一次创建活动时调用，在这个方法中完成初始化操作，比如加载布局、绑定事件等。
- onStart()：活动由不可见变为可见时调用。
- onResume()：
- onPause()
- onRestart()
- onStop()
- onDestroy()

#### 4.生存期

- 前台生存期
- 可见生存期
- 完整生存期

### 启动模式

#### 四种启动模式

#### 设置启动模式的两种方式

1. launchMode
2. intent.setFlags()

### 活动的最佳实践

#### 1.知晓当前是在哪个活动

#### 2.随时随地退出程序

#### 3.启动活动的最佳写法