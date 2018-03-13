# Working with System Permissions

## 为什么需要权限？

每款 Android 应用都在访问受限的沙盒中运行。如果应用需要使用其沙盒外的资源或信息，则必须请求相应*权限*。



## 授予应用权限的方式

根据权限的敏感性，系统可能会自动授予权限（不需要请求权限），或者需要由设备用户对请求进行许可。Android6.0以上，除了需要在安装时授予权限，还需要在运行时授予权限。



## 开发者确定应用需要哪些权限？

开发应用时，您应注意应用何时使用需要权限的功能。通常，在使用并非由自身创建的信息资源、执行会影响设备或其他应用行为的操作时，应用都需要获得相应的权限。

如果应用请求另一应用执行任务或提供信息，则不需要获得相应权限。（[使用Intent](https://developer.android.com/training/permissions/best-practices.html#perms-vs-intents)）



## 如何申请权限？

### 1.Declaring Permissions

### 2.Requseting Permissions at Run time



## 参考资料：

1. [权限最佳做法](https://developer.android.com/training/permissions/best-practices.html#perms-vs-intents)
2. [Patterns–Permissions](https://material.io/guidelines/patterns/permissions.html#)
3. [APP Permissions](https://developer.android.com/guide/topics/permissions/index.html)
4. [系统权限](https://developer.android.com/guide/topics/security/permissions.html#normal-dangerous)

