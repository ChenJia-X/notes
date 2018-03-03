# Chapter5 Inheritance

## Questions

1. 为什么要使用多态性？
2. -5.1.5警告- 数组如何在内存中实现拷贝的过程？为什么对staff[0]的赋值会影响到managers[0]？
   -  解答：P81
3. -5.1.6- 对象调用方法的过程。
4. -5.3.2- 没怎么看懂

## Concepts

1. polymorphism -5.1.3
2. dynamic binding -5.1.3
3. inheritance hierarchy -5.1.4
4. inheritance chain -5.1.4
5. substitution principle -5.1.5
6. overloading resolution -5.1.6
7. static binding -5.1.6
8. dynamic binding -5.1.6
9. -5.1.6- method table
10. -5.1.7- inlining
11. -5.3- type parameter
12. -5.3- generic class
13. -5.4- wrapper
14. -5.4- autoboxing
15. -5.7- reflective
16. -5.7.2- handler

## Notifications

1. - Recall that the `this` keyword has two meanings: ①to denote a reference to the implicit parameter and ②to call another constructor of the same class.
   - Likewise, the `super` keyword has two meanings:① to invoke a superclass method and ②to invoke a superclass constructor. 
   - When used to invoke constructors, the this and super keywords are closely related.The constructor calls can only occur as the **first** statement in another constructor. The constructor parameters are either passed to another constructor of the same class (this) or a constructor of the superclass (super) 。-5.1.3
2. -5.1.5- 使用多态后的对象变量，该对象变量**无法**调用子类有而超类无的fields或method。ye是 dynamic binding 。②如果是dynamic binding，虚拟机会从与 implicit parameter 所引用对象的实际类型最合适的那个类的method table中寻找符合调用方法签名的方法。-5.1.6
3. 0理解方法调用：虚拟机会为每一个类都创建一个method table。①先判断调用的方法是 `static binding` 还是 `dynamic binding` 。②如果是dynamic binding，虚拟机会从与 `implicit parameter ` 所引用对象的实际类型最合适的那个类的method table中寻找符合调用方法签名的方法。-5.1.6
4. When you override a method, the subclass method must be at least as visible as the superclass method.  -5.1.6
5. If a class is declared final, only the methods, not the fields, are automatically final. -5.1.7
6. The rules of casting: -5.1.8
   -  You can cast only within an inheritance hierarchy.
   -  Use `instanceof ` to check before casting from a superclass to a subclass 



## Concrete contents

1. -5.2.2- equals()有3个判断层次，先判断变量值是否相等，再判断参数是否为空，接着判断两者是否是同类，最后判断fields是否相等。

2. -5.3ArrayList- 参数n表示第n个元素
   - add()
   - remove()
   - get()
   - set()
   - size()

3. -5.7- reflective

   - Class
   - Filed
   - Constructor
   - Method
   - Modifier


   - [反射](https://yq.aliyun.com/articles/61588#)
   - [通过案例理解反射](http://www.cnblogs.com/rollenholt/archive/2011/09/02/2163758.html)