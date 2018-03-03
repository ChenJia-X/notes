# Chapter6 Interface、Lambda Expressions、Inner Classes 

## Questions

1. [接口与抽象类](#3.接口与抽象类) 设计成超类还是接口？

## Concepts

1. -6.1.3- multiple inheritance
2. -6.1.5- interface evolution
3. -6.1.5- source compatible
4. -6.2- callback
5. -6.2.3- 浅拷贝、深拷贝
6. -6.2.3- tagging interfacex
7. -6.3.3- functional interface

## Notifications

1. -6.1.5- 在接口中使用默认方法可以解决两个问题：①重新编译时，保证`source compatible`。当为接口增加新的方法时，不需要为使用该接口的source实现新的方法。②当不重新编译时，如果程序调用接口新增加的方法，可以避免出现`AbstractMethodError`。

## Concrete contents

### 6.1 接口

接口不是类，而是对类的一组需求（功能）的描述。

#### 1.接口的特性

- 接口不能有实例域，但可以有常量。常量会被自动设置为`public static final`。


- 在Java SE 8以下时，接口中的方法不能实现。
  - 方法在接口中会被自动设置为`public abstract（abstract书中没写）`，但是在实现接口时，必须把方法声明为public。
- 在Java SE 8中允许接口中增加`static method`。从而接口对应的伴随类就不再时必要的了。
- 在接口中使用`default method`可以解决两个问题：
  - ①重新编译时，保证`source compatible`。当为接口增加新的方法时，不需要为使用该接口的source实现新的方法。
  - ②当不重新编译时，如果程序调用接口新增加的方法，可以避免出现`AbstractMethodError`。
- 解决 default method 冲突规则：
  - ①类优先
  - ②接口冲突，需要在类中重写该方法。
- 接口不能实例化，却能声明接口的变量。接口变量必须引用实现了接口的类对象。
- 接口可以继承多个接口。
- `tagging interface`不包含任何方法，它的唯一作用是允许在类型查询中使用instanceof。

#### 2.在非抽象类中实现接口

- ①implements
- ②需要实现接口的==所有==非默认方法。

> 抽象类可以不实现所有的非默认方法

#### 3.接口与抽象类

两者有些类似，但是Java中类只支持单继承，却可以实现多个接口。

- [深入理解Java的接口和抽象类](http://www.cnblogs.com/dolphin0520/p/3811437.html) 抽象类是对一种事物的抽象，即对类抽象，而接口是对行为的抽象。抽象类作为超类规定了类具有的最基本的属性和行为，而子类具有的额外特性，可以通过实现接口来实现。但是如果把子类的每一个额为特性都通过接口实现，而接口只服务于这个类，那么无需将这些特性从子类中剥离出来。设计成接口的初衷是为了代码的复用，当有多个类具有一个相同特性时，可以将这个特性抽象成接口。而这又延伸出了另一个问题，可以为这些具有相同特性的类设计一个超类插入到继承层次中去。抽象成接口还是超类，哪个更好？