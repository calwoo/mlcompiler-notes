#lang plait

(define-type Exp
  [addE (l : Exp) (r : Exp)]
  [appendE (l : Exp) (r : Exp)]
  [numE (n : Number)]
  [iteE (g : Exp) (thn : Exp) (els : Exp)]
  [stringE (s : String)])

(define-type Value
  [numV (n : Number)]
  [stringV (s : String)])

(calc : (Exp -> Value))
(define (calc e)
  (type-case Exp e
    [(numE n) (numV n)]
    [(stringE s) (stringV s)]
    [(addE l r ) (numV (+ (numV-n (calc l)) (numV-n (calc r))))]
    [(iteE g thn els)
     (if (eq? (numV-n (calc g)) 0)
         (calc thn)
         (calc els))]
    [(appendE l r ) (stringV (string-append
                              (stringV-s (calc l))
                              (stringV-s (calc r))))]))

(define-type Type
  [stringT]
  [numT])

(type-of : (Exp -> Type))
(define (type-of e)
  (type-case Exp e
    [(numE n) (numT)]
    [(stringE s) (stringT)]
    [(addE l r)
     (if (and (numT? (type-of l)) (numT? (type-of r)))
         (numT)
         (error 'type-error "tried to add non-numbers"))]
    [(iteE g thn els)
     (let [(t-g (type-of g))
           (t-thn (type-of thn))
           (t-els (type-of els))]
       (if (and (equal? t-g (numT)) (equal? t-thn t-els))
           t-thn
           (error 'type-error "type error in if")))]
    [(appendE l r)
     (if (and (stringT? (type-of l)) (stringT? (type-of r)))
         (stringT)
         (error 'type-error "tried to append non-strings"))]))

; (type-of (addE (numE 10) (stringE "hello")))
(type-of (iteE (numE 0) (stringE "hello") (stringE "world")))
; (type-of (iteE (numE 0) (numE 10) (stringE "world")))