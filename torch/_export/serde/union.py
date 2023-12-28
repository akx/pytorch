from dataclasses import fields


class _Union:
    @classmethod
    def create(cls, **kwargs):
        assert len(kwargs) == 1
        obj = cls(**{**{f.name: None for f in fields(cls)}, **kwargs})  # type: ignore[arg-type]
        obj._type = list(kwargs.keys())[0]
        return obj

    def __post_init__(self):
        assert not any(f.name in ("type", "_type", "create", "value") for f in fields(self))  # type: ignore[arg-type, misc]

    @property
    def type(self) -> str:
        try:
            return self._type
        except AttributeError as e:
            raise RuntimeError(f"Please use {type(self).__name__}.create to instantiate the union type.") from e

    @property
    def value(self):
        return getattr(self, self.type)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if attr is None and name in set(f.name for f in fields(type(self))) and name != self.type:
            raise AttributeError(f"Field {name} is not set.")
        return attr

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{type(self).__name__}({self.type}={getattr(self, self.type)})"
