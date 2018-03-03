# Other

## [Type Checks and Casts](http://kotlinlang.org/docs/reference/typecasts.html#type-checks-and-casts)

1. `is`and`!is` Operator
2. Smart Casts
   - Smart Casts will do work after Type Checks for **immutable values.**
   - If the complier cannot guarantee that the variable can't change between check and the usage, Smart Casts won't work.
3. "Unsafe" cast operator `as`
4. "Safe"(nullable) cast operator `as?`

## [Null Safety](https://kotlinlang.org/docs/reference/null-safety.html#null-safety)

1. **Nullable variables** must declare explicitly with `?`.
2. If you want to access a property or function of a **nullable variable**,you can use these ways below:
   -  Checking for null in conditions
   - Safe Calls `?.`
     - Elvis Operator `?:` 
   - The `!!` Operator
3. Safe Casts
4. Collections of Nullable Type
   1. using `filterNotNull()`
   2. 111 81 52 121 111 7 32 