from typing import Dict, Any, TypeVar, Type, Literal

T = TypeVar("T")  # any type
RT = TypeVar("RT")  # any func return type
MT = TypeVar("MT", bound="StorableModel")  # model type
MC = TypeVar("MC", bound=Type["StorableModel"])  # model class

QueryType = Dict[str, Any]
QueryExpression = str | QueryType

CommonDict = Dict[str, Any]
KwArgs = CommonDict
EnvironmentType = Literal["development", "testing", "staging", "production"]
