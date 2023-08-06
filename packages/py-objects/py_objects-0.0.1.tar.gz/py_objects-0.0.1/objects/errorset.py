from types import MethodType


class BaseError(Exception):
    ...


def ErrorSet(setname, *errors):
    setclass = type(setname, (BaseError,), {})
    setclass.graphene = MethodType(graphene, setclass)

    setclass.errormap = dict()
    for error in errors:
        leafclass = type(error, (setclass,), dict(parent=setclass))
        leafclass.name = leafclass.__name__
        setclass.errormap[error] = leafclass
        setattr(setclass, error, leafclass)

    return setclass
