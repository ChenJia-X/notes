# Chapter10 Service、Thread

## Questions

## Concepts

- Message：可以携带少量信息，在线程之间传递数据。
- Handler：接收、处理Message。
- MessageQueue：存放所有通过Handler发送的Message。每个线程只有一个MessageQueue。
- Looper：调用loop()进入无限循环中，每当发现MessageQueue中存在Message，就会取出message，并传递给Handler进行处理。每个线程也只有一个Looper。

## Notifications

1. -359- 每个服务只会存在一个实例。

## Concrete contents

### 一、Thread

UI操作不能在子线程中进行，Android提供了两种解决方式：

1. 异步消息处理机制
   - 实现过程：
     - 首先在主线程中创建一个`handler`对象，并重写`handleMessage()`。
     - 每当需要在子线程中进行UI操作时，就在子线程中创建一个`Message`对象，并通过handler发送出去。
     - 之后这个message会被添加到`MessageQueue`的队列中等待处理。
     - 而`Looper`检测到MessageQueue中存在Message后，会将这个Message取出，并分发给handler。
     - 最后handler会调用handleMessage()进行处理。
2. AsyncTask
   - 实现过程：
     - ①创建一个类（例如DownloadTask）继承AsyncTask。
     - ②重写AsyncTask的几个重要方法。
       - onPreExecute()：会在后台任务开始执行前调用，用于进行一些界面初始化操作。
       - doInBackground(Params...)：该方法在子线程中运行，用于处理各种耗时操作。
         - 若是要进行UI操作，需要在该方法中调用publishProgress(Progress...)。
       - onProgressUpdate(Progress...)：在后台任务调用publishProgress(Progress...)后，该方法很快会被调用。该方法的参数就是后台任务传递过来的。在这个方法中可以对UI进行操作。
       - onPostExecute(Result)：后台任务执行完毕后并通过return语句返回时，这个方法就会被调用。返回的数据作为参数传递到此方法中，可以利用返回的数据进行一些UI操作。
     - ③启动这个任务
       - new DownloadTask().execute();


### 二、Service

服务适合执行那些不需要和用户交互，而且还要求长期执行的任务。

服务并不是运行在一个独立的进程中，而是依赖于创建服务时所在的应用程序进程。

服务不会自动开启线程，所有的代码默认运行在主线程。

#### （一）定义服务

1. 创建一个继承自`service`的类，并override `onBind()`。
2. override `onCreate()` 、`onStartCommand()`、 `onDestroy()`。
3. 在AndroidManifest文件中注册。

> onCreate() 只在服务第一次启动的时候调用，而 onStartCommand() 会在每一次服务启动时被调用。

#### （二）启动和停止服务

```java
Intent startIntent=new Intent(this,MyService.class);
startService(startIntent);//stopService(startIntent)
```

`startService()` 和 `stopService()` 都是定义在Context类中，所以我们可以在活动中直接调用这两个方法。

如果想要在service中停止服务，则需要调用 `stopSelf()`。

#### （三）活动和服务进行通信

1. 创建`ServiceConnection`匿名类，并 override  `onServiceDisconnected()` 、`onServiceDisconnected()`。

   ```java
   private ServiceConnection connection=new ServiceConnection(){
     @override
     public void onServiceConnected(ComponentName name, IBinder service){
       //do something
     }
     public void onServiceDisconnected(ComponentName name){
       //do something
     }
   }
   ```

2. 绑定服务

   ```java
   Intent bindIntent=new Intent(this,MyService.class);
   bindService(bindIntent, connection, BIND_AUTO_CREATE);//会调用MyService的onBinder方法，并在connection的onServiceConnected()返回一个IBinder对象。
   ```

3. 解除绑定

   ```java
   unbindService(connection);
   ```

> 任何一个服务在整个应用程序范围内都是通用的，也就是说，MyService 可以和任何一个 Activity 绑定，并且绑定后获取到同一个 IBinder 实例。-P358-

#### （四）服务的活动周期

onCreate() -> onStartCommand() ->运行状态 -> onDestroy() //startService() 、stopService()/stopSelf()

运行状态 -> onBinder() -> 通信状态 -> onDestroy() //bindService() 、unbindService()

> 每个服务只会存在一个实例。 
>
> 当既调用了startService() 又调用了 bindService() ，则需要同时调用 stopService() 和 unbindService()。