def func(func_, *args, **kwargs) -> dict:
    return {"func": func_, "args": [*args], "kwargs": dict(**kwargs)}


def run(_: dict, **kwargs):
    return _["func"](
        *_["args"],
        **(
            {
                **_["kwargs"],
                **(dict(**kwargs))
            }
        )
    )
