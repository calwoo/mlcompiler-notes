#lang plait


; exercise 1
(define (all-greater? [nums : (Listof Number)] [comp : Number]) : Boolean
  (type-case (Listof 'a) nums
    [empty #t]
    [(cons a b) (cond
                  [(> a comp) (all-greater? b comp)]
                  [else #f])]))

(test (all-greater? '(1 2 9) 0) #t)
(test (all-greater? '() 0) #t)
(test (all-greater? '(2 3 5) 4) #f)

; exercise 2
(define (sorted? [nums : (Listof Number)]) : Boolean
  (type-case (Listof 'a) nums
    [empty #t]
    [(cons a b) (if (all-greater? b a)
                    (sorted? b)
                    #f)]))

(test (sorted? '(1 2 3)) #t)
(test (sorted? '()) #t)
(test (sorted? '(2 1 3)) #f)

; exercise 3
(define-type Tree
  (leaf [val : Number])
  (node [val : Number]
        [left : Tree]
        [right : Tree]))

(define (sum [tree : Tree]) : Number
  (type-case Tree tree
    [(leaf val) val]
    [(node val left right) (+ val (+ (sum left) (sum right)))]))

(test (sum (node 5 (leaf 6) (leaf 7))) 18)
(test (sum (leaf 3)) 3)
(test (sum (node 3
                 (node 5
                       (leaf 2)
                       (leaf -1))
                 (node 4
                       (leaf 0)
                       (leaf 8))))
      21)

; exercise 4
(define (contains? [tree : Tree] [num : Number]) : Boolean
  (type-case Tree tree
    [(leaf val) (equal? val num)]
    [(node val left right)
       (or (equal? val num)
           (or (contains? left num)
               (contains? right num)))]))

(test (contains? (node 0 (leaf 4) (leaf 5)) 5) #t)
(test (contains? (node 0 (leaf 4) (leaf 5)) 3) #f)

; exercise 5
(define (nonneg [tree : Tree]) : Tree
  (type-case Tree tree
    [(leaf val) (if (>= val 0)
                    tree
                    (leaf 0))]
    [(node val left right) (if (>= val 0)
                               (node val (nonneg left) (nonneg right))
                               (node 0 (nonneg left) (nonneg right)))]))

(test (nonneg (node -4 (leaf 6) (leaf 7)))
      (node 0 (leaf 6) (leaf 7)))
(test (nonneg (leaf -2)) (leaf 0))
