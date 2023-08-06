from __future__ import annotations

from dataclasses import dataclass, field
from inspect import Parameter, currentframe, signature
from types import FunctionType
from typing import _GenericAlias  # type: ignore[attr-defined]
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Literal,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    cast,
    get_type_hints,
    overload,
)

from typing_extensions import ParamSpec, get_args, get_origin

from .declarations import *
from .monkeypatch import monkeypatch_forward_ref
from .runtime import *
from .runtime import class_to_ref

monkeypatch_forward_ref()

__all__ = [
    "Registry",
    "BUILTINS",
    "BaseExpr",
    "Unit",
    "rewrite",
    "eq",
    "panic",
    "let",
    "delete",
    "union",
    "set_",
    "rule",
    "var",
    "vars_",
    "Fact",
    "expr_parts",
]

T = TypeVar("T")
P = ParamSpec("P")
TYPE = TypeVar("TYPE", bound=type)
CALLABLE = TypeVar("CALLABLE", bound=Callable)
EXPR = TypeVar("EXPR", bound="BaseExpr")

# Attributes which are sometimes added to classes by the interpreter or the dataclass decorator, or by ipython.
# We ignore these when inspecting the class.

IGNORED_ATTRIBUTES = {
    "__module__",
    "__doc__",
    "__dict__",
    "__weakref__",
    "__orig_bases__",
}


