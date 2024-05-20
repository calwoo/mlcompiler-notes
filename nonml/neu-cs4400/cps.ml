(************************************)
(* Exceptions and Testing Functions *)
(************************************)

exception Not_implemented
exception Runtime

(* Asserts that a function call throws a Runtime exception. *)
let assert_runtime (f : unit -> 'a) : unit =
  try
    f ();
    assert false
  with
  | Runtime -> assert true
  | _ -> assert false

exception Uncaught_exception

(* Asserts that a function call throws a Uncaught_exception exception. *)
let assert_uncaught (f : unit -> 'a) : unit =
  try
    f ();
    assert false
  with
  | Uncaught_exception -> assert true
  | _ -> assert false

(*************)
(* Problem 1 *)
(*************)

(**************)
(* Problem 1a *)
(**************)

(* Continuation passing function for 'factors_helper' in tail form. *)
let rec factors_helper_cps (n : int) (d : int) (kont : int list -> int list) :
    int list =
  if n = 1 then kont []
  else if n mod d = 0 then factors_helper_cps (n / d) 2 (fun x -> kont (d :: x))
  else factors_helper_cps n (d + 1) kont

(* Computes all of the prime factors of n using 'factors_helper_cps'. *)
let factors_cps (n : int) : int list = factors_helper_cps n 2 (fun x -> x)

(**************)
(* Problem 1b *)
(**************)

(* Represents a binary tree. *)
type btree = Leaf of int | Node of int * btree * btree

(* Continuation passing helper function for 'all_prime_cps'. *)
let rec all_prime_helper_cps (t : btree) (kont : bool -> bool) : bool =
  raise Not_implemented

(* Returns true if all vertices (leaves & nodes) in a btree are prime;
   otherwise, returns false. Uses helper funciton 'all_prime_helper_cps'. *)
let all_prime_cps (t : btree) : bool = raise Not_implemented

(**************)
(* Problem 1c *)
(**************)

(* Continuation passing helper function for 'zip_with_cps'. *)
let rec zip_with_helper_cps (x : 'a list) (y : 'b list) (f : 'a -> 'b -> 'c)
    (kont : 'c list -> 'c list) : 'c list =
  raise Not_implemented

(* Zips two lists into a single list, given a function that combines list
   elements pair-wise. Uses helper function 'zip_with_helper_cps'. *)
let zip_with_cps (x : 'a list) (y : 'b list) (f : 'a -> 'b -> 'c) : 'c list =
  raise Not_implemented

(*************)
(* Problem 2 *)
(*************)

module StringMap = Map.Make (String)

(* Syntax for expressions in the extended try-catch language. *)
type texp =
  | Var of string
  | Lam of string * texp
  | App of texp * texp
  (* Follows the syntax: Try(try_exp, exception_code, catch_exp) *)
  | Try of texp * int * texp
  (* Follows the syntax: Raise(exception_code) *)
  | Raise of int

(* Syntax for values in the extended try-catch language. *)
type tvalue =
  (* Follows the syntax: Lam(x, closure, body) *)
  | Lam of string * tvalue StringMap.t * texp

(* An environment is a mapping from variable names (strings) to expressions. *)
type env = tvalue StringMap.t

let mt_env = StringMap.empty

module IntMap = Map.Make (Int)

(* A 'kont_map' is a mapping from exception codes (integers) to
   continuations. *)
type kont_map = (unit -> tvalue) IntMap.t

let mt_kont_map = IntMap.empty

(* Continuation passing helper function for 'interp'. *)
let rec interp_h (exp : texp) (env : env) (handlers : kont_map)
    (kont : tvalue -> tvalue) : tvalue =
  raise Not_implemented

(* Interprets expressions in the 'texp' language using the helper function 'interp_h'. *)
let interp (exp : texp) : tvalue = raise Not_implemented

(*************)
(* Problem 3 *)
(*************)

(* The calculator language, with nested computations *)
type calc =
  | Const of int
  | Add of calc * calc
  | Mul of calc * calc
  | Sub of calc * calc
  | Div of calc * calc

(* The calculator language, in ANF form. This has:
    1. value of either variables or constants,
    2. arith_anf made out of values,
    3. calc_anf a sequence of arith_anfs. *)
type value = Var of string | Const of int

type arith_anf =
  | Val of value
  | Add of value * value
  | Mul of value * value
  | Sub of value * value
  | Div of value * value

type calc_anf = Finally of arith_anf | Let of string * arith_anf * calc_anf

(* Evaluating calc expressions *)
let rec eval_calc : calc -> int = function
  | Const i -> i
  | Add (l, r) -> eval_calc l + eval_calc r
  | Mul (l, r) -> eval_calc l * eval_calc r
  | Sub (l, r) -> eval_calc l - eval_calc r
  (* The greatest integer less than or equal to the real quotient of l by r  *)
  | Div (l, r) -> eval_calc l / eval_calc r

(* Evaluating calc_anf expressions. We assume no shadowing *)
let rec eval_calc_anf : calc_anf -> int =
 fun e -> eval_calc_anf_h StringMap.empty e

and eval_calc_anf_h s = function
  | Finally a -> eval_arith_anf s a
  | Let (x, a, c) ->
      let v = eval_arith_anf s a in
      let s' = StringMap.add x v s in
      eval_calc_anf_h s' c

and eval_arith_anf s = function
  | Val v -> lookup s v
  | Add (l, r) -> lookup s l + lookup s r
  | Mul (l, r) -> lookup s l * lookup s r
  | Sub (l, r) -> lookup s l - lookup s r
  | Div (l, r) -> lookup s l / lookup s r

and lookup s = function Const i -> i | Var x -> StringMap.find x s

(* Calling fresh () will generate a new variable name *)
let ct = ref (-1)

let fresh _ =
  ct := !ct + 1;
  "x" ^ Int.to_string !ct

let rec to_anf : calc -> calc_anf =
 fun e -> to_anf_h e (fun x -> raise Not_implemented)

and to_anf_h : calc -> (value -> calc_anf) -> calc_anf =
 fun e k -> raise Not_implemented
