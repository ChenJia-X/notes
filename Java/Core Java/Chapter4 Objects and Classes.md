# Chapter4 Objects and Classes

## Questions

1. P111 4.3.7基于类的访问权限。
2. p111 4.3.8私有方法。
3. P115 4.4.5main方法。为什么要对类进行单元测试？
4. p128 4.6.7初始化块。什么是“类的构造器行为依赖于数据域声明的顺序”？
5. P131 4.7包。什么是嵌套？
6. P137 4.8类路径。看不太懂。
7. P140 4.9文档注释。内容太多，当前没什么用，就大概了解下。

## Concepts

1. mutator method -4.2.3
2. accessor method -4.2.3
3. implicit parameter -4.3.5
4. explicit parameter -4.3.5
5. factory method -4.4.4
6. argument 实参（有待进一步确定，两者经常被人混用）
7. parameter 形参（有待进一步确定，两者经常被人混用）
8. call by value -4.5
9. call by reference -4.5    **注意：方法接收的是调用者提供的变量地址，而不是变量所引用的对象地址。** 
10. overloading -4.6.1
11. overloading resolution -4.6.1
12. signature of the method -4.6.1
13. -4.6.8- finalize

## Notifications

1. The key to making `encapsulation` work is to have methods **never** directly access instance fields in a class other than their own.
2. In every mothed,keyword `this` refers to the implicit parameter. -4.3.5
3. Be careful **not** to write `accessor methods` that return **references to mutable objects** . -4.3.6
4. Some programmers (and unfortunately even some book authors) claim that **Java use call by reference for objects. ** `That is false`. 注意`call by referece `的定义。-4.5
5. -4.6.6- `this`的两种用法：
   - The keyword this refers to the implicit parameter of a method.
   - If the **first** statement of a constructor has the form this(. . .), then the constructor calls another constructor of the same class. 
6. -4.6.7- 初始化块在构造器之前被初始化。