@dataclass
class Registry:
    """
    A registry holds all the declerations of classes and functions as well as the mapping
    to and from egg names to python names.
    """

    _decls: Declarations = field(default_factory=Declarations)

    def _on_register_sort(self, name: str) -> None:
        """
        Called whenever a sort is registered.
        """
        pass

    def _on_register_function(self, ref: CallableRef, decl: FunctionDecl) -> None:
        """
        Called whenever a function is registered.
        """
        pass

    def _on_register_rewrite(self, decl: RewriteDecl) -> None:
        """
        Called whenever a rewrite is registered.
        """
        pass

    def _on_register_rule(self, decl: RuleDecl) -> None:
        """
        Called whenever a rule is registered.
        """
        pass

    def _on_register_action(self, decl: ActionDecl) -> None:
        pass

    @overload
    def class_(self, *, egg_sort: str) -> Callable[[TYPE], TYPE]:
        ...

    @overload
    def class_(self, cls: TYPE, /) -> TYPE:
        ...

    def class_(self, *args, **kwargs) -> Any:
        """
        Registers a class.
        """
        hint_locals = currentframe().f_back.f_locals  # type: ignore

        if kwargs:
            assert set(kwargs.keys()) == {"egg_sort"}
            return lambda cls: self._class(cls, hint_locals, kwargs["egg_sort"])
        assert len(args) == 1
        return self._class(args[0], hint_locals)

    def _class(
        self,
        cls: type[BaseExpr],
        hint_locals: dict[str, Any],
        egg_sort: Optional[str] = None,
    ) -> RuntimeClass:
        """
        Registers a class.
        """
        cls_name = cls.__name__
        # Get all the methods from the class
        cls_dict: dict[str, Any] = {
            k: v for k, v in cls.__dict__.items() if k not in IGNORED_ATTRIBUTES
        }
        parameters: list[TypeVar] = cls_dict.pop("__parameters__", [])

        # Register class first
        if cls_name in self._decls.classes:
            raise ValueError(f"Class {cls_name} already registered")
        n_type_vars = len(parameters)
        cls_decl = ClassDecl(n_type_vars=n_type_vars)
        self._decls.classes[cls_name] = cls_decl
        self._decls.register_sort(JustTypeRef(cls_name), egg_sort)
        self._on_register_sort(egg_sort or cls_name)

        # The type ref of self is paramterized by the type vars
        slf_type_ref = TypeRefWithVars(
            cls_name, tuple(ClassTypeVarRef(i) for i in range(n_type_vars))
        )

        # Then register each of its methods
        for method_name, method in cls_dict.items():
            is_init = method_name == "__init__"
            # Don't register the init methods for literals, since those don't use the type checking mechanisms
            if is_init and cls_name in LIT_CLASS_NAMES:
                continue
            if isinstance(method, _WrappedMethod):
                fn = method.fn
                egg_fn = method.egg_fn
                cost = method.cost
                default = method.default
                merge = method.merge
            else:
                fn = method
                egg_fn, cost, default, merge = None, None, None, None
            if isinstance(fn, classmethod):
                fn = fn.__func__
                is_classmethod = True
            else:
                # We count __init__ as a classmethod since it is called on the class
                is_classmethod = is_init

            fn_decl = self._generate_function_decl(
                fn,
                hint_locals,
                default,
                cost,
                merge,
                "cls" if is_classmethod and not is_init else slf_type_ref,
                parameters,
                is_init,
                # If this is an i64, use the runtime class for the alias so that i64Like is resolved properly
                # Otherwise, this might be a Map in which case pass in the original cls so that we
                # can do Map[T, V] on it, which is not allowed on the runtime class
                (
                    RuntimeClass(self._decls, "i64") if cls_name == "i64" else cls,
                    cls_name,
                ),
            )
            ref: MethodRef | ClassMethodRef
            if is_classmethod:
                cls_decl.class_methods[method_name] = fn_decl
                ref = ClassMethodRef(cls_name, method_name)
            else:
                cls_decl.methods[method_name] = fn_decl
                ref = MethodRef(cls_name, method_name)
            self._register_callable_ref(egg_fn, ref)
            self._on_register_function(ref, fn_decl)

        # Register != as a method so we can print it as a string
        self._register_callable_ref("!=", MethodRef(cls_name, "__ne__"))
        return RuntimeClass(self._decls, cls_name)

    # We seperate the function and method overloads to make it simpler to know if we are modifying a function or method,
    # So that we can add the functions eagerly to the registry and wait on the methods till we process the class.

    # We have to seperate method/function overloads for those that use the T params and those that don't
    # Otherwise, if you say just pass in `cost` then the T param is inferred as `Nothing` and
    # It will break the typing.
    @overload
    def method(  # type: ignore
        self,
        *,
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        merge: Optional[Callable[[Any, Any], Any]] = None,
    ) -> Callable[[CALLABLE], CALLABLE]:
        ...

    @overload
    def method(
        self,
        *,
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        default: Optional[EXPR] = None,
        merge: Optional[Callable[[EXPR, EXPR], EXPR]] = None,
    ) -> Callable[[Callable[P, EXPR]], Callable[P, EXPR]]:
        ...

    def method(
        self,
        *,
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        default: Optional[EXPR] = None,
        merge: Optional[Callable[[EXPR, EXPR], EXPR]] = None,
    ) -> Callable[[Callable[P, EXPR]], Callable[P, EXPR]]:
        return lambda fn: _WrappedMethod(egg_fn, cost, default, merge, fn)

    @overload
    def function(self, fn: CALLABLE, /) -> CALLABLE:
        ...

    @overload
    def function(  # type: ignore
        self,
        *,
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        merge: Optional[Callable[[Any, Any], Any]] = None,
    ) -> Callable[[CALLABLE], CALLABLE]:
        ...

    @overload
    def function(
        self,
        *,
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        default: Optional[EXPR] = None,
        merge: Optional[Callable[[EXPR, EXPR], EXPR]] = None,
    ) -> Callable[[Callable[P, EXPR]], Callable[P, EXPR]]:
        ...

    def function(self, *args, **kwargs) -> Any:
        """
        Registers a function.
        """
        fn_locals = currentframe().f_back.f_locals  # type: ignore

        # If we have any positional args, then we are calling it directly on a function
        if args:
            assert len(args) == 1
            return self._function(args[0], fn_locals)
        # otherwise, we are passing some keyword args, so save those, and then return a partial
        return lambda fn: self._function(fn, fn_locals, **kwargs)

    def _function(
        self,
        fn: Callable[..., RuntimeExpr],
        hint_locals: dict[str, Any],
        egg_fn: Optional[str] = None,
        cost: Optional[int] = None,
        default: Optional[RuntimeExpr] = None,
        merge: Optional[Callable[[RuntimeExpr, RuntimeExpr], RuntimeExpr]] = None,
    ) -> RuntimeFunction:
        """
        Uncurried version of function decorator
        """
        name = fn.__name__
        if name in self._decls.functions:
            raise ValueError(f"Function {name} already registered")

        # Save function decleartion
        fn_decl = self._generate_function_decl(fn, hint_locals, default, cost, merge)
        self._decls.functions[name] = fn_decl
        # Register it with the egg name
        fn_ref = FunctionRef(name)
        self._register_callable_ref(egg_fn, fn_ref)
        self._on_register_function(fn_ref, fn_decl)
        # Return a runtime function whcich will act like the decleration
        return RuntimeFunction(self._decls, name)

    def _generate_function_decl(
        self,
        fn: Any,
        # Pass in the locals, retrieved from the frame when wrapping,
        # so that we support classes and function defined inside of other functions (which won't show up in the globals)
        hint_locals: dict[str, Any],
        default: Optional[RuntimeExpr],
        cost: Optional[int],
        merge: Optional[Callable[[RuntimeExpr, RuntimeExpr], RuntimeExpr]],
        # The first arg is either cls, for a classmethod, a self type, or none for a function
        first_arg: Literal["cls"] | TypeOrVarRef | None = None,
        cls_typevars: list[TypeVar] = [],
        is_init: bool = False,
        cls_type_and_name: Optional[tuple[type | RuntimeClass, str]] = None,
    ) -> FunctionDecl:
        if not isinstance(fn, FunctionType):
            raise NotImplementedError(
                f"Can only generate function decls for functions not {fn}  {type(fn)}"
            )

        hint_globals = fn.__globals__.copy()

        if cls_type_and_name:
            hint_globals[cls_type_and_name[1]] = cls_type_and_name[0]
        hints = get_type_hints(fn, hint_globals, hint_locals)
        # If this is an init fn use the first arg as the return type
        if is_init:
            if not isinstance(first_arg, (ClassTypeVarRef, TypeRefWithVars)):
                raise ValueError("Init function must have a self type")
            return_type = first_arg
        else:
            return_type = self._resolve_type_annotation(
                hints["return"], cls_typevars, cls_type_and_name
            )

        params = list(signature(fn).parameters.values())
        # Remove first arg if this is a classmethod or a method, since it won't have an annotation
        if first_arg is not None:
            first, *params = params
            if first.annotation != Parameter.empty:
                raise ValueError(
                    f"First arg of a method must not have an annotation, not {first.annotation}"
                )

        for param in params:
            if param.kind != Parameter.POSITIONAL_OR_KEYWORD:
                raise ValueError(
                    f"Can only register functions with positional or keyword args, not {param.kind}"
                )

        arg_types = tuple(
            self._resolve_type_annotation(
                hints[t.name], cls_typevars, cls_type_and_name
            )
            for t in params
        )
        # If the first arg is a self, and this not an __init__ fn, add this as a typeref
        if isinstance(first_arg, (ClassTypeVarRef, TypeRefWithVars)) and not is_init:
            arg_types = (first_arg,) + arg_types

        default_decl = None if default is None else default.__egg_expr__
        merge_decl = (
            None
            if merge is None
            else merge(
                RuntimeExpr(self._decls, return_type.to_just(), VarDecl("old")),
                RuntimeExpr(self._decls, return_type.to_just(), VarDecl("new")),
            ).__egg_expr__
        )
        decl = FunctionDecl(
            return_type=return_type,
            arg_types=arg_types,
            cost=cost,
            default=default_decl,
            merge=merge_decl,
        )
        return decl

    def _register_callable_ref(self, egg_fn: Optional[str], ref: CallableRef) -> None:
        egg_fn = egg_fn or ref.generate_egg_name()
        if ref in self._decls.callable_ref_to_egg_fn:
            raise ValueError(f"Callable ref {ref} already registered")
        self._decls.callable_ref_to_egg_fn[ref] = egg_fn
        self._decls.egg_fn_to_callable_refs[egg_fn].add(ref)

    def _resolve_type_annotation(
        self,
        tp: object,
        cls_typevars: list[TypeVar],
        cls_type_and_name: Optional[tuple[type | RuntimeClass, str]],
    ) -> TypeOrVarRef:
        if isinstance(tp, TypeVar):
            return ClassTypeVarRef(cls_typevars.index(tp))
        # If there is a union, it should be of a literal and another type to allow type promotion
        if get_origin(tp) == Union:
            args = get_args(tp)
            if len(args) != 2:
                raise TypeError("Union types are only supported for type promotion")
            fst, snd = args
            if fst in {int, str}:
                return self._resolve_type_annotation(
                    snd, cls_typevars, cls_type_and_name
                )
            if snd in {int, str}:
                return self._resolve_type_annotation(
                    fst, cls_typevars, cls_type_and_name
                )
            raise TypeError("Union types are only supported for type promotion")

        # If this is the type for the class, use the class name
        if cls_type_and_name and tp == cls_type_and_name[0]:
            return TypeRefWithVars(cls_type_and_name[1])

        # If this is the class for this method and we have a paramaterized class, recurse
        if (
            cls_type_and_name
            and isinstance(tp, _GenericAlias)
            and tp.__origin__ == cls_type_and_name[0]  # type: ignore
        ):
            return TypeRefWithVars(
                cls_type_and_name[1],
                tuple(
                    self._resolve_type_annotation(a, cls_typevars, cls_type_and_name)
                    for a in tp.__args__  # type: ignore
                ),
            )

        if isinstance(tp, (RuntimeClass, RuntimeParamaterizedClass)):
            return class_to_ref(tp).to_var()
        raise TypeError(f"Unexpected type annotation {tp}")

    def register(self, *values: Rewrite | Rule | Action) -> None:
        """
        Registers any number of rewrites or rules.
        """
        for value in values:
            self._register_single(value)

    def _register_single(self, value: Rewrite | Rule | Action) -> None:
        if isinstance(value, Rewrite):
            rewrite_decl = value._to_decl()
            self._decls.rewrites.append(rewrite_decl)
            self._on_register_rewrite(rewrite_decl)
        elif isinstance(value, Rule):
            rule_decl = value._to_decl()
            self._decls.rules.append(rule_decl)
            self._on_register_rule(rule_decl)
        else:
            action_decl = _action_to_decl(value)
            self._decls.actions.append(action_decl)
            self._on_register_action(action_decl)


