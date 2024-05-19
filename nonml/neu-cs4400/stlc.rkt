#lang plait

(define-type LType
  [NumT]
  [FunT (arg : LType) (body : LType)])

(define-type LExp
  [varE (s : Symbol)]
  [numE (n : Number)]
  [lamE (arg : Symbol) (typ : LType) (body : LExp)]
  [appE (e : LExp) (arg : LExp)])

; perform e1[x |-> e2]
(subst : (LExp Symbol LExp -> LExp))
(define (subst e1 x e2)
  (type-case LExp e1
    [(varE s) (if (symbol=? s x)
                  e2
                  (varE s))]
    [(numE n) (numE n)]
    [(lamE id typ body)
    (if (symbol=? x id)
      (lamE id typ body)              ; shadowing case
      (lamE id typ (subst body x e2)))]
    [(appE e1App e2App)
     (appE (subst e1App x e2)
           (subst e2App x e2))]))

(define (interp e)
  (type-case LExp e
    [(varE s) (error 'runtime "unbound symbol")]
    [(lamE id typ body) (lamE id typ body)]
    [(numE n) (numE n)]
    [(appE e1 e2)
     ; run e1 to get (lambda (id) body)
     ; run e2 to get a value argV
     ; run body[id |-> v]
     (letrec [(e1V (interp e1))
              (body (lamE-body e1V))
              (id (lamE-arg e1V))
              (argV (interp e2))]
       (interp (subst body id argV)))]))

; typechecking
(define-type-alias TEnv (Hashof Symbol LType))
(define mt-env (hash empty)) ; empty typeenv

(define (lookup (gam : TEnv) (s : Symbol))
  (type-case (Optionof LType) (hash-ref gam s)
    [(none) (error 'type-error "unrecognized symbol")]
    [(some v) v]))

(extend : (TEnv Symbol LType -> TEnv))
(define (extend old-env new-name value)
  (hash-set old-env new-name value))

(define (type-of env e)
  (type-case LExp e
    [(varE s) (lookup env s)]
    [(numE n) (NumT)]
    [(lamE arg typ body)
     (FunT typ (type-of (extend env arg typ) body))]
    [(appE e1 e2)
     (let [(t-e1 (type-of env e1))
           (t-e2 (type-of env e2))]
       (type-case LType t-e1
         [(FunT tau1 tau2)
          (if (equal? tau1 t-e2)
              tau2
              (error 'type-error "invalid function call"))]
         [else (error 'type-error "invalid function call")]))]))

(test (interp (appE (lamE 'x (NumT) (varE 'x)) (numE 10))) (numE 10))
(test (type-of mt-env (lamE 'x (NumT) (varE 'x))) (FunT (NumT) (NumT)))








