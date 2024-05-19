#lang plait

(define-type LExp
  [varE (n : Symbol)]                 ; variable reference
  [numE (n : Number)]                 ; numbers
  [lamE (x : Symbol) (body : LExp)]   ; lambda introduction
  [appE (e : LExp) (arg : LExp)])     ; lambda application: run function e1 with argument

(define-type Value
  [funV (arg : Symbol) (body : LExp)]
  [numV (n : Number)])

(define (get-arg v)
  (type-case Value v
    [(funV arg body) arg]
    [else (error 'runtime "invalid")]))

(define (get-body v)
  (type-case Value v
    [(funV arg body) body]
    [else (error 'runtime "invalid")]))

; perform e1[x |-> e2]
(subst : (LExp Symbol LExp -> LExp))
(define (subst e1 x e2)
  (type-case LExp e1
    [(varE s) (if (symbol=? s x)
                  e2
                  e1)]
    [(numE n) (numE n)]
    [(lamE id body)
     (if (symbol=? id x)
         e1    ; shadowing case
         (lamE id (subst body x e2)))]
    [(appE func exp) (appE (subst func x e2)
                           (subst exp x e2))]))

(define (interp e)
  (type-case LExp e
    [(varE s) (error 'runtime "unbound symbol")]
    [(numE n) (numV n)]
    [(lamE id body) (funV id body)]
    [(appE e1 e2)
     (letrec [(e1V (interp e1))
              (body (get-body e1V))
              (id (get-arg e1V))
              (argV (interp e2))]
       (type-case Value argV
         [(funV argId argBody)
          (interp (subst body id (lamE argId argBody)))]
         [(numV n)
          (interp (subst body id (numE n)))]))]))

(interp (appE (lamE 'x (varE 'x)) (numE 10)))
(interp (appE (lamE 'y (lamE 'x (varE 'y))) (numE 10)))