@dataclass(frozen=True)
class _WrappedMethod(Generic[P, EXPR]):
    """
    Used to wrap a method and store some extra options on it before processing it.
    """

    egg_fn: Optional[str]
    cost: Optional[int]
    default: Optional[EXPR]
    merge: Optional[Callable[[EXPR, EXPR], EXPR]]
    fn: Callable[P, EXPR]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> EXPR:
        raise NotImplementedError(
            "We should never call a wrapped method. Did you forget to wrap the class?"
        )


class BaseExpr:
    """
    Expression base class, which adds suport for != to all expression types.
    """

    def __ne__(self: EXPR, other_expr: EXPR) -> Unit:  # type: ignore[override, empty-body]
        """
        Compare whether to expressions are not equal.

        :param self: The expression to compare.
        :param other_expr: The other expression to compare to, which must be of the same type.
        :meta public:
        """
        ...

    def __eq__(self, other: NoReturn) -> NoReturn:  # type: ignore[override, empty-body]
        """
        Equality is currently not supported. We only add this method so that
        if you try to use it MyPy will warn you.
        """
        ...


BUILTINS = Registry()


@BUILTINS.class_(egg_sort="unit")
class Unit(BaseExpr):
    """
    The unit type. This is also used to reprsent if a value exists, if it is resolved or not.
    """

    def __init__(self) -> None:
        ...


