import dataclasses


@dataclasses.dataclass
class RuleLayout:
    rule_status: str
    rule_name: str
    rule_runtime: str
    rule_children: list
