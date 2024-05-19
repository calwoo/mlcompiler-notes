#lang plait


; problem 1
(define-type Exp
  [numE (n : Number)]
  [plusE (l : Exp) (r : Exp)]
  [varE (s : Symbol)]
  [let1E (var : Symbol)
         (assignment : Exp)
         (body : Exp)])

(define (subst id assignment body)
  (type-case Exp body
    [(numE n) (numE n)]
    [(plusE l r) (plusE (subst id assignment l) (subst id assignment r))]
    [(varE s) (if (symbol=? s id) (numE assignment) (varE s))]
    [(let1E innervar innerassignment innerbody)
     (let1E innervar (subst id assignment innerassignment)
            ; check for shadowing
            ; if id is being shadowed, then return inner body
            ; else, substitute inner body
            (if (symbol=? innervar id)
                innerbody
                (subst id assignment innerbody))
            )]))

(define (eval e)
  (type-case Exp e
    [(numE n) n]
    [(plusE l r) (+ (eval l) (eval r))]
    [(varE s) (error 'runtime "uninitialized")]
    [(let1E id assignment body)
       ;Semantics of (let1E var assignment body):
       ;(1) evaluate assignment to value
       ;(2) substitute `var` with value in body
       ;(3) evaluate body
     (eval (subst id (eval assignment) body))
     ]))

(define (broken-subst id assignment body)
  (type-case Exp body
    [(numE n) (numE n)]
    [(plusE l r) (plusE (broken-subst id assignment l)
                        (broken-subst id assignment r))]
    [(varE s) (if (symbol=? s id)
                  (numE assignment)
                  (varE s))]
    [(let1E innervar innerassignment innerbody)
     (let1E innervar (broken-subst id assignment innerassignment)
            (broken-subst id assignment innerbody))]))

(define (broken-eval e)
  (type-case Exp e
    [(numE n) n]
    [(plusE l r) (+ (broken-eval l) (broken-eval r))]
    [(varE s) (error 'runtime "uninitialized")]
    [(let1E id assignment body)
     (broken-eval (broken-subst id (broken-eval assignment) body))]))

(test (broken-eval (let1E 'x (numE 10)
                          (let1E 'x (numE 20) (varE 'x)))) 10)
(test (broken-eval (let1E 'x (numE 20)
                          (let1E 'x (plusE (varE 'x) (numE 5))
                                 (varE 'x)))) 20)

(define unaffected
  (let1E 'x (numE 10)
         (let1E 'y (numE 20) (varE 'x))))

(test (eval unaffected) (broken-eval unaffected))

(define affected
  (let1E 'x (numE 10)
         (let1E 'x (numE 20) (plusE (varE 'x) (varE 'x)))))

(test (eval affected) 40)
(test (broken-eval affected) 20)

; problem 2
(define (update-names e id id2)
  (type-case Exp e
    [(numE n) (numE n)]
    [(plusE l r) (plusE (update-names l id id2)
                        (update-names r id id2))]
    [(varE s) (if (symbol=? s id)
                  (varE id2)
                  (varE s))]
    [(let1E id-let assignment body)
     (let1E (if (symbol=? id-let id) id2 id-let)
            (update-names assignment id id2)
            (update-names body id id2))]))

(test (update-names
       (let1E 'x (numE 10) (varE 'x)) 'x 'y)
      (let1E 'y (numE 10) (varE 'y)))
(test (update-names
       (let1E 'x (varE 'x) (let1E 'x (numE 10) (varE 'x))) 'x 'y)
      (let1E 'y (varE 'y) (let1E 'y (numE 10) (varE 'y))))

(define counter (box "###"))
(define (fresh-name!)
  (string->symbol (begin
                    (set-box! counter (string-append "a" (unbox counter)))
                    (unbox counter))))

; problem 3










