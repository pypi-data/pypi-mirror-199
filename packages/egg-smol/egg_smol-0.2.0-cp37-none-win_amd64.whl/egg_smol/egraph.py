from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, TypeVar, cast

from . import bindings
from .builtins import BUILTINS, BaseExpr
from .declarations import *
from .registry import *
from .registry import _fact_to_decl
from .runtime import *

__all__ = ["EGraph"]

EXPR = TypeVar("EXPR", bound=BaseExpr)


@dataclass
class EGraph(Registry):
    _egraph: bindings.EGraph = field(default_factory=bindings.EGraph)

    # The current declarations which have been pushed to the stack
    _decl_stack: list[Declarations] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Copy the builtin declarations, so we can add to it
        self._decls = deepcopy(BUILTINS._decls)

    def run(self, iterations: int) -> None:
        """
        Run the egraph for a given number of iterations.
        """
        self._egraph.run_rules(iterations)

    def check(self, fact: Fact) -> None:
        """
        Check if a fact is true in the egraph.
        """
        fact_decl = _fact_to_decl(fact)
        fact_egg = fact_decl_to_egg(self._decls, fact_decl)
        return self._egraph.check_fact(fact_egg)

    def extract(self, expr: EXPR) -> EXPR:
        """
        Extract the lowest cost expression from the egraph.
        """
        tp, decl = expr_parts(expr)
        egg_expr = decl.to_egg(self._decls)
        _cost, new_egg_expr, _variants = self._egraph.extract_expr(egg_expr)
        new_tp, new_decl = tp_and_expr_decl_from_egg(self._decls, new_egg_expr)
        if new_tp != tp:
            raise RuntimeError(f"Type mismatch: {tp} != {new_tp}")
        return cast(EXPR, RuntimeExpr(self._decls, tp, new_decl))

    def extract_multiple(self, expr: EXPR, n: int) -> list[EXPR]:
        """
        Extract multiple expressions from the egraph.
        """
        tp, decl = expr_parts(expr)
        egg_expr = decl.to_egg(self._decls)
        _cost, new_egg_expr, variants = self._egraph.extract_expr(
            egg_expr, variants=n + 1
        )
        new_decls = [
            tp_and_expr_decl_from_egg(self._decls, egg_expr)[1]
            for egg_expr in variants[::-1]
        ]
        return [
            cast(EXPR, RuntimeExpr(self._decls, tp, new_decl)) for new_decl in new_decls
        ]

    def define(self, name: str, expr: EXPR, cost: Optional[int] = None) -> EXPR:
        """
        Define a new expression in the egraph and return a reference to it.
        """
        tp, decl = expr_parts(expr)
        self._egraph.define(name, decl.to_egg(self._decls), cost)
        self._decls.constants[name] = ConstantDecl(tp, decl, cost)
        self._register_callable_ref(name, ConstantRef(name))
        return cast(EXPR, RuntimeExpr(self._decls, tp, VarDecl(name)))

    def push(self) -> None:
        """
        Push the current state of the egraph, so that it can be popped later and reverted back.
        """
        self._egraph.push()
        self._decl_stack.append(self._decls)
        self._decls = deepcopy(self._decls)

    def pop(self) -> None:
        """
        Pop the current state of the egraph, reverting back to the previous state.
        """
        self._egraph.pop()
        self._decls = self._decl_stack.pop()

    def __enter__(self):
        """
        Copy the egraph state, so that it can be reverted back to the original state at the end.
        """
        self.push()

    def __exit__(self, exc_type, exc, exc_tb):
        self.pop()

    def _on_register_function(self, ref: CallableRef, decl: FunctionDecl) -> None:
        # Don't need to registry constants, since they are already registered
        if isinstance(ref, ConstantRef):
            raise RuntimeError("Constants should not be registered as functions")
        egg_decl = decl.to_egg(self._decls, self._egraph, ref)
        self._egraph.declare_function(egg_decl)

    def _on_register_sort(self, name: str) -> None:
        self._egraph.declare_sort(name, None)

    def _on_register_rewrite(self, rewrite: RewriteDecl) -> None:
        self._egraph.add_rewrite(rewrite.to_egg(self._decls))

    def _on_register_rule(self, rule: RuleDecl) -> None:
        self._egraph.add_rule(rule.to_egg(self._decls))

    def _on_register_action(self, decl: ActionDecl) -> None:
        self._egraph.eval_actions(action_decl_to_egg(self._decls, decl))
