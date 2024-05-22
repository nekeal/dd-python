from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    type: str

    @staticmethod
    def skill(name: str) -> "Capability":
        return Capability(name, "SKILL")

    @staticmethod
    def permission(name: str) -> "Capability":
        return Capability(name, "PERMISSION")

    @staticmethod
    def asset(asset: str) -> "Capability":
        return Capability(asset, "ASSET")
