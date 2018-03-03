# Chapter 3 Defining and calling functions

## Question

1. -64- `fun click() = println("Button clicked")` 函数体不是表达式，也可以用这种形式？
2. -66- The getter must always be defined, because there’s no backing field and therefore no default getter implementation. 什么是backing field？
3. -68- Technically, this feature is called using a spread operator, in practice it’s as simple as putting the character before the corresponding argument: 怎么用的？

## Concept

1. -54- named arguments
2. -55- default parameter values 
3. -60- extension function
4. -60- receiver type
5. -61- receiver object
6. -68- infix call
7. -69- destructuring declaration

## Notification

1. -57- default parameter values with Java

## Content

### 3.1 Creating collections in Kotlin

- set
  - val set=setof(1,7,9)
- list
  - val list=listof(1,7,9)
- map
  - val map=mapof(1 to "one", 7 to "seven", 9 to "nine")

\> > > println(set.javaClass)
 class java.util.HashSet
\>>> println(list.javaClass)
 class java.util.ArrayList
\>>> println(map.javaClass)
 class java.util.HashMap 

> 1. -52-javaClass is Kotlin’s equivalent of Java’s getClass() 
> 2. -52-Kotlin uses the standard Java collection classes.Because using the standard Java collection classes makes it easier to interact with Java code.

### 3.2 Making functions easier to call 

joinToString方法

#### 3.2.1 Named arguments



>1. -55- If you specify the name of an argument in a call, you should **also specify the names for all the arguments after that**, to avoid confusion .
>2. Unfortunately you **can’t** use named arguments **when calling methods written in Java**, including methods from the JDK and the Android framework. 

#### 3.2.2 Default parameter values

> 1. -56- When using the regular call syntax, you can **omit only trailing arguments**. If you **use named arguments**, you can omit some arguments from the middle of the list and **specify only the ones you need**.
> 2. -56-Note that the default values of the parameters are encoded in the function being called.
> 3. -57- default parameter values with Java

#### 3.2.3 Top-level functions and properties: getting rid of static utility classes

- -58- All top-level functions in the file are compiled to static methods of that class.  
- -60- The value of a top-level property will be stored in a static field 

> 1. -59- Changing the file class name.
> 2. Exposing a constant to Java code as a `public static final` field, to make its usage more natural, you can mark it with the `const` modifier .

### 3.3 Extension functions and properties: adding methods to other people's classes

- the target of designing extension function
  - integrate Kotlin with existing code,without having to rewrite them.
- syntax
  - fun className.

> -61- In the extension function, you can **directly access** the methods and properties of the class you’re extending, **as in methods defined in the class itself**. Note that extension functions don’t allow you to break encapsulation. Unlike methods defined in the class,**extension functions don’t have access to private or protected members of the class** .

#### 3.3.1 Imports and extension functions

> 1. -62- For extension functions, the syntax requires you to **use the short name**, so the `as` keyword in an import statement is **the only way** to resolve the conflict. 

#### 3.3.2 Calling extension functions from Java

> 1. -62- This extension function is declared as a top-level function.

#### 3.3.3 Utility functions as extensions

#### 3.3.4 No overriding for extension functions

-64- you can’t override an extension function.  

-65- For extension functions, the function that’s called depends on **the static type of the variable being declared**, **not on the runtime type** of the value stored in that variable. 

-65- To use extension functions in Java, the receiver is as the first argument. 

-65- If the class has a member function with the same signature as an extension function, the member function always **takes precedence**.

#### 3.3.4 Extension properties

-66- The getter **must** always be defined, because there’s **no backing field** and therefore no default getter implementation. 

-66- Note that when you need to access an extension property from Java, you should invoke its getter explicitly: StringUtilKt.getLastChar("Java"). 

### 3.4 Working with collections: varargs, infix calls, and library support

#### 3.4.1 Extending the Java Collections API

#### 3.4.2 Varargs: functions that accept an arbitrary number of arguments

-68- Technically, this feature is called using a spread operator, in practice it’s as simple as putting the character before the corresponding argument: 

#### 3.4.3 Infix calls and destructuring declarations: Working with pairs

```kotlin
1 to "one" //to function: 1 to "one" -> Pair(1,"one")
val (number,name)= 1 to "one"//destructuring declaration: Pair(1,"one") -> (number,name)
```

### 3.5 Working with Strings and regular expressions

#### 3.5.1 Splitting strings

`split()`is a extension method which has two kind of parameters,string delimiters or regular expressions.

#### 3.5.2 Regular expressions and triple-quoted strings

#### 3.5.2 Multiline triple-quoted strings

### 3.6 Local functions and properties: making your code tidy

Don’t Repeat Yourself(DRY) 	

-74- you can **nest** the functions you’ve extracted in the containing function. This way, you have the structure you need without any extra syntactic overhead. 

-75- it’s entirely **unnecessary**, because local functions have access to all parameters and variables of **the enclosing function**.  

### 3.7 Summary

