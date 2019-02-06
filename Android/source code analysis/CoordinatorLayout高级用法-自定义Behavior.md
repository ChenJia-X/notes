# [CoordinatorLayout高级用法-自定义Behavior](https://blog.csdn.net/qibin0506/article/details/50290421)

## Question

- 我一直不明白 是什么把两个ScrollView联系起来的, 只在一个ScrollView加了 behavior,为什么 他会关联到 第一个ScrollView 而不是关联其他的View。
  - 作者：见下一篇[《源码看CoordinatorLayout.Behavior原理》](https://blog.csdn.net/qibin0506/article/details/50377592)



## Content

版权声明：本文来自Loader's Blog，未经博主允许不得转载。 https://blog.csdn.net/qibin0506/article/details/50290421

在新的support design中，CoordinatorLayout可以说是最重要的一个控件了，CoordinatorLayout给我们带来了一种新的事件的处理方式——behavior，你是不是还记得我们在使用CoordinatorLayout的时候，一些子view需要一段，

```xml
app:layout_behavior="@string/appbar_scrolling_view_behavior"
```

这样的xml配置？当时我们不知道这是干嘛的，直接照用就行了，后来发现这玩意是一个类！而且我们还可以自定义！所以，今天这篇博客我们首先来学习一下如何自定义Behavior，之后的博客可能会看一下CoordinatorLayout是怎么处理这个Behavior的。

### 认识Behavior

Behavior是CoordinatorLayout的一个抽象内部类

```java
public abstract static class Behavior<V extends View> {
      public Behavior() {
      }

      public Behavior(Context context, AttributeSet attrs) {
      }
      ...
}
```

有一个泛型是指定的我们应用这个Behavior的View的类型，例如上面的appbar_scrolling_view_behavior对应的字符串其实是`android.support.design.widget.AppBarLayout$ScrollingViewBehavior`,这个`ScrollingViewBehavior`内部类指定的泛型是`View`,所以理论上这个Behavior我们任何的View都可以使用，我们在自定义的时候，如果不是特殊的行为，也可以直接指定泛型`View`。

在自定义Behavior的时候，我们需要关心的两组四个方法，为什么分为两组呢？看一下下面两种情况

> 1. 某个view监听另一个view的状态变化，例如大小、位置、显示状态等
> 2. 某个view监听CoordinatorLayout里的滑动状态

对于第一种情况，我们关心的是： 
`layoutDependsOn`和`onDependentViewChanged`方法， 
对于第二种情况，我们关心的是： 
`onStartNestedScroll`和`onNestedPreScroll`方法。 
对于这几个方法什么意思，我们需要干什么，稍候我们就能了解到。

### 初步自定义

现在我们就来根据第一种情况尝试自定义一个Behavior，这里我们实现一个简单的效果，让一个View根据另一个View上下移动。 
首先我们来自定义一个Behavior，起名为`DependentBehavior`

```java
public class DependentBehavior extends CoordinatorLayout.Behavior<View> {

    public DependentBehavior(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean layoutDependsOn(CoordinatorLayout parent, View child, View dependency) {
        return super.layoutDependsOn(parent, child, dependency);
    }

    @Override
    public boolean onDependentViewChanged(CoordinatorLayout parent, View child, View dependency) {
        ViewCompat.offsetLeftAndRight();
        return super.onDependentViewChanged(parent, child, dependency);
    }
}
```

注意一下，带有参数的这个构造必须要重载，因为在CoordinatorLayout里利用==反射==去获取这个Behavior的时候就是拿的这个构造。我们覆写了两个方法`layoutDependsOn`和`onDependentViewChanged`，这两个方法的参数都是一样的，解释一下，第一个不用说，就是当前的CoordinatorLayout，第二个参数是我们设置这个Behavior的View，第三个是我们关心的那个View。如何知道关心的哪个呢？`layoutDependsOn`的返回值决定了一切！

这里我们关心一个TextView好了，所以`layoutDependsOn`可以这么写,

```java
@Override
public boolean layoutDependsOn(CoordinatorLayout parent, View child, View dependency) {
    return dependency instanceof TextView;
}
```

现在设置好了关心谁，接下来就是在这个View状态发生变化的时候，我们现在的View该做些什么了，恩，这里肯定是在`onDependentViewChanged`做工作了。我们的任务就是获取dependency距离底部的距离，并且设置给child,很简单。

```java
@Override
public boolean onDependentViewChanged(CoordinatorLayout parent, View child, View dependency) {
    int offset = dependency.getTop() - child.getTop();
    ViewCompat.offsetTopAndBottom(child, offset);
    return true;
}
```

首先我们先获取两个View的top值的差，然后让child的位置位移一下就ok啦，如此简单，那这个简单的Behavior如何用呢？

```java
<android.support.design.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true"
    tools:context="org.loader.mybehavior.MainActivity">

    <TextView
        android:id="@+id/depentent"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:background="#FFFF0000"
        android:gravity="center"
        android:textColor="@android:color/white"
        android:layout_gravity="top|left"
        android:text="depentent"/>

    <TextView
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:background="#FF00FF00"
        android:gravity="center"
        android:textColor="@android:color/white"
        android:layout_gravity="top|right"
        app:layout_behavior="org.loader.mybehavior.DependentBehavior"
        android:text="auto"/>

</android.support.design.widget.CoordinatorLayout>
```

注意，第二个TextView我们设置了`app:layout_behavior="org.loader.mybehavior.DependentBehavior"` 
值正好是我们定义的那个`DependentBehavior`。

```java
final TextView depentent = (TextView) findViewById(R.id.depentent);
depentent.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        ViewCompat.offsetTopAndBottom(v, 5);
    }
});
```

在Activity中，我们每次点击第一个TextView都会去改变一下它的位置，下面让我们来看看另一个TextView的位置改变了没有。

![img](https://img-blog.csdn.net/20151214090538564)

### Scroll Behavior

在学会了如何自定义Behavior后，我们接着来实现上面说的第二种情况-滑动。为了演示这种Behavior的定义，我们还是来做个无用功，让一个ScrollView跟随另一个ScrollView滑动。恩，先来看看效果吧，

![img](https://img-blog.csdn.net/20151214090621925)

从效果中我们可以看出，第二个ScrollView明显是是在跟随第一个进行滑动，现在就让我们用自定义Behavior的形式实现它。 
创建一个Behavior，起名叫ScrollBehavior，

```java
public class ScrollBehavior extends CoordinatorLayout.Behavior<View> {

    public ScrollBehavior(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onStartNestedScroll(CoordinatorLayout coordinatorLayout, View child, View directTargetChild, View target, int nestedScrollAxes) {
        return super.onStartNestedScroll(coordinatorLayout, child, directTargetChild, target, nestedScrollAxes);
    }

    @Override
    public void onNestedPreScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dx, int dy, int[] consumed) {
        super.onNestedPreScroll(coordinatorLayout, child, target, dx, dy, consumed);
    }

    @Override
    public boolean onNestedPreFling(CoordinatorLayout coordinatorLayout, View child, View target, float velocityX, float velocityY) {
        return super.onNestedPreFling(coordinatorLayout, child, target, velocityX, velocityY);
    }
}
```

和你想的一样，我们覆写了`onStartNestedScroll`和`onNestedPreScroll`方法，但是除了这两个方法外，我们还覆写了`onNestedPreFling`方法，这个方法是干嘛的？ 估计大家已经猜出来了，这里是处理fling动作的，你想想，我们在滑动松开手的时候，ScrollView是不是还继续滑动一会，那我们也需要让跟随的那个ScrollView也要继续滑动一会，这种效果，`onNestedPreFling`就派上用场了。

好，接下来我们来实现代码，首先来看看`onStartNestedScroll`，这里的返回值表明这次滑动我们要不要关心，我们要关心什么样的滑动？当然是y轴方向上的。

```java
@Override
public boolean onStartNestedScroll(CoordinatorLayout coordinatorLayout, View child, View directTargetChild, View target, int nestedScrollAxes) {
    return (nestedScrollAxes & ViewCompat.SCROLL_AXIS_VERTICAL) != 0;
}1234
```

现在我们准备好了关心的滑动事件了，那如何让它滑动起来呢？还是要看`onNestedPreScroll`的实现

```java
@Override
public void onNestedPreScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dx, int dy, int[] consumed) {
    super.onNestedPreScroll(coordinatorLayout, child, target, dx, dy, consumed);
    int leftScrolled = target.getScrollY();
    child.setScrollY(leftScrolled);
}123456
```

也很简单，让child的scrollY的值等于目标的scrollY的值就ok啦，那fling呢？更简单,

```java
@Override
public boolean onNestedFling(CoordinatorLayout coordinatorLayout, View child, View target, float velocityX, float velocityY, boolean consumed) {
    ((NestedScrollView) child).fling((int)velocityY);
    return true;
}12345
```

直接将现在的y轴上的速度传递传递给child，让他fling起来就ok了。 
定义好了Behavior，就得在xml中使用了，使用方法和前面的一样。

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true"
    android:orientation="vertical">

    <android.support.v4.widget.NestedScrollView
        android:layout_gravity="left"
        android:layout_width="wrap_content"
        android:background="#FF00FF00"
        android:layout_height="match_parent">

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="vertical">
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentLeft"/>


        </LinearLayout>

    </android.support.v4.widget.NestedScrollView>

    <android.support.v4.widget.NestedScrollView
        android:layout_gravity="right"
        android:layout_width="wrap_content"
        android:background="#FFFF0000"
        android:layout_height="match_parent"
        app:layout_behavior="org.loader.mybehavior.ScrollBehavior">

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="vertical">
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingTop="50dp"
                android:paddingBottom="50dp"
                android:textColor="@android:color/white"
                android:text="contentRight"/>

        </LinearLayout>

    </android.support.v4.widget.NestedScrollView>

</android.support.design.widget.CoordinatorLayout>
```

第二个ScrollView的layout_behavior我们指定为`org.loader.mybehavior.ScrollBehavior`，现在就可以看到上面的效果了。

ok， 最后是文章中demo的代码下载：<http://download.csdn.net/detail/qibin0506/9352989>