# Java内部类的解析

## 内部类的分类

- 根据内部类声明的位置不同，可以分为`成员内部类`、`局部内部类`、`匿名内部类`。
- 此外还可以根据是否声明为static，分为`静态内部类`、`非静态内部类`。

**注意：**为了更好的定义以及划分，引入了树的深度的概念来区分各种内部类。

本文参考[Java内部类详解](http://www.cnblogs.com/dolphin0520/p/3811445.html)

## 一、成员内部类

### 1. 定义

成员内部类定义在类的第一层，深度为1，与成员变量处于同一深度。

### 2.创建

- ①在外部类的非static方法中创建内部类的实例：直接new一个就行了。
- ②在外部类的static方法中创建内部类的实例：先创建一个外部类的实例，再通过外部类的实例创建一个内部类。
  - ==其它四个都好理解，就是第二个为什么会这样需要进一步了解==
- ③在其它的类中创建内部类的实例：先创建一个外部类的实例，在用外部类的实例创建一个内部类的实例。
- ④在外部类中创建静态内部类：直接new一个就行了。
- ⑤在其它的类中创建静态内部类：通过引用外部类的类名创建静态内部类。

> ```java
> class Bean{
>     class Bean3{
>         public int k = 0;
>     }
>   	static class Bean4{
>         public int l=0;
>     }
> }
> public class Circle {
>   	class Bean1{
>         public int I = 0;
>     }
>     static class Bean2{
>         public int J = 0;
>     }
>     public void test(){
>         Bean1 bean1 = new Bean1();//①在外部类的非static方法中创建内部类的实例
>     }
>     public static void main(String[] args){
>         // 初始化Bean1
>         Circle circle =new Circle();
>         Circle.Bean1 bean1=circle.new Bean1(); //②在外部类的static方法中创建内部类的实例
>         bean1.I++;
>         //初始化Bean3
>         Bean bean =new Bean();
>         Bean.Bean3 bean3 = bean.new Bean3(); //③在其它的类中创建内部类的实例
>         bean3.k++;
>       	// 初始化Bean2
>         Bean2 bean2 = new Bean2(); //④在外部类中创建静态内部类
>         bean2.J++;
>       	//初始化Bean4
>         Bean.Bean4 bean4 = new Bean.Bean4();//⑤在其它的类中创建静态内部类
>         bean4.l++;
>     }
> }
> ```

### 3.内部类和外部类之间的通信

- 内部类可以随意调用外部类的成员变量和成员方法。
- 外部类要调用内部类的成员变量方法需要先获取内部类的实例，再通过这个对这个实例的引用来访问相应的成员变量和成员方法。
- 当内部类和外部类有同名的成员变量和方法，默认情况下访问的是的是成员内部类的成员。