# We use these builders so that when creating these structures we can type check
# if the arguments are the same type of expression


def rewrite(lhs: EXPR) -> _RewriteBuilder[EXPR]:
    """Rewrite the given expression to a new expression."""
    return _RewriteBuilder(lhs=lhs)


def eq(expr: EXPR) -> _EqBuilder[EXPR]:
    """Check if the given expression is equal to the given value."""
    return _EqBuilder(expr)


def panic(message: str) -> Panic:
    """Raise an error with the given message."""
    return Panic(message)


def let(name: str, expr: BaseExpr) -> Let:
    """Create a let binding."""
    return Let(name, expr)


def delete(expr: BaseExpr) -> Delete:
    """Create a delete expression."""
    return Delete(expr)


def union(lhs: EXPR) -> _UnionBuilder[EXPR]:
    """Create a union of the given expression."""
    return _UnionBuilder(lhs=lhs)


def set_(lhs: EXPR) -> _SetBuilder[EXPR]:
    """Create a set of the given expression."""
    return _SetBuilder(lhs=lhs)


def rule(*facts: Fact) -> _RuleBuilder:
    """Create a rule with the given facts."""
    return _RuleBuilder(facts=facts)


def var(name: str, bound: type[EXPR]) -> EXPR:
    """Create a new variable with the given name and type."""
    return cast(EXPR, _var(name, bound))


def _var(name: str, bound: Any) -> RuntimeExpr:
    """Create a new variable with the given name and type."""
    if not isinstance(bound, (RuntimeClass, RuntimeParamaterizedClass)):
        raise TypeError(f"Unexpected type {type(bound)}")
    return RuntimeExpr(bound.__egg_decls__, class_to_ref(bound), VarDecl(name))


def vars_(names: str, bound: type[EXPR]) -> Iterable[EXPR]:
    """Create variables with the given names and type."""
    for name in names.split(" "):
        yield var(name, bound)


@dataclass
class _RewriteBuilder(Generic[EXPR]):
    lhs: EXPR

    def to(self, rhs: EXPR, *conditions: Fact) -> Rewrite:
        return Rewrite(lhs=self.lhs, rhs=rhs, conditions=list(conditions))

    def __str__(self) -> str:
        return f"rewrite({self.lhs})"


