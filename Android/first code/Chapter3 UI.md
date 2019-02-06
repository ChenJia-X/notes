# 第三章 UI

标签（空格分隔）： 未分类

---
## Question
1. 3.5.2，inflate()的第三个参数false是起什么作用？为什么不添加父布局？[定位](#3.5.2-定制listview的界面)
2. 能否写出通用的RecyclerViewAdapter和ViewHolder？
3. 观察者模式

---
## Content
### 3.2 常用控件/组件的使用方法 P77
#### 3.2.1 TextView
- 文字默认为居左上角对齐，通过`android:gravity`来指定文字的对齐方式。
- 对控件的高和宽指定固定值会造成适配的问题。
#### 3.2.2 Button
- 系统会对Button中的所有英文字母自动进行大写转换，可以通过`android：textAllCaps="false"`来禁止。
- 为点击事件注册监听器的方法：①匿名类；②实现接口。实现接口，可以集中管理点击事件的逻辑。
#### 3.2.3 EditText
- 使用`android：hint`属性来指定一段提示性文字。
- 使用`android：maxLines`属性来指定EditText的最大行数，避免EditText过分拉长。
#### 3.2.4 ImageView
图片通常都存放在以“drawable”开头的不同分辨率的目录下。
- 使用`android：src`属性来指定图片的地址。
- 使用`setImageResource()`来改变显示的图片。
#### 3.2.5 ProgressBar
>Android所有控件均有可见属性，可通过`android：visibility`属性进行指定，它有三个取值，visible、invisible、gone。还可以通过`setVisibility()`方法来设置可见性，可以传入View.VISIBILE、View.INVISIBLE、View.GONE三个值

- 通过`style`属性来指定多种进度条。
- 通过`android：max`来指定progress的最大值。
- 通过`setProgress()`和`getProgress()`方法来操作progress值。
#### 3.2.6 AlterDialog
使用方法如下所示：
```java
AlterDialog.Builder dialog = new AlterDialog.Builder(MainActivity.this);
dialog.setTitle("this is title");
dialog.setMessage("this is message");
dialog.setCancelable(false);
dialog.setPositiveButton("Ok", new DialogInterface.OnClickListener(){
    @Override                
    public void onClick(DialogInterface dialog, int which) {
        //do something
    }
});
dialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
    @Override
    public void onClick(DialogInterface dialog, int which) {
         //do something
    }
});
dialog.show();
```
#### 3.2.7 ProgressDialog
使用方法和AlertDialog较为相似。
>**注意：在setCancelable()中传入false，则无法使用Back键退出。当数据加载完，必须调用progressDialog的dismiss()方法来关闭对话框。**

### 3.3 详解4种基本布局 P94
####3.3.1 LinearLayout 
- `android:orientation`用于指定控件的排列顺序。**默认为horizontal**，水平排列；vertical，水平排列。按照控件在布局代码中的位置依次排列。
- `android:layout_gravity`用于指定控件在布局中的对齐方式；`android:gravity`用于指定文字在控件中的对齐方式。
> **注意：当LinearLayout的排列方式为horizontal时，它所包含的view的`android：layout_gravity`只能为vertical。同理当LinearLayout的排列方式为vertical时，`android：layout_gravity`只能为horizontal.**
- `android:layout_weight`属性允许使用比例的方式来指定控件的大小。**只有在LinearLayout中才可以使用这个属性。**

  以下是规范写法：
```
android:layout_width="0dp"
android:layout_weight="1"
```
#### 3.3.2 RelativeLayout
##### 1.相对父布局定位
    android:layout_alignParentRight
    android:layout_alignParentLeft
    android:layout_alignParentTop
    android:layout_alignParentBottom
    android:layout_centerInParent
##### 2.相对控件定位
```xml
android:layout_above
android:layout_below
android:layout_toRightOf
android:layout_toLeftOf
android:layout_alignLeft
android:layout_alignRight
android:layout_alignTop
android:layout_alignBottom
```
>**注意：当一个控件引用另一个控件时，该控件一定要定义在另一个控件的后面,否则会出现找不到id的情况**

#### 3.3.3 FrameLayout
所有控件默认摆放在布局的左上角。也可以使用`android.layout_gravity`属性来指定控件在布局中的对齐方式。因为定位方式存在缺陷，所以使用场景较少。
#### 3.3.4 百分比布局
只有在LinearLayout中才可以使用`android.layout_weight`属性。为了能够按比例指定控件大小，百分比布局为RelativeLayout、FrameLayout提供了PercentRelativeLayout、PercentFrameLayout两个全新的布局。
##### 使用方法
1. 打开`app/build.gradle`文件，在dependencies闭包中添加百分比布局依赖。
```
compile 'com.android.support:percent:24.2.1'
```
2. 在布局文件中，先写出最外层完整的包路。还要再定义一个app的[命名空间](http://blog.qiji.tech/archives/3744)，这样才能使用百分比布局的自定义属性。
```xml
<android.support.percent.PercentFrameLayout
    xmlns:android="……"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width=……><!--定义app命名空间-->
    
    <Button android:id="@+id/button1"
        android:layout_gravity="left|bottom"
        app:layout_widthPercent=50%
        app:layout_heightPercent=50%/>
        
    <Button android:id="@+id/button2"
        android:laytout_gravity="right|bottom"
        app:layout_widthPercent=50%
        app:layout_heightPercent=50%/>
</android.support.percent.PercentFrameLayout>
```
> **注意：在上面的代码中，能使用app的前缀就是因为刚才定义了app的命名空间。我们能一直使用android前缀的属性也是同样的道理。**

### 3.4 创建自定义控件 P109
>View是Android中一种最基本的组件，它可以在屏幕上绘制一块矩形区域，并能响应这块区域上的各种事件。
>ViewGroup是一种特殊的View，它是一个用于放置控件和布局的容器，它可以包含多个子View和子ViewGroup。
>所有控件都是直接或间接继承自View，所有布局都是直接或间接继承自ViewGroup。

#### 3.4.1 引入布局
    <include layout="layout/title"/>
- `android:padding`规定控件与父View的距离；
- `android:layout_margin`规定控件与其它（上下左右）View之间的距离。
##### 如何隐藏系统自带的标题栏。P111
```java
@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main3);
        android.support.v7.app.ActionBar actionBar = getSupportActionBar();
        if (actionBar != null){
            actionBar.hide();
        }
    }
```
#### 3.4.2 创建自定义控件
1. 创建自定义控件。先创建一个布局B(TitleLayout)的**类**,在该类中加载3.4.1中创建的布局A（title），并将B设为A的父布局。再为其中的各个控件添加事件以及功能。
```java
public class TitleLayout extends LinearLayout implements View.OnClickListener{
    public TitleLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
        LayoutInflater.from(context).inflate(R.layout.title,this);//加载3.4.1中创建的布局A（title），并将B（TitleLayout）设为A的父布局
        Button button_titleBack = (Button)findViewById(R.id.title_back);
        Button button_titleEdit = (Button)findViewById(R.id.title_edit);
        button_titleBack.setOnClickListener(this);
        button_titleEdit.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.title_back:
                ((Activity)getContext()).finish();
                break;
            case R.id.title_edit:
                Toast.makeText(getContext(),"nihao",Toast.LENGTH_SHORT).show();
        }
    }
}
```
>①LayoutInflater.from(context).inflate(R.layout.title,this);
>通过LayoutInflaer的from()可以构建出一个LayoutInflater对象，然后调用inflate()动态加载一个布局文件。inflate()方法的第一个参数是要加载的布局文件的id，第二个参数是给加载好的布局再添加一个父布局，这里我们想要指定为TitileLayout，于是直接传入this。
>②((Activity)getContext()).finish();
>其实就是从Activity传了个Context过来，不过因为不只Activity有Context，比如Service也有，所以加了个强制类型转化。而getContext()得到的是this，就相当于this.finish()，其实一般我们在Activity里直接finish()是一种简写。

2. 使用自定义控件。在布局C中，使用自定义控件的完整类名（包名不可省略），就可添加该控件。
```
<com.example.man.test.TitleLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content">    
</com.example.man.test.TitleLayout>
```
### 3.5 ListView P113
==*ListView*==:允许用户通过手指上下滑动的方式，将屏幕外的数据滚动到屏幕内，同时屏幕上原有的数据会滚动到屏幕外。
#### 3.5.1 ListView的简单用法
1. 添加控件
```
<ListView
    android:id="@+id/listview"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"/>
```
2. 新建一个Adapter，将context、子项（Item）的样式和data传入进去。
>数组中的数据无法直接传递给ListView，需要借助适配器。ArrayAdapter可以通过泛型来指定要匹配的数据类型。

3. 调用setAdapter()为ListView添加Adapter.
```java
private String[] data = {"apple","orange","watermelon","pear","grape","pineapple","strawberry","cherry","mango","banana","apple","orange","watermelon","pear","grape","pineapple", "strawberry","cherry","mango","banana"};

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main3);
    ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(Main3Activity.this,android.R.layout.simple_list_item_1,data);
    ListView listView = (ListView)findViewById(R.id.listview);
    listView.setAdapter(arrayAdapter);
}
```
#### 3.5.2 定制ListView的界面
1. 新建一个Fruit类
```
public class Fruit {
    private String name;
    private int imageId;

    public Fruit(String name, int imageId) {
        this.name = name;
        this.imageId = imageId;
    }
    public String getName() {
        return name;
    }
    public int getImageId() {
        return imageId;
    }
}
```
2. 新建一个fruit_item布局文件
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <ImageView
        android:id="@+id/fruit_image"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    <TextView
        android:id="@+id/fruit_name"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginLeft="10dp"
        android:layout_gravity="center_vertical"/>
</LinearLayout>
```
3.新建一个FruitAdapter类
```java
public class FruitAdapter extends ArrayAdapter<Fruit> {
    private int resourceid;

    public FruitAdapter(Context context, int resource, List<Fruit> objects) {
        super(context, resource, objects);
        resourceid=resource;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Fruit fruit = getItem(position);
        View view = LayoutInflater.from(getContext()).inflate(resourceid,parent,false);
        ImageView fruitImage = (ImageView) view.findViewById(R.id.fruit_image);
        TextView frutiName = (TextView) view.findViewById(R.id.fruit_name);
        frutiName.setText(fruit.getName());
        fruitImage.setImageResource(fruit.getImageId());
        return view;
        //return super.getView(position, convertView, parent);AS自动生成的返回值，但是在这个例子中运行会报错
    }
}
```
> ①getView()在每一个子项被滚动到屏幕内时会被调用。
> ②LayoutInflater.from(getContext()).inflate(resourceid,parent,false);第三个参数指定为false，表示只让我们在父布局中声明的layout属性生效，但不为view添加父布局。因为一旦view有了父布局之后，它就不能添加到ListView中了。

4. 将context、fruit_item布局和数据传入FruitAdapter，调用setAdapter()为ListView添加Adapter.
```java
private String[] data = {"apple","orange","watermelon","pear","grape","pineapple","strawberry","cherry","mango","banana","apple","orange","watermelon","pear","grape","pineapple", "strawberry","cherry","mango","banana"};
private List<Fruit> fruitList = new ArrayList<>();
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main3);
    initFruits();
    ListView listView = (ListView)findViewById(R.id.listview);
    FruitAdapter fruitAdapter = new FruitAdapter(Main3Activity.this,
            R.layout.fruit_item,fruitList);
    listView.setAdapter(fruitAdapter);
}

