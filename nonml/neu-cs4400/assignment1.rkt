#lang plait


; exercise 1
(define (my-max a b)
  (cond
    [(>= a b) a]
    [(< a b) b]))

(test (my-max 5 6) 6)
(test (my-max 4 -3) 4)
(test (my-max 0 0) 0)

; exercise 2
(define (plural word)
  (local [(define end-y?
            (equal? #\y (string-ref word (- (string-length word) 1))))]
  (cond
    [end-y? (string-append
              (substring word 0 (- (string-length word) 1))
              "ies")]
    [else (string-append word "s")])))

(test (plural "baby") "babies")
(test (plural "fish") "fishs")
(test (plural "ruby") "rubies")

; exercise 3
(define-type Light
  (bulb [watts-per-hour : Number] [technology : Symbol])
  (candle [inches : Number]))

(define (electricity-usage light)
  (cond
    [(candle? light) 0]
    [(bulb? light) (* 24 (bulb-watts-per-hour light))]))

(test (electricity-usage (bulb 10 'modern)) 240)
(test (electricity-usage (candle 1.1)) 0)

; exercise 4
(define (use-for-one-hour light)
  (cond
    [(candle? light) (candle (- (candle-inches light) 1))]
    [else light]))

(test (use-for-one-hour (bulb 100 'halogen)) (bulb 100 'halogen))
(test (use-for-one-hour (bulb 25 'magic)) (bulb 25 'magic))
(test (use-for-one-hour (candle 1)) (candle 0))
