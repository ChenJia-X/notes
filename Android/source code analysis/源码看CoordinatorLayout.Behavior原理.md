# [源码看CoordinatorLayout.Behavior原理](https://blog.csdn.net/qibin0506/article/details/50377592)

版权声明：本文来自Loader's Blog，未经博主允许不得转载。 https://blog.csdn.net/qibin0506/article/details/50377592

在上一篇博客[CoordinatorLayout高级用法-自定义Behavior](http://blog.csdn.net/qibin0506/article/details/50290421)中，我们介绍了如何去自定义一个CoordinatorLayout的Behavior，通过文章也可以看出Behavior在CoordinatorLayout中地位是相当高的，那么今天我们就来接着上篇博客来从源码分析一下Behavior的实现思路，如果你对CoordinatorLayout和Behavior还不熟悉的话，建议先去看看上篇博客[《CoordinatorLayout高级用法-自定义Behavior》](http://blog.csdn.net/qibin0506/article/details/50290421)。

这篇文章我们要分析的内容有：

> 1. Behavior的实例化
> 2. layoutDependsOn和onDependentViewChanged调用过程
> 3. onStartNestedScroll和onNestedPreScroll实现原理
> 4. Behavior的事件分发过程

## Behavior的实例化

大家都知道，我们在view中可以通过`app:layout_behavior`然后指定一个字符串来表示使用哪个behavior，稍微去想一下，**在CoordinatorLayout中肯定是利用反射机制来完成的behavior的实例化**，现在就让我们从CoordinatorLayout的源码中找寻答案，来验证我们的猜想。首先，我们来看看CoordinatorLayout的一个内部类，也是大家熟悉的`LayoutParams`，

```Java
public static class LayoutParams extends ViewGroup.MarginLayoutParams {
       /**
        * A {@link Behavior} that the child view should obey.
        */
       Behavior mBehavior;
       ...
}
```

在这里我们确实看到了behavior的影子，那它是在什么时候被初始化的呢？继续看代码，

```Java
LayoutParams(Context context, AttributeSet attrs) {
    super(context, attrs);

    final TypedArray a = context.obtainStyledAttributes(attrs,
            R.styleable.CoordinatorLayout_LayoutParams);
    ...
    mBehaviorResolved = a.hasValue(
            R.styleable.CoordinatorLayout_LayoutParams_layout_behavior);
    if (mBehaviorResolved) {
        mBehavior = parseBehavior(context, attrs, a.getString(
                R.styleable.CoordinatorLayout_LayoutParams_layout_behavior));
    }

    a.recycle();
}
```

在LayoutParams的构造方法中，首先是去检查了是不是有`layout_behavior`，这里很容易理解，接下来调用了`parseBehavior`方法，返回了Behavior的实例，我们非常有理由去看看`parseBehavior`到底干了嘛，或许我们要的答案就在里面！

```Java
// 这里是指定的Behavior的参数类型
static final Class<?>[] CONSTRUCTOR_PARAMS = new Class<?>[] {
        Context.class,
        AttributeSet.class
};

...

static Behavior parseBehavior(Context context, AttributeSet attrs, String name) {
    if (TextUtils.isEmpty(name)) {
        return null;
    }

    // 代表了我们指定的那个behavior的完整路径
    final String fullName;
    // 如果是".MyBehavior"
    // 则在前面加上程序的包名
    if (name.startsWith(".")) {
        // Relative to the app package. Prepend the app package name.
        fullName = context.getPackageName() + name;
    } else if (name.indexOf('.') >= 0) {
        // 这里我们指定了全名
        // Fully qualified package name.
        fullName = name;
    } else {
        // Assume stock behavior in this package (if we have one)
        fullName = !TextUtils.isEmpty(WIDGET_PACKAGE_NAME)
                ? (WIDGET_PACKAGE_NAME + '.' + name)
                : name;
    }

    try {
        Map<String, Constructor<Behavior>> constructors = sConstructors.get();
        if (constructors == null) {
            constructors = new HashMap<>();
            sConstructors.set(constructors);
        }
        Constructor<Behavior> c = constructors.get(fullName);
        // 这里利用反射去实例化了指定的Behavior
        // 并且值得注意到是，这里指定了构造的参数类型
        // 也就是说我们在自定义Behavior的时候，必须要有这种类型的构造方法
        if (c == null) {
            final Class<Behavior> clazz = (Class<Behavior>) Class.forName(fullName, true,
                    context.getClassLoader());
            c = clazz.getConstructor(CONSTRUCTOR_PARAMS);
            c.setAccessible(true);
            constructors.put(fullName, c);
        }
        return c.newInstance(context, attrs);
    } catch (Exception e) {
        throw new RuntimeException("Could not inflate Behavior subclass " + fullName, e);
    }
}
```

上面的代码很容易理解，就是利用反射机制去实例化了Behavior，调用的是两个参数的那个构造方法，这也就是我们在自定义Behavior的时候为什么一定要去重写，

```Java
public Behavior(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
```

这个构造的原因。看来获取一个Behavior的实例还是很简单的，那么，下面就让我们开始分析Behavior中常用方法调用的机制吧。

## layoutDependsOn和onDependentViewChanged调用过程

在上一篇博客中我们学会了自定义两种形式的Behavior，其中第一种就是去观察一个view的状态变化，也就是涉及到`layoutDependsOn`和`onDependentViewChanged`两个方法的调用，现在我们从源码的角度来分析一下这两个方法调用的时机和调用的过程，**在前一篇博客中我们提到过`onDependentViewChanged`这个方法会在view的状态发生变化后去调用，那在状态发生变化时必定会执行什么操作呢？重绘，是的，状态变化了，那肯定重绘是避免不了的**，在`CoordinatorLayout`中注册了一个`ViewTreeObserver`，我们可以从这里入手，因为它可以监听到view的各种状态变化，

```Java
@Override
public void onAttachedToWindow() {
    super.onAttachedToWindow();
    resetTouchBehaviors();
    if (mNeedsPreDrawListener) {
        if (mOnPreDrawListener == null) {
            // 实例化了OnPreDrawListener
            // 并在下面注册到了ViewTreeObserver中
            mOnPreDrawListener = new OnPreDrawListener();
        }
        final ViewTreeObserver vto = getViewTreeObserver();
        vto.addOnPreDrawListener(mOnPreDrawListener);
    }
    if (mLastInsets == null && ViewCompat.getFitsSystemWindows(this)) {
        // We're set to fitSystemWindows but we haven't had any insets yet...
        // We should request a new dispatch of window insets
        ViewCompat.requestApplyInsets(this);
    }
    mIsAttachedToWindow = true;
}
```

在`onAttachedToWindow`向ViewTreeObserver注册了一个监听draw变化的Observer，那在这里Observer中到底干了嘛呢？

```Java
class OnPreDrawListener implements ViewTreeObserver.OnPreDrawListener {
    @Override
    public boolean onPreDraw() {
        dispatchOnDependentViewChanged(false);
        return true;
    }
}
```

就两行代码，调用了`dispatchOnDependentViewChanged`方法，看方法名我们就知道这次找对对象了，怀着激动的心情来看看`dispatchOnDependentViewChanged`

```Java
void dispatchOnDependentViewChanged(final boolean fromNestedScroll) {
    final int layoutDirection = ViewCompat.getLayoutDirection(this);
    final int childCount = mDependencySortedChildren.size();
    // 遍历所有的子view
    for (int i = 0; i < childCount; i++) {
        final View child = mDependencySortedChildren.get(i);
        final LayoutParams lp = (LayoutParams) child.getLayoutParams();
        ...

        // Did it change? if not continue
        // 检查是否变化了，没有变化直接下一次循环
        final Rect oldRect = mTempRect1;
        final Rect newRect = mTempRect2;
        getLastChildRect(child, oldRect);
        getChildRect(child, true, newRect);
        if (oldRect.equals(newRect)) {
          continue;
        }

        // Update any behavior-dependent views for the change
        // 这里从下一个子view开始
        //mDependencySortedChildren有一个排序规则
        // selectionSort
        // 感兴趣的可以看一下mDependencySortedChildren部分。
        for (int j = i + 1; j < childCount; j++) {
            final View checkChild = mDependencySortedChildren.get(j);
            final LayoutParams checkLp = (LayoutParams) checkChild.getLayoutParams();
            // 获取到Behavior
            final Behavior b = checkLp.getBehavior();
            // 这里调用Behavior的layoutDependsOn来判断我们的带有behavior的view是不是依赖这个view
            if (b != null && b.layoutDependsOn(this, checkChild, child)) {
                if (!fromNestedScroll && checkLp.getChangedAfterNestedScroll()) {
                    // If this is not from a nested scroll and we have already been changed
                    // from a nested scroll, skip the dispatch and reset the flag
                    checkLp.resetChangedAfterNestedScroll();
                    continue;
                }

                // 这里调用了Behavior的onDependentViewChanged
                final boolean handled = b.onDependentViewChanged(this, checkChild, child);
                ...
            }
        }
    }
}
```

`dispatchOnDependentViewChanged`方法有一个布尔类型的参数，上面我们传递的是false， 这里主要是区分是view引起的状态变化还是布局引起的，在一些的scroll中也会调用`dispatchOnDependentViewChanged`这个方法。

好了，现在我们终于搞懂了`onDependentViewChanged`调用机制了，下面我们来看看关于滑动监听的部分。

## onStartNestedScroll和onNestedPreScroll实现原理

在开始源码之前，我们先来思考个问题，现在有一个view是可以上下滑动的，那这个view的滑动对于父view来说是不是可见的？或者说是可预知的？显然不是，一个view的滑动对于父布局来说是透明的？所以现在我们不能简简单单的从`CoordinatorLayout`入手了，而是要从那个可以滑动的view入手，我们选择`NestedScrollView`来进行分析。`NestedScrollView`有一个`NestedScrollingChildHelper`类型的变量`mChildHelper`引起了我们的注意，因为很多看名字很像关于滑动部分的代码都调用了这个类的一些方法，来看看有哪些吧？

```Java
mChildHelper = new NestedScrollingChildHelper(this);

...

@Override
public void onNestedScrollAccepted(View child, View target, int nestedScrollAxes) {
    mParentHelper.onNestedScrollAccepted(child, target, nestedScrollAxes);
    startNestedScroll(ViewCompat.SCROLL_AXIS_VERTICAL);
}

@Override
public void onNestedScroll(View target, int dxConsumed, int dyConsumed, int dxUnconsumed,
        int dyUnconsumed) {
    final int oldScrollY = getScrollY();
    scrollBy(0, dyUnconsumed);
    final int myConsumed = getScrollY() - oldScrollY;
    final int myUnconsumed = dyUnconsumed - myConsumed;
    dispatchNestedScroll(0, myConsumed, 0, myUnconsumed, null);
}

@Override
public boolean startNestedScroll(int axes) {
    return mChildHelper.startNestedScroll(axes);
}

@Override
public boolean dispatchNestedScroll(int dxConsumed, int dyConsumed, int dxUnconsumed,
        int dyUnconsumed, int[] offsetInWindow) {
    return mChildHelper.dispatchNestedScroll(dxConsumed, dyConsumed, dxUnconsumed, dyUnconsumed,
            offsetInWindow);
}

@Override
public boolean dispatchNestedPreScroll(int dx, int dy, int[] consumed, int[] offsetInWindow) {
    return mChildHelper.dispatchNestedPreScroll(dx, dy, consumed, offsetInWindow);
}
```

很简单，不过我们好像发现了一点眉目，这些方法何时调用我们还是不是很清楚，滑动必然和事件有关，我们就来从事件的部分入手吧，毕竟是我们熟悉的地方。

```Java
@Override
public boolean onInterceptTouchEvent(MotionEvent ev) {
  ...
  switch (action & MotionEventCompat.ACTION_MASK) {
      ...
     case MotionEvent.ACTION_DOWN: {
       ...
       startNestedScroll(ViewCompat.SCROLL_AXIS_VERTICAL);
     }
     ...
  }
  ...
}
```

在down的时候我们调用了`startNestedScroll`方法，那我们就顺着这条线往下看`mChildHelper.startNestedScroll(axes)`。

```Java
public boolean startNestedScroll(int axes) {
    if (hasNestedScrollingParent()) {
        // Already in progress
        return true;
    }
    if (isNestedScrollingEnabled()) {
       // 获取当前view的parent
        ViewParent p = mView.getParent();
        View child = mView;
        // 一个循环，不断的往上层去获取parent
        // 直到条件成立，或者没有parent了 退出
        while (p != null) {
            // 这里是关键代码，猜测这里肯定肯定去调用了CoordinatorLayout的对应方法。
            if (ViewParentCompat.onStartNestedScroll(p, child, mView, axes)) {
                mNestedScrollingParent = p;
                ViewParentCompat.onNestedScrollAccepted(p, child, mView, axes);
                return true;
            }
            if (p instanceof View) {
                child = (View) p;
            }
            // 替换，继续循环
            p = p.getParent();
        }
    }
    return false;
}
```

在这个方法中一个while循环，不断的去获取view的的parent，然后一个`ViewParentCompat.onStartNestedScroll`作为条件成立了就return true了，我们有理由猜测`ViewParentCompat.onStartNestedScroll`里去调用了`CoordinatorLayout`的相应方法。注意参数，p是我们遍历到父view，我们先认为是`CoordinatorLayout`吧，child是`CoordinatorLayout`的直接嵌套着目标view的子view，mView在这里就是`NestedScrollView`了。

```Java
public class ViewParentCompat {
   static class ViewParentCompatStubImpl implements ViewParentCompatImpl {
     @Override
      public boolean onStartNestedScroll(ViewParent parent, View child, View target,
             int nestedScrollAxes) {
           if (parent instanceof NestedScrollingParent) {
               return ((NestedScrollingParent) parent).onStartNestedScroll(child, target,
                       nestedScrollAxes);
           }
           return false;
      }
   }
}
```

这里面很简单，看看parent是不是`NestedScrollingParent`类型的，如果是，则调用了`onStartNestedScroll`这个方法，而我们的`CoordinatorLayout`肯定是实现了`NestedScrollingParent`接口的，

```Java
public class CoordinatorLayout extends ViewGroup implements NestedScrollingParent { }
```

好了，现在我们终于回到`CoordinatorLayout`了，来看看他的`onStartNestedScroll`方法，

```Java
public boolean onStartNestedScroll(View child, View target, int nestedScrollAxes) {
    boolean handled = false;

    final int childCount = getChildCount();
    for (int i = 0; i < childCount; i++) {
        final View view = getChildAt(i);
        final LayoutParams lp = (LayoutParams) view.getLayoutParams();
        final Behavior viewBehavior = lp.getBehavior();
        if (viewBehavior != null) {
            // 调用遍历出来的这个子view的onStartNestedScroll方法
            final boolean accepted = viewBehavior.onStartNestedScroll(this, view, child, target,
                    nestedScrollAxes);
            handled |= accepted;

            lp.acceptNestedScroll(accepted);
        } else {
            lp.acceptNestedScroll(false);
        }
    }
    return handled;
}
```

这里还是去遍历了所有子view，然后去调用它的`onStartNestedScroll`方法，它的返回值，决定了`NestedScrollingChildHelper.onStartNestedScroll`是不是要继续遍历，如果我们的子view对这个view的滑动感兴趣，就返回true，它的遍历就会结束掉。

好了，现在start的过程我们分析完了，大体的流程就是：

> NestedScrollView.onInterceptTouchEvent->NestedScrollingChildHelper.onStartNestedScroll->CoordinatorLayout.onStartNestedScroll

下面的各种滑动调用流程也是一样的，这里我们就不再重复分析了，感兴趣的可以自己去看一下源码。

## Behavior的事件分发过程

上面的分析其实已经将我们自定义Behavior中使用到的方法的调用流程分析完了，不过我们还是要拓展一下，其实Behavior也是支持事件的传递的，在这方面，Behavior好像是一个代理一样，在CoordinatorLayout的各种事件处理的方法中去调用Behavior的事件处理方法，返回值决定了CoordinatorLayout对事件的消费情况。

```Java
@Override
public boolean onInterceptTouchEvent(MotionEvent ev) {
    MotionEvent cancelEvent = null;

    final int action = MotionEventCompat.getActionMasked(ev);

    // Make sure we reset in case we had missed a previous important event.
    if (action == MotionEvent.ACTION_DOWN) {
        resetTouchBehaviors();
    }

    // 去看看子view中behavior是有要拦截
    // 如果要拦截，则我们要拦截
    // 在这里Behavior类似一个代理
    final boolean intercepted = performIntercept(ev, TYPE_ON_INTERCEPT);

    if (cancelEvent != null) {
        cancelEvent.recycle();
    }

    if (action == MotionEvent.ACTION_UP || action == MotionEvent.ACTION_CANCEL) {
        resetTouchBehaviors();
    }

    return intercepted;
}
```

这里面调用了`performIntercept`方法，而且指定了个常量`TYPE_ON_INTERCEPT`代表了我们在拦截阶段调用的，既然有区分，肯定在别的地方也有调用，答案是肯定的，在`onTouch`里也有对`performIntercept`的调用，

```Java
@Override
public boolean onTouchEvent(MotionEvent ev) {
    boolean handled = false;
    boolean cancelSuper = false;
    MotionEvent cancelEvent = null;

    final int action = MotionEventCompat.getActionMasked(ev);

    // 这里要说道说道
    // 两个条件：1 如果behavior想要拦截
    // 2 behavior的onTouchEvent返回true
    // 为什么会有两个条件呢？
    // 解答：第一个条件是正常的分发流程， 很容易理解
    //
    // 第二个条件是在没有子view消费事件，所以事件会冒泡到此
    // 这时，我们还要继续询问behavior是否要消费该事件
    // 这里在performIntercept中执行的是：
    //  case TYPE_ON_TOUCH: // 从onTouchEvent调用的
    // intercepted = b.onTouchEvent(this, child, ev);
    // break;
    // 当intercepted为true时，表示我们对该down事件感兴趣
    // 此时 mBehaviorTouchView也有了赋值
    if (mBehaviorTouchView != null || (cancelSuper = performIntercept(ev, TYPE_ON_TOUCH))) {
        // Safe since performIntercept guarantees that
        // mBehaviorTouchView != null if it returns true
        final LayoutParams lp = (LayoutParams) mBehaviorTouchView.getLayoutParams();
        final Behavior b = lp.getBehavior();
        if (b != null) {
            // 这里同样的事件会继续执行一遍onTouchEvent?
            handled = b.onTouchEvent(this, mBehaviorTouchView, ev);
        }
    }

    // 如果behavior不感兴趣
    // 轮到自己了，问问自己干不感兴趣
    // Keep the super implementation correct
    if (mBehaviorTouchView == null) {
        handled |= super.onTouchEvent(ev);
    } else if (cancelSuper) {
        // 如果behavior执行了事件（并不是拦截了事件，上面的第一个if的第一个条件不成立，第二个条件成立）
        // 能执行到这，说明behavior没有拦截事件，但在事件冒泡的过程中消费了事件
        // mBehaviorTouchView是在performIntercept(ev, TYPE_ON_TOUCH)赋值的
        // 则给自己执行一个cancel事件
        if (cancelEvent == null) {
            final long now = SystemClock.uptimeMillis();
            cancelEvent = MotionEvent.obtain(now, now,
                    MotionEvent.ACTION_CANCEL, 0.0f, 0.0f, 0);
        }
        super.onTouchEvent(cancelEvent);
    }

    if (!handled && action == MotionEvent.ACTION_DOWN) {

    }

    if (cancelEvent != null) {
        cancelEvent.recycle();
    }

    if (action == MotionEvent.ACTION_UP || action == MotionEvent.ACTION_CANCEL) {
        resetTouchBehaviors();
    }

    return handled;
}
```

恩，这里面的代码注释已经写的很明白了，但是需要注意的一点，这一点我很长时间没有想通，就是为什么还要在`onTouch`里还要调用一遍`performIntercept`，是这样的，假如现在事件没有任何子view去消费，那么事件会冒泡到此，本着把Behavior看作是一个代理的原则，这里肯定还是要去询问一下Behavior是不是要执行这个事件，注意这里说的是执行而不是拦截，这是因为`performIntercept`不仅仅会调用Behavior的拦截部分的代码，也会调用执行的代码，就是通过第二个参数区分的。可以看到，这里我们使用了`TYPE_ON_TOUCH`。 
好了，说了这么多`performIntercept`，是时候来看看`performIntercept`的代码了。

```Java
private boolean performIntercept(MotionEvent ev, final int type) {
    boolean intercepted = false;
    boolean newBlock = false;

    MotionEvent cancelEvent = null;

    final int action = MotionEventCompat.getActionMasked(ev);

    final List<View> topmostChildList = mTempList1;
    getTopSortedChildren(topmostChildList);

    // Let topmost child views inspect first
    final int childCount = topmostChildList.size();
    for (int i = 0; i < childCount; i++) {
        final View child = topmostChildList.get(i);
        final LayoutParams lp = (LayoutParams) child.getLayoutParams();
        final Behavior b = lp.getBehavior();

        // 如果现在已经有拦截了的
        // 并且现在是down
        // 则 所有的behavior会受到一个cancel事件
        if ((intercepted || newBlock) && action != MotionEvent.ACTION_DOWN) {
            // Cancel all behaviors beneath the one that intercepted.
            // If the event is "down" then we don't have anything to cancel yet.
            if (b != null) {
                if (cancelEvent == null) {
                    final long now = SystemClock.uptimeMillis();
                    cancelEvent = MotionEvent.obtain(now, now,
                            MotionEvent.ACTION_CANCEL, 0.0f, 0.0f, 0);
                }
                switch (type) {
                    case TYPE_ON_INTERCEPT: // 从onInterceptTouchEvent调用的
                        b.onInterceptTouchEvent(this, child, cancelEvent);
                        break;
                    case TYPE_ON_TOUCH: // 从onTouch调用的
                        b.onTouchEvent(this, child, cancelEvent);
                        break;
                }
            }
            continue;
        }

        // 如果现在还没有拦截 并且具有behavior
        if (!intercepted && b != null) {
            switch (type) {
                case TYPE_ON_INTERCEPT: // 从onInterceptTouchEvent调用的
                    intercepted = b.onInterceptTouchEvent(this, child, ev);
                    break;
                case TYPE_ON_TOUCH: // 从onTouchEvent调用的
                    intercepted = b.onTouchEvent(this, child, ev);
                    break;
            }
            if (intercepted) {
                mBehaviorTouchView = child;
            }
        }

        // Don't keep going if we're not allowing interaction below this.
        // Setting newBlock will make sure we cancel the rest of the behaviors.
        final boolean wasBlocking = lp.didBlockInteraction();
        final boolean isBlocking = lp.isBlockingInteractionBelow(this, child);
        newBlock = isBlocking && !wasBlocking;
        // 如果不允许继续分发，则直接退出
        if (isBlocking && !newBlock) {
            // Stop here since we don't have anything more to cancel - we already did
            // when the behavior first started blocking things below this point.
            break;
        }
    }

    topmostChildList.clear();

    return intercepted;
}
```

这里面的代码也很容易理解，就是去遍历所有的view，在不同的情景下调用Behavior的onInterceptTouchEvent或onTouch方法。

好了关于Behavior的源码我们就分析到这里，相信大家在看完之后会对Behavior有一个全新的认识，而且google已经建议我们使用support design的东西了(没发现现在的项目默认模板文件就是一个标准的support design布局吗)，所以我们还是有必要对新东西有个更加深入的认识，而且这样也会有助于我们理解google工程师的思路，在解决一些问题的时候我们完全可以参考一下这些思路。 
ok，不扯了，今天就到这里吧，拜拜。