private void initFruits(){
    for (String f :
            data) {
        Fruit fruit = new Fruit(f,R.drawable.ic_launcher);
        fruitList.add(fruit);
    }
}
```
#### 3.5.3 提升ListView的运行效率
- 每次调用getView()时都会加载一遍布局，影响效率。
  解决方法：convertView参数可以将加载的布局进行缓存，以便之后可以重用。
- 每次调用getView()时都会获取一次控件的实例，影响效率。
  解决方法：新建一个ViewHolder类来缓存控件实例。
```java
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Fruit fruit = getItem(position);
        View view;
        ViewHolder viewHolder;
        if (convertView == null){
            view = LayoutInflater.from(getContext()).inflate(resourceid,parent,false);
            viewHolder = new ViewHolder();
            viewHolder.fruitName =(TextView) view.findViewById(R.id.fruit_name);
            viewHolder.fruitImage =(ImageView) view.findViewById(R.id.fruit_image);
            view.setTag(viewHolder);
        }else {
            view = convertView;
            viewHolder =(ViewHolder) view.getTag();
        }
        viewHolder.fruitName.setText(fruit.getName());
        viewHolder.fruitImage.setImageResource(fruit.getImageId());
        return view;
    }

    class ViewHolder{
        ImageView fruitImage;
        TextView fruitName;
    }
