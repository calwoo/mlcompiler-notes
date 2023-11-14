class ASTTransformer:
    @staticmethod
    def transform_def_to_var_lambda(def_exp):
        (_, fn_name, fn_params, fn_body) = def_exp
        desugared_exp = ["var", fn_name, ["lambda", fn_params, fn_body]]
        return desugared_exp

    @staticmethod
    def transform_switch_to_if(switch_exp):
        (_, *cases) = switch_exp
        
        def if_builder(cases):
            if_exp = ["if", None, None, None]
            cond, val = cases[0]
            if_exp[1] = cond
            if_exp[2] = val
            # lookahead
            next_cond, next_val = cases[1]
            if next_cond == "else":
                # break
                if_exp[3] = next_val
            else:
                # recurse
                if_exp[3] = if_builder(cases[1:])
            return if_exp

        return if_builder(cases)

    @staticmethod
    def transform_for_to_while(for_exp):
        (_, init, condition, modifier, exp) = for_exp
        while_exp = ["begin",
            init,
            ["while", condition, ["begin",
                exp, modifier
            ]]
        ]
        return while_exp

    @staticmethod
    def transform_inc_to_set(inc_exp):
        (_, var) = inc_exp
        return ["set", var, ['+', var, 1]]
    
    @staticmethod
    def transform_incassign_to_set(inc_exp):
        (_, var, val) = inc_exp
        return ["set", var, ['+', var, val]]
    
    @staticmethod
    def transform_dec_to_set(dec_exp):
        (_, var) = dec_exp
        return ["set", var, ['-', var, 1]]
    
    @staticmethod
    def transform_decassign_to_set(dec_exp):
        (_, var, val) = dec_exp
        return ["set", var, ['-', var, val]]
