# 再现 Java

## OverVIew

撰写本文的目的是通过分析Java的语法来还原Java的设计思想，并彻底分解Java的结构，形成若干条规则，在这些规则的约束下，将Java转化为一个数学模型。Java是从多个模块延伸出来的，模块与模块之间又会根据规则发生“碰撞”。

[Description of Java Conceptual Diagram](http://docs.oracle.com/javase/8/docs/)

##一、疑问

- [x] - 3.3.1中，对象是实例的父集，在实际使用中将实例称为对象是否合适？这个问题转化为数学集合论中父集和子集的问题。
        - 不合适。在[内部类](http://www.cnblogs.com/dolphin0520/p/3811445.html)中，局部内部类是定义在一个方法或者作用域中，而成员内部类是定义在类的内部（与数据域同一等级），显然局部内部类也可以认为是定义在类的内部，但是这样定义局部内部类的话就会和方法内部类混淆，所以为了减少歧义与谬误，必须精确地说明，即父集不能越权去替代子集。

> **注意：在Java中`继承(inheritance)`概念里的`超类(superclass)`和`子类(subclass)`，与集合论中`子集(subset)`和`父集(superset)`的关系正好相反，应该称之为`基类(base class)`和`派生类(derived class)`更合适（C++ 中的叫法），这样就能和集合论相协调。**==我想错了，集合的关系是根据集合A的元素是否包含于集合B，而不是集合A的元素的特性比集合B的元素多，所以`超类(superclass)`对应`superset`，`subclass`对应`subset`==

## 二 、Java的特性

- 由1可得唯一性、确定性

## 三 、Java的具体实现

1. 为了能唯一确定所要指定的文件，以及对文件(所具有的功能)进行分类，于是有了`包(package)`的概念。为了避免重名，使用倒叙域名作为包结构。为了简化使用指定文件时需要输入的字符数量，而引入了`Import`的简化方式（[详见](http://soft.chinabyte.com/database/361/11365861.shtml)）

2. Java程序的基本单元：`类(Class)`。类中可以包含`数据域(data fileds)`、`方法(methods)`、[内部类](http://www.cnblogs.com/dolphin0520/p/3811445.html)、代码块。数据域又分为`类域(class fileds)`、`实例域(instance fileds)`。又根据方法操作的数据域的类型，把方法分为`类方法(class methods)`、`实例方法(instance methods)`。

   - 在面向对象的概念当中，类是既包括数据又包括作用于数据的一组操作的封装体。类的数据称为数据域，类对数据的操作称为方法。数据域反映类的状态和特征，方法反映类的行为和能力。类的数据域和方法统称为类的成员。
   - 对于一个Java源代码文件，如果存在public类的话，只能有一个public类，且此时源代码文件的名称必须和public类的名称完全相同，另外，如果还存在其他类，这些类在包外是不可见的，即使是这个包的子包里也是不可见的，只有该源文件处在同一深度的类才可见。如果源代码文件没有public类，则源代码文件的名称可以随意命名。
   - data fileds 与 variables 的区别。
   - 变量的作用域。Blocks define the scope of variables.
   - 变量的初始化。The default value of a data field is **null** for a `reference type`, **0** for a `numeric type`,**false** for a `boolean type`, and **\u0000** for a `char type`. However, Java assigns **no default value**  to a `local variable` inside a method.  
   - Relationships between classes.

3. Java程序实际操作中的基本单元是`对象(Object)`。类是对象的抽象化，对象是类的实例化。 **对象（实例）是在类的基础上填充了数据。**

   - 对象代表在现实世界中可以明确标识的一个实体,即一切皆对象。对象应该是`实例(instance)`的父集，实例是对象，对象不一定是实例。

   - 对象和实例在很多情况下是混用的，在Java中对象是类的实例。对象是动态的，拥有生命周期，都会经历一个从创建、运行到消亡的过程。对象与类的关系就像变量与数据类型一样。

   - 匿名对象（anonymous object）只使用一次就被销毁了。

   - 创建对象有2种方式，一种是使用构造器，另外一种是使用`静态工厂方法(factory method)`。

     - [静态工厂方法](http://www.cnblogs.com/allenzhaox/archive/2012/08/14/3201818.html)
     - [Effective Java 读书笔记（一）：使用静态工厂方法代替构造器](http://www.cnblogs.com/honoka/p/4858416.html)

4. 类、对象以及两者内部的初始化块、构造器在JVM中的初始化顺序

5. 访问控制权限

   - 类：public、默认访问权限（包访问）

   - 类的成员和方法：public、protected、默认访问权限、private

   - 详细分析：[浅析Java中的访问权限控制](http://www.cnblogs.com/dolphin0520/p/3734915.html)

   - > **注意：因为成员和方法从属于类，所以类的访问控制修饰符是具有更高的优先级。只有存在类的实例才会进一步看实例的访问控制修饰符。当类的实例都无法创建时，即使方法和变量是public也不可以访问，因为根本就不存在相应的变量和方法** 

6. 程序的加载过程以及顺序

   1. JVM决定
      - 先载入class文件，当发现载入的文件某一行代码处需要调用到其它class文件，则会暂停当前运行的代码转而去加载需要调用的文件。
   2. 程序员决定——static
      1. static的成员变量和代码块是在加载class文件时就会运行。
      2. [java中静态代码块的用法 static用法详解 类的加载顺序](http://www.cnblogs.com/guanghuiqq/archive/2012/10/09/2716898.html)
      3. [Java中的static关键字解析](http://www.cnblogs.com/dolphin0520/p/3799052.html)
      4. [如何理解《Java编程思想》描述的“即使没有显式地使用static关键字，构造器实际上也是静态方法”?](http://zhihu.com/question/35860619/answer/64802279)

7. 继承(Inheritance)

   - override
   - overload
   - abstract class 

8. 运算符

9. Blocks

   - Blocks define the scope of variables.

10. `this`的两种用法：

  - The keyword this refers to the implicit parameter of a method.
  - If the **first** statement of a constructor has the form this(. . .), then the constructor calls another constructor of the same class. 

11. 接口

12. 异常处理



## 四、Java编程的思想

1. encapsulation
   - 数据域使用private修饰的好处：-4.3.8
   - 数据域通过accessor method 、mutator method 操作的好处： -4.3.8
   - ​