```
注意：可能会有人问ViewHolder静态类结合缓存convertView与直接使用convertView有什么区别吗，是否重复了在这里，官方给出了解释

> To work efficiently the adapter implemented here uses two techniques:
> -It reuses the convertView passed to getView() to avoid inflating View when it is not necessary
>
> （译:重用缓存convertView传递给getView()方法来避免填充不必要的视图）
> -It uses the ViewHolder pattern to avoid calling findViewById() when it is not necessary
>
> （译：使用ViewHolder模式来避免没有必要的调用findViewById()：因为太多的findViewById也会影响性能）
> ViewHolder类的作用
> -The ViewHolder pattern consists in storing a data structure in the tag of the view
> returned by getView().This data structures contains references to the views we want to bind data to,
> thus avoiding calling to findViewById() every time getView() is invoked
>
> （译：ViewHolder模式通过getView()方法返回的视图的标签(Tag)中存储一个数据结构，这个数据结构包含了指向我们

#### 3.5.4 ListView的点击事件

```java
listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        Fruit fruit = fruitList.get(position);
        Toast.makeText(Main3Activity.this,fruit.getName(),Toast.LENGTH_SHORT).show();
    }
});
```
> **注意：**
> **Fruit fruit = getItem(position);只能在Adapter内部使用。**
> **Fruit fruit = fruitList.get(position);则是在声明fruitList的那个类中使用，这里也就是Main3Activity。**

### 3.6 ListView的增强版RecyclerView
> ListView的布局排列是自身管理的，而RecyclerView则是把这个工作交给了LayoutManager。LayoutManager制定了一套可拓展的布局排列接口，子类只要按照接口的规范来实现，就能制定出不同排列方式的布局了。

#### 3.6.1 RecyclerView的基本用法
1. 打开app/build.gradle文件，在dependenceies闭包中添加远程依赖：
```
compile 'com.android.support:recyclerview-v7:24.2.1'
```
2. 在布局文件中，用**完整的包路径**添加RecyclerView：
```java
<android.support.v7.widget.RecyclerView
    android:id="@+id/recycler_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent"/>
