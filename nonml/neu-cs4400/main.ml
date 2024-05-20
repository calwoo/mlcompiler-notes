(* exercise 1: basic OCaml *)

exception Not_implemented

let rec sum_if (l : int list) (f : int -> bool) : int =
  match l with
  | [] -> 0
  | x :: xs -> if f x then x + sum_if xs f else sum_if xs f

type btree = Leaf of int | Node of int * btree * btree

let rec sum_tree_if (t : btree) (f : int -> bool) : int =
  match t with
  | Leaf i -> if f i then i else 0
  | Node (v, l, r) ->
      if f v then v + sum_tree_if l f + sum_tree_if r f
      else sum_tree_if l f + sum_tree_if r f

(**********************************************************************************)
(* exercise 2: environment-passing untyped lambda-calculus interpreter *)
module StringMap = Map.Make (String)

exception Runtime of string

type lexp =
  | App of lexp * lexp
  | Abs of string * lexp
  | Let of string * lexp * lexp
  | Var of string
  | Num of int
  | Add of lexp * lexp

type lamvalue = LamV of lamvalue StringMap.t * string * lexp | NumV of int
type env = lamvalue StringMap.t

let mt_env = StringMap.empty

let get_num v =
  match v with
  | LamV _ -> raise (Runtime "runtime: expected number")
  | NumV v -> v

let rec interp_l (env : env) e =
  match e with
  | Var s -> (
      match StringMap.find_opt s env with
      | Some v -> v
      | None -> raise (Runtime "runtime: unbound variable"))
  | Num i -> NumV i
  | Abs (v, b) -> LamV (env, v, b)
  | Add (l, r) -> NumV (get_num (interp_l env l) + get_num (interp_l env r))
  | App (fn, arg) -> (
      let evalfn = interp_l env fn in
      let evalarg = interp_l env arg in
      match evalfn with
      | LamV (closure, argu, body) ->
          interp_l (StringMap.add argu evalarg closure) body
      | NumV _ -> raise (Runtime "runtime: trying to run a number"))
  | Let (s, t, body) ->
      let evalt = interp_l env t in
      interp_l (StringMap.add s evalt env) body

(**********************************************************************************)

module IntMap = Map.Make (Int)
(** exercise 3: a typechecker and interpreter for a language with references *)

type hvalue = NumV of int | LocV of int
type heap = { fresh : int; state : hvalue IntMap.t }
type henv = hvalue StringMap.t

(** returns a pair (new_loc, new_heap) where new_heap is the result of inserting value
    into h at location loc *)
let alloc_heap (h : heap) (value : hvalue) : int * heap =
  let ret_address = h.fresh in
  let new_heap = IntMap.add ret_address value h.state in
  (ret_address, { fresh = ret_address + 1; state = new_heap })

(** looks up location in h *)
let lookup_heap (h : heap) (loc : int) : hvalue = IntMap.find loc h.state

(* returns a new heap equal to h except at location loc is equal to v *)
let update_heap (h : heap) (loc : int) (v : hvalue) =
  { fresh = h.fresh; state = IntMap.add loc v h.state }

let empty_heap = { fresh = 0; state = IntMap.empty }

(* atoms do not affect the heap *)
type atom = Num of int | Var of string

type hexp =
  | Let of string * hexp * hexp
  | Box of atom
  | Unbox of atom
  | Set of atom * atom
  | Atom of atom

let get_loc v =
  match v with LocV v -> v | _ -> raise (Runtime "expected location")

let rec interp_h (env : henv) (heap : heap) (e : hexp) : heap * hvalue =
  raise Not_implemented

(**********************************************************************************)
(* problem 3b *)
type typ = TNum | TRef of typ
type tenv = typ StringMap.t

exception Typecheck of string

let rec type_of tenv e = raise Not_implemented
