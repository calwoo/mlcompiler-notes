; ModuleID = "hello"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"_print_int"(i32 %".1")

define i32 @"hello"()
{
entry:
  %"x" = alloca i32
  %"y" = alloca i32
  store i32 4, i32* %"x"
  store i32 5, i32* %"y"
  %".4" = load i32, i32* %"x"
  %".5" = load i32, i32* %"y"
  %".6" = mul i32 %".4", %".4"
  %".7" = mul i32 %".5", %".5"
  %".8" = add i32 %".6", %".7"
  %"d" = alloca i32
  store i32 %".8", i32* %"d"
  %".10" = load i32, i32* %"d"
  call void @"_print_int"(i32 %".10")
  ret i32 42
}

define double @"dsquared"(double %".1", double %".2")
{
entry:
  %".4" = fmul double %".1", %".1"
  %".5" = fmul double %".2", %".2"
  %".6" = fadd double %".4", %".5"
  ret double %".6"
}

