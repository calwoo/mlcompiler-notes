#lang plait


; exercise 1
(define-type ExtendedNumValue
  [v-num (n : Number)]
  [v-infty])

(define-type Exp
  [num (n : ExtendedNumValue)]
  [plus (left : Exp) (right : Exp)])

(parse : (S-Exp -> Exp))
(define (parse s)
  (cond
    [(s-exp-symbol? s)
     (if (symbol=? (s-exp->symbol s) 'infty)
         (num (v-infty))
         (error 'parse "unrecognized symbol"))]
    [(s-exp-number? s) (num (v-num (s-exp->number s)))]
    [(s-exp-list? s)
     (let ([l (s-exp->list s)])
       (cond
         [(empty? l) (error 'parse "empty list")]
         [(symbol=? '+ (s-exp->symbol (first l)))
          (plus (parse (second l))
                (parse (third l)))]
         [else (error 'parse "unrecognized symbol")]))]))

(calc : (Exp -> ExtendedNumValue))
(define (calc e)
  (type-case Exp e
    [(num n) n]
    [(plus l r) (let [(lval (calc l))
                      (rval (calc r))]
                  (if (or (v-infty? lval)
                          (v-infty? rval))
                      (v-infty)
                      (v-num (+ (v-num-n lval) (v-num-n rval)))))]))

(parse `(+ infty 1))
(calc (parse `(+ infty 1)))
(calc (parse `(+ 2 3)))

; exercise 2
(define-type Value
  [numV (n : Number)]
  [boolV (b : Boolean)])

(define-type IteExp
  [numE (n : Number)]
  [boolE (b : Boolean)]
  [plusE (left : IteExp) (right : IteExp)]
  [condE (arms : (Listof (IteExp * IteExp)))])

(define (boolean-decision v)
  (type-case Value v
             [(boolV b) b]
             [else (error 'if "expects conditional to evaluate to a boolean")]))

(define (add v1 v2)
  (type-case Value v1
             [(numV n1)
              (type-case Value v2
                         [(numV n2) (numV (+ n1 n2))]
                         [else (error '+ "expects RHS to be a number")])]
             [else (error '+ "expects LHS to be a number")]))

(define (ite-parse-pairs pairs)
  (type-case (Listof 'a) pairs
    [empty empty]
    [(cons a b)
     (let [(p (s-exp->list a))]
       (cons (pair (ite-parse (first p))
                  (ite-parse (second p)))
       (ite-parse-pairs b)))]))

(define (ite-parse s)
  (cond
    [(s-exp-number? s)
     (numE (s-exp->number s))]
    [(s-exp-boolean? s)
     (boolE (s-exp->boolean s))]
    [(s-exp-list? s)
     (let ([l (s-exp->list s)])
       (cond
         [(empty? l) (error 'parse "empty list")]
         [(symbol=? '+ (s-exp->symbol (first l)))
          (plusE (ite-parse (second l)) (ite-parse (third l)))]
         [(symbol=? 'cond (s-exp->symbol (first l)))
          (condE (ite-parse-pairs (rest l)))]
         [else (error 'parse "unrecognized symbol")]
         ))]
    [else (error 'parse "unrecognized symbol")]))

(define (ite-calc e)
  (type-case IteExp e
             [(numE n) (numV n)]
             [(boolE b) (boolV b)]
             [(plusE l r) (add (ite-calc l) (ite-calc r))]
             [(condE arms)
              (type-case (Listof 'a) arms
                [empty (error 'runtime "incomplete match")]
                [(cons a b)
                 (cond
                   [(boolean-decision (ite-calc (fst a))) (ite-calc (snd a))]
                   [else (ite-calc (condE b))])])]))

(test (ite-calc (ite-parse `(cond (#t 10) (#f 20)))) (numV 10))
(test/exn (ite-calc (ite-parse `(cond (10 10) (#f 20)))) "")
(test (ite-calc (ite-parse `(cond (#t (cond (#f 0) (#t 25))) (#f 20) (#t 0)))) (numV 25))