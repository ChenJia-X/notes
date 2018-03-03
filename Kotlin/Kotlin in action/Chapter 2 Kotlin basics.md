# Chapter 2 Kotlin basics

## Question

1. -P128- Capturing a mutable variable: implementation details  看不懂
2. -P128- because the onClick handler will be called after the function returns.  为什么？
3. var对于基本类型是线程安全，对于引用类型是线程安全吗？

## Concept

1. -23- statement、expression
2. -23- expression body、block body
3. -24- type inference
4. -28- value objects
5. -33- soft keywords
6. -39- is
7. -39- smart cast
8. -42- ranges
9. -42- progression

## Notification

1. -23- In Java, all control structures are statements. In Kotlin, most control structures, except for the loops (for, do, and do/while) are expressions. 
2. -48- The biggest difference from Java is that the throws clause isn’t present in the code 

## Content

### 2.1 Basics elements：functions and variables

#### 2.1.2 function 

- syntax
  - expression body function
    - This style is used not only for trivial one-line functions, but also for functions that evaluate a single,more complex expression, such as if, when, or try.  
  - block body function
- type inference

> 1. -23- In Java, all control structures are statements. In Kotlin, most control structures, **except for the loops** (for, do, and do/while) are expressions. 
> 2. -24- Note that omitting the return type is allowed only for functions with **an expression body**.  For functions **with a block body** that return a value, you have to specify the return type and **write the return statements explicitly**.  

#### 2.1.3 variable

- type inference
- mutable and immutable variables
  - 在IDE中为了区分val和var，会在var变量下划一条紫色横线。

> 1. -25- Note that, even though a val reference is itself immutable and cannot be changed, the object that it points to may be mutable. 

#### 2.1.4 String templates

- syntax
  - variable name
  - complex expressions
    - nest double quotes

> -50- String templates help you avoid noisy string concatenation. **Prefix a variable name with**`$`or **surround an expression with** `${ }` to have its value injected into the string.

### 2.2 Classes and properties

#### 2.2.1 Properties

- val、var
- The way to access value objects which defined in Java/Kotlin from Java/Kotlin.

> 1. -29- For **Boolean properties**, a special rule for getter naming applies: if the property name starts with is, no additional prefix for the getter is added. Thus, from Java, you call isMarried(). 

#### 2.2.2 Custom accessors

> 1. -30- The property isSquare doesn’t need a field to store its value. It only has a custom getter with the implementation provided. The value is computed every time the property is accessed. -30- The property isSquare doesn’t need a field to store its value. It only has a custom getter with the implementation provided. The value is computed every time the property is accessed. 

#### 2.2.4 Kotlin source code layout: directories and packages

> 1. -31- Kotlin doesn’t make a distinction between importing **classes** and **methods**, and it allows you to import any kind of declaration using the import keyword.  
> 2. -32- This `star import(.*)` will make visible not only classes defined in the package, but also top-level functions. 
> 3. -32- In Kotlin, you can put multiple classes in the same file and choose any name for that file.  

### 2.3 Representing and handling choices: enums and 'when' 

#### 2.3.1 Declaring enum classes 

- syntax
  - enum class enumName(properties){enum constant list==;== function}

> -33- The only place in the Kotlin syntax where you’re required to use semicolons：

#### 2.3.2 Using 'when' to deal with enum classes

> 1. -34- you don’t need to write break statements in each branch.If a match is successful, only the corresponding branch is executed.
> 2. -34- You can also combine multiple values in the same branch if you separate them with commas: 
> 3. -34- For specifying the Color enum class name,You can simplify the code by importing the constant values: 

#### 2.3.3 Using 'when' with arbitrary objects

#### 2.3.4 Using 'when' without an argument

If no argument is supplied for the when expression, the branch condition is any boolean expression.  

如果不提供参数，所有的分支条件都是简单的布尔表达式，而当一个分支的条件为真时则执行该分支：

#### 2.3.5 Smart casts:combining type checks and casts

-39- The IDE highlights smart casts with green color.

-39- The smart cast works only if a variable couldn’t hqave changed after the is check. 

#### 2.3.6 Refactoring：replacing 'if' with 'when'

-40- In Kotlin, there is no ternary operator, because, unlike in Java, the `if` expression returns a value. That means you can rewrite the eval function to use the expression-body syntax, removing the `return` statement .

#### 2.3.7 Blocks as branches of 'if' and 'when'

-41- In `if`and`when`,the last expression in the block is the result. 

### 2.4 Iterating over thing: 'while' and 'for' loops

#### 2.4.1 The while loop

The usage of while and do-while doesn't differ form the corresponding loops in Java.

#### 2.4.2 Iterating over numbers:ranges and progressions

- ranges [区间](https://www.kotlincn.net/docs/reference/ranges.html#区间)
  - syntax
    - `..` operator 
      - val oneToTen=1..10
      - -44- The `..` syntax to create a range works not only for numbers, but also for **characters**. 
    - `downTo`
      - val tenToOne=10 downTo 1
    - `step`
      - val oneToTen=1..10 step 2
  - -42- Ranges in Kotlin are closed or inclusive. You can use `until` to express an open range.
    - `until`
      - val oneToNine=1 until 10
  - -46- Ranges aren’t restricted to characters, either. If you have any class that **supports comparing instances** (by implementing the java.lang.Comparable interface), you can create ranges of objects of that type.  
- progression
  - -42- A range in which the loop can iterate over all the values is called a progression.	

#### 2.4.3 Iterating over maps

-44- The `..` syntax to create a range works not only for numbers, but also for **characters**. 

-44- The example shows that the for loop allows you to **unpack an element of a collection you’re iterating over** (in this case, a collection of key/value pairs in the map). 

-45- Another nice trick used in this example is **the shorthand syntax for getting and updating the values of a map by key**. Instead of calling get() and put(), you can use `map[key]` to read values and `map[key] = value` to set them. 

#### 2.4.5 Using an 'in' check

-46- But this logic is concisely hidden in the implementation of the range classes in the standard library.一种优秀的编程思想

-46- Ranges aren’t restricted to characters, either. If you have any class that **supports comparing instances** (by implementing the java.lang.Comparable interface), you can create ranges of objects of that type.  

> `in` check works with ranges,collections and maps.

### 2.5 Exceptions in Kotlin

-47- Unlike in Java, in Kotlin the `throw` construct is an expression and can be used as a part of other expressions: 

#### 2.5.1 'try' ,'catch','finally'

-48- The biggest difference from Java is that the throws clause isn’t present in the code.

-48- Kotlin doesn’t differentiate between checked and unchecked exceptions.  

-48- This design decision is based on the practice of using checked exceptions in Java. Experience has shown that the Java rules often require a lot of meaningless code to rethrow or ignore exceptions, and the rules don’t consistently protect you from the errors that can happen. 

#### 2.5.2 'try' as an exception

-49- the try keyword in Kotlin, just like if and when, introduces an expression, and you can assign its value to a variable. 

### 2.6 Summary