@dataclass
class _EqBuilder(Generic[EXPR]):
    expr: BaseExpr

    def to(self, *exprs: EXPR) -> Eq:
        return Eq([self.expr, *exprs])

    def __str__(self) -> str:
        return f"eq({self.expr})"


@dataclass
class _SetBuilder(Generic[EXPR]):
    lhs: BaseExpr

    def to(self, rhs: EXPR) -> Set:
        return Set(lhs=self.lhs, rhs=rhs)

    def __str__(self) -> str:
        return f"set_({self.lhs})"


@dataclass
class _UnionBuilder(Generic[EXPR]):
    lhs: BaseExpr

    def with_(self, rhs: EXPR) -> Union_:
        return Union_(lhs=self.lhs, rhs=rhs)

    def __str__(self) -> str:
        return f"union({self.lhs})"


@dataclass
class _RuleBuilder:
    facts: tuple[Fact, ...]

    def then(self, *actions: Action) -> Rule:
        return Rule(actions, self.facts)


def expr_parts(expr: BaseExpr) -> tuple[JustTypeRef, ExprDecl]:
    """
    Returns the underlying type and decleration of the expression. Useful for testing structural equality or debugging.

    :rtype: tuple[object, object]
    """
    assert isinstance(expr, RuntimeExpr)
    return expr.__egg_parts__


@dataclass
class Rewrite:
    lhs: BaseExpr
    rhs: BaseExpr
    conditions: list[Fact]

    def __str__(self) -> str:
        args_str = ", ".join(map(str, [self.rhs, *self.conditions]))
        return f"rewrite({self.lhs}).to({args_str})"

    def _to_decl(self) -> RewriteDecl:
        return RewriteDecl(
            expr_parts(self.lhs)[1],
            expr_parts(self.rhs)[1],
            tuple(_fact_to_decl(fact) for fact in self.conditions),
        )


@dataclass
class Eq:
    exprs: list[BaseExpr]

    def __str__(self) -> str:
        first, *rest = self.exprs
        args_str = ", ".join(map(str, rest))
        return f"eq({first}).to({args_str})"

    def _to_decl(self) -> EqDecl:
        return EqDecl(tuple(expr_parts(expr)[1] for expr in self.exprs))


Fact = Union[Unit, Eq]


def _fact_to_decl(fact: Fact) -> FactDecl:
    if isinstance(fact, Eq):
        return fact._to_decl()
    return expr_parts(fact)[1]


@dataclass
class Delete:
    expr: BaseExpr

    def __str__(self) -> str:
        return f"delete({self.expr})"

    def _to_decl(self) -> DeleteDecl:
        decl = expr_parts(self.expr)[1]
        if not isinstance(decl, CallDecl):
            raise ValueError(f"Can only delete calls not {decl}")
        return DeleteDecl(decl)


@dataclass
class Panic:
    message: str

    def __str__(self) -> str:
        return f"panic({self.message})"

    def _to_decl(self) -> PanicDecl:
        return PanicDecl(self.message)


@dataclass
class Union_(Generic[EXPR]):
    lhs: BaseExpr
    rhs: BaseExpr

    def __str__(self) -> str:
        return f"union({self.lhs}).with_({self.rhs})"

    def _to_decl(self) -> UnionDecl:
        return UnionDecl(expr_parts(self.lhs)[1], expr_parts(self.rhs)[1])


@dataclass
class Set:
    lhs: BaseExpr
    rhs: BaseExpr

    def __str__(self) -> str:
        return f"set_({self.lhs}).to({self.rhs})"

    def _to_decl(self) -> SetDecl:
        lhs = expr_parts(self.lhs)[1]
        if not isinstance(lhs, CallDecl):
            raise ValueError(
                f"Can only create a call with a call for the lhs, got {lhs}"
            )
        return SetDecl(lhs, expr_parts(self.rhs)[1])


@dataclass
class Let:
    name: str
    value: BaseExpr

    def __str__(self) -> str:
        return f"let({self.name}, {self.value})"

    def _to_decl(self) -> LetDecl:
        return LetDecl(self.name, expr_parts(self.value)[1])


Action = Union[Let, Set, Delete, Union_, Panic, "BaseExpr"]


def _action_to_decl(action: Action) -> ActionDecl:
    if isinstance(action, BaseExpr):
        return expr_parts(action)[1]
    return action._to_decl()


@dataclass
class Rule:
    header: tuple[Action, ...]
    body: tuple[Fact, ...]

    def _to_decl(self) -> RuleDecl:
        return RuleDecl(
            tuple(_action_to_decl(action) for action in self.header),
            tuple(_fact_to_decl(fact) for fact in self.body),
        )