```
3. 新建RecyclerViewAdapter类：
```java
public class FruitRAdapter extends RecyclerView.Adapter<FruitRAdapter.ViewHolder> {
    private List<Fruit> mFruitList;
    static class ViewHolder extends RecyclerView.ViewHolder{
         ImageView fruitImage;
         TextView fruitName;
        public ViewHolder(View itemView) {
            super(itemView);
            fruitImage = (ImageView)itemView.findViewById(R.id.fruit_image);
            fruitName = (TextView)itemView.findViewById(R.id.fruit_name);
        }
    }

    public FruitRAdapter(List<Fruit> fruitList) {
        mFruitList = fruitList;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.fruit_item,parent,false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        holder.fruitImage.setImageResource(mFruitList.get(position).getImageId());
        holder.fruitName.setText(mFruitList.get(position).getName());
    }

    @Override
    public int getItemCount() {
        return mFruitList.size();
    }
}
```
> - onCreateViewHolder()用于加载子项（item）布局，创建ViewHolder实例，将布局中的控件实例缓存到ViewHolder中。
> - onBindViewHolder()用于为ViewHolder中的实例设置属性。
> - gerItemCount()用于返回RecyclerView中item的数量。

4. 创建RecyclerViewAdapter的实例，并将context、item布局、data传递进去。

5. 为RecycleerView添加Adapter。

   ```java
   RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view);
   LinearLayoutManager layoutManager = new LinearLayoutManager(this);
   recyclerView.setLayoutManager(layoutManager);
   FruitRAdapter fruitRAdapter = new FruitRAdapter(fruitList);
   recyclerView.setAdapter(fruitRAdapter);
   ```
   > LayoutManager用于指定RecyclerView的布局方式，这里使用的LinearLayoutManager是线性布局，可以实现和ListView类似的效果。

#### 3.6.2 实现横向滚动和瀑布流

##### 实现横向滚动

1. 修改item布局。LinearLayout改成垂直方向排列，使其适合横向滚动要求。

2. 在[3.6.1](#3.6.1 RecyclerView的基本用法)的基础上,调用LinearLayout的setOrientation()来设置布局的排列方向，默认是纵向排列
```java
layoutManager.setOrientation(LinearLayoutManager.HORIZONTAL);
```

##### 实现瀑布流

1. 修改item布局。LinearLayout的宽度改为match_parent，因为瀑布流布局中item的宽度是根据布局的列数自动适配的，不是一个固定值。

2. LinearLayoutManager改为StaggeredGridLayoutManager。StaggeredGridLayoutManager()的第一个参数用于指定布局的列数，第二个参数用于指定布局的排列方向。

   ```java
   StaggeredGridLayoutManager layoutManager = new
                   StaggeredGridLayoutManager(3,StaggeredGridLayoutManager.VERTICAL);
   ```

同理实现网格布局也只需要将LinearLayoutManager改为GridLayoutManager。GridLayoutManager()的第一个参数是context，第二个是网格列数（spanCount）。

#### 3.6.3 RecyclerView的点击事件

##### ①在Adapter内部实现点击事件的业务逻辑

> ListView的点击事件是对整个子项（item）注册了点击监听器，而RecyclerView为了能对item中的所有view添加监听器，舍弃了子项点击事件的监听器，所有的点击事件都由具体的View在**Adapter**中注册。

```java
public class FruitRAdapter extends RecyclerView.Adapter<FruitRAdapter.ViewHolder> implements View.OnClickListener {
    private List<Fruit> mFruitList;

