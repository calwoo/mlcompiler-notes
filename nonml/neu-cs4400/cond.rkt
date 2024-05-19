#lang plait

(define-type Value
  [vbool (v : Boolean)]
  [vnum (n : Number)])

(define-type Expr
  [num (n : Number)]
  [bool (b : Boolean)]
  [plus (l : Expr) (r : Expr)]
  [cnd (guard : Expr) (thn: Expr) (els: Expr)])

(define (value->num v)
  (type-case Value v
    [(vbool b) (error 'value "invalid valid")]
    [(vnum n) n]))

(define (value->bool v)
  (type-case Value v
    [(vnum n) (error 'value "invalid value")]
    [(vbool b) b]))

(define (add v1 v2)
  (+ (value->num v1) (value->num v2)))

(calc : (Exp -> Value))
(define (calc e)
  (type-case Expr e
    [(num n) (vnum n)]
    [(bool b) (vbool b)]
    [(plus l r) (vnum (add (calc l) (calc r)))]
    [(cnd test thn els) (if (value->bool (calc test))
                            (calc thn)
                            (calc els))]))