#lang plait

(define-type Exp
  [numE (n : Number)]
  [plusE (left : Exp) (right : Exp)]
  [varE (name : Symbol)]
  [let1E (var : Symbol)
         (assignment : Exp)
         (body : Exp)])

(subst : (Exp Symbol Exp -> Exp))
(define (subst substE substId substV)
  (type-case Exp substE
    [(varE name) (if (symbol=? name substId) substV substE)]
    [(plusE l r) (plusE (subst l substId substV)
                        (subst r substId substV))]
    [(numE n) (numE n)]
    [(let1E var assignment body)
     (let [(substV (subst assignment substId substV))
           (substBody (subst body substId substV))]
       (if (symbol=? var substId)
           (let1E var substV body) ; don't substitute, shadowing
           (let1E var substV substBody)))]))

(eval : (Exp -> Number))
(define (eval e)
  (type-case Exp e
    [(numE n) n]
    [(plusE l r) (+ (eval l) (eval r))]
    [(varE s) (error 'runtime "uninitialized variable")]
    [(let1E var assignment body)
     (let [(assign-eval (numE (eval assignment)))]
       (eval (subst body var assign-eval)))]))

; tests
(test (eval (let1E 'x (numE 10)
               (let1E 'x (numE 20)
                      (varE 'x)))) 20)

(test (eval (let1E 'x (numE 10) (plusE (varE 'x) (varE 'x)))) 20)

(test (eval (let1E 'x (numE 10)
                   (plusE (varE 'x)
                          (let1E 'x (numE 20) (varE 'x))))) 30)

(test (eval (plusE (let1E 'x (numE 10) (varE 'x)) (let1E 'x (numE 15) (varE 'x)))) 25)