    static class ViewHolder extends RecyclerView.ViewHolder{
        View fruitView;//添加了子项的view
        ImageView fruitImage;
        TextView fruitName;
        public ViewHolder(View itemView) {
            super(itemView);
            fruitView = itemView;
            fruitImage = (ImageView)itemView.findViewById(R.id.fruit_image);
            fruitName = (TextView)itemView.findViewById(R.id.fruit_name);
        }
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.fruit_item,parent,false);
        final ViewHolder holder = new ViewHolder(view);
        holder.fruitView.setOnClickListener(this);//为item和image分别注册了点击监听器
        holder.fruitImage.setOnClickListener(this);
        return new ViewHolder(view);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.fruit_view:
                Toast.makeText(v.getContext(),"view",Toast.LENGTH_SHORT).show();
                break;
            case R.id.fruit_image:
                Toast.makeText(v.getContext(),"image",Toast.LENGTH_SHORT).show();
                break;
        }
    }
    ...
}
```

##### ②在Adapter外部实现点击事件业务逻辑

[模拟ListView的setOnItemClickListener()方法](http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2015/0327/2647.html#commettop)

​	[[设计模式学习笔记-观察者模式](http://www.cnblogs.com/wangjq/archive/2012/07/12/2587966.html)] **还不太看得懂，为什么使用观察者模式就能降低耦合	**

​	[android观察者模式](http://www.cnblogs.com/xilin/archive/2012/07/31/2617258.html)

​	[Android 设计模式 之 观察者模式](http://blog.csdn.net/fangchongbory/article/details/7774044)

###### 实现方式：

1. 现在Adapter中定义一个接口 `OnRecyclerViewItemClickListener`

   1. ```java
      public interface OnRecyclerViewItemClickListener {
          void onItemClick(View view, News data);
      }
      ```

2. 在Adapter中声明一个成员变量`mOnRecyclerViewItemClickListener`

   1. ```java
      private OnRecyclerViewItemClickListener mOnRecyclerViewItemClickListener = null;
      ```

3. 在Adapter中创建暴露给外部的`setOnItemClickListener()`

   1. ```java
      public void setOnItemClickListener(OnRecyclerViewItemClickListener OnRecyclerViewItemClickListener){
          mOnRecyclerViewItemClickListener =OnRecyclerViewItemClickListener;
      }
      ```

4. 先为Adapter实现`View.OnClickListener`接口，再在Adapter的`onCreateViewHolder()`中为需要添加点击事件的View或控件添加OnClickListener。

   1. ```java
      @Override
      public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
          View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.left_title_item,parent,false);
          final ViewHolder holder = new ViewHolder(view);
          holder.title.setOnClickListener(this);//添加OnClickListener
          return holder;
      }
      ```

5. 在Adapter的`onBindViewHolder()`中设置setTag()，将数据存储到其中

   1. ```java
      @Override
      public void onBindViewHolder(ViewHolder holder, int position) {
          holder.title.setText(mtitleList.get(position).getTitle());
          holder.title.setTag(mtitleList.get(position));//设置setTag
      }
      ```

6. 在Adapter中重写`OnClickListener`接口的`onClick()`，调用`getTag()`从Tag中读取数据。

   1. ```java
      @Override
      public void onClick(View v) {
          switch (v.getId()){
              case R.id.lefit_title:
                  if (mOnRecyclerViewItemClickListener != null){
                      mOnRecyclerViewItemClickListener.onItemClick(v,(News) v.getTag());//从Tag中读取数据
                  }
                  break;
              default:
                  break;
          }
      }
      ```

7. 在其它需要调用Adapter的类或活动中，调用`3`中Adapter的`setOnItemClickListener()`,创建一个`RecyclerViewAdapter.OnRecyclerViewItemClickListener`实例作为参数传入`setOnItemClickListener()`中,并根据业务需要重写`onItemClick()`。

   1. ```java
      recyclerViewAdapter.setOnItemClickListener(new RecyclerViewAdapter.OnRecyclerViewItemClickListener() {
          @Override
          public void onItemClick(View view, News data) {
            	//do something，这里是在碎片中替换碎片，并用Bundle传递数据
              FragmentTransaction fragmentTransaction =
                      getActivity().getSupportFragmentManager().beginTransaction();
              Bundle bundle = new Bundle();
              bundle.putString("title",data.getTitle());
              bundle.putString("content",data.getContent());
            	rightFragment = new RightFragment();
              rightFragment.setArguments(bundle);
              fragmentTransaction.replace(R.id.container,rightFragment);
              fragmentTransaction.addToBackStack(null);
              fragmentTransaction.commit();
          }
      });
      ```


#### 3.7.1 制作Nine-Patch图片 P133

#### 3.7.2 编写精美的聊天界面 

1. 创建一个message类、msg_item.xml、MsgRecyclerViewAdapter类
2. 新建一个MainActivity，在布局中添加RecyclerView、Button、EditText。
3. 在MainActivity中使用RecyclerView。

<!--代码太多了就不贴上来了，书上代码上画红线的地方都是关键以及容易遗忘的点-->

