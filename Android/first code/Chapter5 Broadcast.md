# Chapter 5 Broadcast

## Notification

1. 广播接收器中==不允许开启线程==
2. 动态注册的广播接收器一定要取消注册。
3. 本地广播接收器不能静态注册。

## Model

1. 广播机制有BroadcastReceiver、Broadcast两部分。
2. BroadcastReceiver、Broadcast根据作用范围分为全局（系统）以及local。

## Concrete content

#### 5.1 Broadcast机制简介

##### Broadcast的组成

- `广播接收器（Broadcast Receiver）`
  - 动态注册：在程序运行时注册广播接收器，比较灵活。
  - 静态注册：可以在程序没有启动时接收广播。
- 发送广播
  - `标准广播（Normal broadcast）`：完全异步执行，所有广播接收器同时接收到。
  - `有序广播（Ordered broadcast）`：同步执行，广播接收器有优先级，同时高优先级的广播可以截断正在传递的广播。


##### Broadcast的一些特性

- 广播是跨进程的通信方式。
- 广播接收器中是==不允许开启线程==的，当onReceive()运行较长时间而没有结束，程序就会报错，所以不要在onReceive()中添加过多复杂逻辑。

#### 5.2 接收系统Broadcast

##### 5.2.1 动态注册Broadcast Receiver

1. 新建一个继承`BroadcastReceiver`的类，并重写`onReceive()`。

   ```java
   public class NetworkChangeReceiver extends BroadcastReceiver {
       @Override
       public void onReceive(Context context, Intent intent) {
           Toast.makeText(context,"hello",Toast.LENGTH_SHORT).show();
       }
   }
   ```

2. 创建参数为广播action的`IntentFilter`实例和1中继承BroadcastReceiver的类的实例，并将两者作为参数传入`registerReceiver()`。**注意：动态注册的广播接收器一定要取消注册。**

   ```java
   public class MainActivity extends AppCompatActivity {
       private NetworkChangeReceiver networkChangeReceiver;
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_main);
           IntentFilter intentFilter =new IntentFilter("android.net.conn.CONNECTIVITY_CHANGE");
           networkChangeReceiver =new NetworkChangeReceiver();
           registerReceiver(networkChangeReceiver,intentFilter);
       }

       @Override
       protected void onDestroy() {
           super.onDestroy();
           unregisterReceiver(networkChangeReceiver);//动态注册的广播接收器一定要取消注册
       }
   }
   ```


##### 5.2.2 静态注册广播接收器

1. 新建一个继承`BroadcastReceiver`的类，并重写`onReceive()`。


2. 在AndroidManifest.xml中注册。用AS的话会自动注册。


```xml
<application
……
    <activity android:name=".MainActivity">
       ……
    </activity>

    <receiver
        android:name=".BootCompleteReceiver"
        android:enabled="true"
        android:exported="true"/><!--exported属性表示是否允许这个广播接收器接收除本程序以外的广播-->
</application>
```

#### 5.3发送广播

##### 5.3.1  发送标准广播

```java
Intent intent = new Intent("android.net.conn.CONNECTIVITY_CHANGE");
sendBroadcast(intent);
```

##### 5.3.2 发送有序广播

```java
Intent intent = new Intent("android.net.conn.CONNECTIVITY_CHANGE");
sendOrderedBroadcast(intent,null);//第二个参数是一个与权限有关的字符串，这里传入null就行了
```

接收有序广播的广播接收器的优先级设置

```xml
<receiver
    android:name=".BootCompleteReceiver"
    android:enabled="true"
    android:exported="true">
    <intent-filter android:priority="100">
        <action android:name="android.net.conn.CONNECTIVITY_CHANGE"/>
    </intent-filter>
</receiver>
```

#### 5.4 使用本地广播

本地广播发送的广播只能在应用程序内部传播，并且本地广播接收器只能接收来自本应用程序发出的广播。所以本地广播接收器不能静态注册。

1. 为什么要使用本地广播？

- 防止发送的广播被其它程序获取，造成信息泄露。
- 防止接收其它程序发送的广播，造成安全漏洞的隐患。
- 使用本地广播比全局广播更高效。

2. 如何使用本地广播？

使用`LocalBroadcastManager`来对广播进行管理。



#### 5.5 广播的最佳实践——实现强制下线的功能