# Chapter 4 Classes, objects, interfaces

## Question

1. -81- Therefore, if you need to implement such an interface in a Java class, you have to define your own implementations of all methods, including those that have method bodies in Kotlin.看不太懂
2. -83- Open classes and smart casts 看不懂
3. -86- Visibility modifiers from Java  除了public，其它三个modifiers在Java中的可见范围和在Kotlin中都不完全相同，为什么SIDEBAR这段话中并没有指出这一点？
4. module指什么？
5. -85- Kotlin forbids you to **reference** the **less-visible** type TalkativeButton (internal, in this case) from the public function giveSpeech.  
6. -87- nested classes 是用来干什么的？
7. -94- SIDEBAR Alternatives to private constructors 看不懂
8. -97- The interface doesn’t specify whether the value should be stored in a backing field or obtained through a getter. backing field是什么东西？
9. -99- Note that you can redefine only one of the accessors for a mutable property. 不明白这句话想要表达什么

## Concept

1. -82- fragile base class problem 
2. -91- primary constructor 
3. -91- secondary constructor 
4. -91- initializer block 
5. -99- backing field
6. -106- decorator pattern 装饰器模式
7. -108- companion object
8. -108- object expression
9. -108- object declaration
10. -108- companion objects

## Notification

1. -84- internal
2. -102- SIDEBAR  == for equality 
3. -102- "Any" is the analogue of java.lang.Object: a superclass of all classes in Kotlin.  

## Content

## 4.1 Defining class hierarchy

#### 4.4.1 Interfaces in Kotlin: methods with default implementations

-79- Kotlin interfaces are similar to those of Java 8.

-79- Kotlin uses the **colon** after the class name to replace both the **extends and implements** implements keywords used in Java. 

-79- Unlike Java, using the override modifier is **mandatory** in Kotlin.  

-80- You must provide **an explicit implementation** if **more than one implementation** for the same member is inherited. 

-81- Therefore, if you need to implement such an interface in a Java class, you have to define your own implementations of all methods, including those that have method bodies in Kotlin.

#### 4.1.2 Open, final, and abstract modifiers: final by default

-82- Whereas Java’s classes and methods are **open** by default, Kotlin’s are **final** by default .

-83- Note that if you override a member of a base class or interface, the overriding member will also be open by default. 

-83- Abstract members(classes,funcions) are always open, so you **don’t** need to use **an explicit open** modifier.  

-84- in interfaces you don’t use final, open, or abstract. 

- final
- open
- abstract
- override

#### 4.1.3 Visibility modifiers: public by default

-84- The default visibility in Java, package-private, **isn’t present in Kotlin**. Kotlin uses packages only as a way of organizing code in namespaces; it doesn’t use them for visibility control.

-85- This is a case of a general rule that requires all types used in the list of base types and type parameters of a class, or the signature of a method, to be **as visible as** the class or method itself. 

-85- Note the difference in behavior for the protected modifier in Java and in Kotlin. In Java, you can access a protected member from **the same package**, but Kotlin doesn’t allow that. In Kotlin, visibility rules are simple, and a protected member is **only visible in the class and its subclasses**.  	

-86- **Extension functions** of a class don’t get access to its **private or protected** members. 

| modifier        | class member                          | top-level declaration |
| --------------- | ------------------------------------- | --------------------- |
| public(default) | visible everywhere                    | visible everywhere    |
| internal        | visible in  a module                  | visible in a  module  |
| protected       | visible in the classes and subclasses | --不适用于顶层声明            |
| private         | visible in the class                  | visible in the file   |

-86- Visibility modifiers from Java 

- Thus an internal modifier becomes public in the bytecode. 
- ​

#### 4.1.4 Inner and nested classes: nested by default

-86- Kotlin nested classes don’t have access to the outer class instance.

-88- A nested class in Kotlin with no explicit modifiers is the same as a static nested class in Java. 

| class A declared within another class B  | in Java        | in Kotlin     |
| ---------------------------------------- | -------------- | ------------- |
| nested class(doesn't store a reference to the outer class B) | static class A | class A       |
| inner class(store a reference to the outer class B) | class A        | inner class A |

####  4.1.5 Sealed classes: defining restricted class hierarchies

-89- You mark a superclass with the `sealed` modifier, and that restricts the possibility of creating subclasses.  

- All the direct subclasses must **be nested** in the superclass: 

-90- Note that the `sealed` modifier **implies that the class is open**; you don’t need an explicit open modifier. 

-90- when you add a new subclass, the when expression returning a value fails to compile, which points you to the code that must be changed .

### 4.2 Declaring a class with nontrivial constructors or properties

#### 4.2.1 Initializing classes: primary constructor and initializer blocks

- `constructor` keyword begins the declaration of a primary or secondary constructor.  
- `init` keyword introduces an `initializer block`. 

primary constructor的简化过程：

1. you don’t need to place the initialization code in the initializer block,because it can be combined with the declaration of the nickname property. 
2. You can also omit the constructor keyword if there are no annotations or visibility modifiers on the primary constructor.  
3. If the property is initialized by the corresponding constructor parameter,the code can be simplified by adding the val keyword before the parameter.  

#### 4.2.2 Secondary constructors: initializing the superclass in different ways

-94- The majority of situations where you’d need overloaded constructors in Java are **covered by Kotlin’s support for default parameter values**. 

-95- The most common one comes up when you need to **extend a framework class** that **provides multiple constructors** that initialize the class in different ways.  

-96- There’s another possible case: when you have multiple ways to create instances of your class, with different parameter lists.  

-96- If the class has **no primary constructor**, then **each secondary constructor** has to **initialize the base class** or **delegate to another constructor** that does so.  

#### 4.2.3 Implementing properties declared in interfaces

-97- The interface doesn’t specify whether the value should **be stored in a backing field** or **obtained through a getter.** Therefore, **the interface itself doesn’t contain any state**, and only classes implementing the interface may store the value if they need to. 

-98- In addition to **abstract property declarations**, an interface can **contain properties with getters and setters,** as long as they **don’t reference a backing field.** 

#### 4.2.4 Accessing a backing field from a getter or setter(不明白这节的知识点有什么用)

- `field` to access the value of the backing field.  

-99- Note that you can redefine **only one of the accessors** for a mutable property. 

-99- The compiler will **generate the backing field** for the property if you either reference it explicitly or use the default accessor implementation. 

-99- If you provide custom accessor implementations that don’t use field (for the getter if it’s val and for both accessors if it’s a mutable property), the **backing field won’t be present.** 

#### 4.2.5 Changing accessor visibility

-99- The accessor’s visibility by default is the same as the property’s.  

- putting a visibility modifier before the get or set keyword.  

### 4.3 Data classes and class delegation: compiler-generated methods

#### 4.3.1 Universal object methods

-102- SIDEBAR  == for equality 

#### 4.3.2 Data classes: autogenerated implementations of universal methods

-104-Note that properties that **aren’t declared in the primary constructor don’t take part in** the equality checks and hashcode calculation.  

#### 4.3.3 Class delegation: using the "by" keyword(看不懂可以用来做什么)

## 4.4 Declaring a class and creating an instance, combined, with the object keyword 

#### 4.4.1 Object declarations: singletons made easy

