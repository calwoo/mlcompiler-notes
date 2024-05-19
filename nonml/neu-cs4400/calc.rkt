#lang plait

(define-type Exp
  [num (n : Number)]
  [plus (left : Exp) (right : Exp)])


(parse : (S-Exp -> Exp))
(define (parse s)
  (cond
    [(s-exp-number? s) (num (s-exp->number s))]
    [(s-exp-list? s)
     (let ([l (s-exp->list s)])
       (cond
         [(empty? l) (error 'parse "empty list")]
         [(symbol=? '+ (s-exp->symbol (first l)))
          (plus (parse (second l))
                (parse (third l)))]
         [else (error 'parse "unrecognized symbol")]))]))

(test (parse `1) (num 1))
(test (parse `{+ 1 2}) (plus (num 1) (num 2)))
(test/exn (parse `{1 + 2}) "")

 
(calc : (Exp -> Number))
(define (calc e)
  (type-case Exp e
    [(num n) n]
    [(plus e1 e2)
       (+ (calc e1) (calc e2))]))


(calc (num 10))
(calc (plus (num 1) (num 2)))
(calc (plus (plus (num 1) (num 2)) (num 3)))