# Chapter3 Fundamental Programming Structures in Java

## Concepts

1. access modifier-3.1
2. primitive type-3.3
3. reference type
4. class constant -3.4.2 
5. casts-3.5.3
6. argument 实参（有待进一步确定，两者经常被人混用）
7. parameter 形参（有待进一步确定，两者经常被人混用）
8. format specifiers -3.7.2
9. conversion character -3.7.2
10. blocks -3.8.1

## Notifications

1. Java is case sensitive.

2. Naming convention:CamelCase

3. Java SE 5.0 brought back the venerable `printf()` method form the C library for formatting output.**Your can't use`print()`or`println()`method to format output.** 

4. The default value of a data field is **null** for a `reference type`, **0** for a `numeric type`,**false** for a `boolean type`, and **\u0000** for a `char type`. However, Java assigns **no default value**  to a `local variable` inside a method.  

   - After you declare a variable, you must **explicitly initialize** it by means of an assignment statement—you can never use the value of an uninitialized variable. 

5. -3.4.2- `final`修饰变量时的作用是使变量中存储的值不变。如果是`reference variables`，因为变量存储的是引用对象的地址，所以引用的对象不能变，而对象的内容可以改变。

6. -3.5.4 注释- ` int x+=3.5`，在编译的时候实际执行了2条规则，先将x转化为float类型，再plus with3.5，然后将相加后的值cast为int类型，最后赋值给x。

7. Java uses exactly one mode of passing arguments to method: `pass-by-value`.

   > - When passing an argument of a `primitive data type`, the **value** of the argument is passed. 
   > - When passing an argument of a `reference type`, the **reference** of the object is passed. 
   >
   > Pass-by-value on references can be best described semantically as `pass-by-sharing`.
   >
   > 向方法中传递实参实际上就是一个赋值的过程，因为Java方法中会生成一个形参接收实参传来的值。Primitive type passes the value,but reference type passes the reference of the object.所以primitive type arguments不会因为方法中的操作而改变，而reference type arguments会因为方法中的操作而改变。

8. You can avoid the Math prefix for the mathematical methods and constants by adding the following line to the top of your source file:`import static java.lang.Math.*`; 

9. `=`比较的是变量存储的值，所以如果对`reference variables`使用，比较的是两个引用变量是否引用同一个对象。而`equals()`比较的是变量所引用的对象的值。


## Concert contents

### 3.3 Data Types

#### 3.3.1 Integer Types

- Starting with Java SE 7, you can write numbers in binary, with a prefix `0b or 0B`.

  - For example, 0b1001 is 9.

  - 0b以及0x默认都是int长度//待验证

    - > 验证代码：
      >
      > ```java
      > System.out.println(0xffffffff);//-1 int类型的长度
      > System.out.println(0b1000_0000_0000_0000_0000_0000_0000_0000);//-2147483648
      > ```

-  Also starting with Java SE 7, you can add underscores to number literals.

  - such as `1_000_000` (or `0b1111_0100_0010_0100_0000`) to denote one million

- Note that Java does not have any `unsigned` versions of the int, long, short, or byte types. 



### 3.5 Operators

#### 3.5.2 Conversions between Numeric Types

- 两个不同类型的数值进行运算时，需要进行类型转换：
  - If either of the operands is of type `double`, the other one will be converted to a double.

  - Otherwise, if either of the operands is of type `float`, the other one will be converted to a float.

  - Otherwise, if either of the operands is of type `long`, the other one will be converted to a long.

  - Otherwise, both operands will be converted to an `int` .

    - > 如果一个byte和一个short进行运算，那么两者都会被转化为int。
      >
      > 验证代码：`System.out.println((byte)1+(short)32767);//32768，溢出了short的上限`

#### 3.5.3 Cats

- 高精度的numeric type转换成低精度的类型，会丢失精度。

  - ```java
    System.out.println((byte)128);//-128。128是int型，强制转化成byte，会把高位的信息全部丢弃，所以只剩1000 0000，就变成了-128。
    System.out.println((byte)129);//-127。同理，丢失高位，只剩1000 0001，即-127
    ```

### 3.10 Arrays

1. declare an array
2. initialize an array
   - If  you don't explicitly initialize an array,Java will assign default value to the array.
   - The array length can be a **variable**:`new int[n]` creates an array of length n.
   - Once you create an array,you **can't change it's size**.You can create an **array list**  to adapt the need of **changing size frequently**.
3. access elements in an array
4. print an array:`System.out.println(Arrays.toString(the array)`