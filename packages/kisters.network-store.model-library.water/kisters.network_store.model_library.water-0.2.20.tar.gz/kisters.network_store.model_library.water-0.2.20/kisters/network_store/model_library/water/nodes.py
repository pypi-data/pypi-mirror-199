from enum import Enum
from typing import Any, List, Optional

from kisters.network_store.model_library.base import (
    BaseNode as _BaseNode,
    Model as _Model,
)
from pydantic import Field, validator


class _Node(_BaseNode):
    domain: str = Field("water", const=True)
    name: Optional[str] = Field(
        None,
        description="Optional node name",
    )


class Junction(_Node):
    element_class: str = Field("Junction", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class LevelBoundary(_Node):
    element_class: str = Field("LevelBoundary", const=True)
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )


class FlowBoundary(_Node):
    element_class: str = Field("FlowBoundary", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class _StorageLevelVolume(_Model):
    level: float = Field(..., description="Reservoir level in m")
    volume: float = Field(
        ..., ge=0.0, description="Reservoir volume in CM (default), MCM, BCM"
    )


class _StorageLevelCapacity(_Model):
    level: float = Field(..., description="Reservoir level in m")
    capacity: float = Field(..., ge=0.0, description="Total outflow capacity in m^3/s")


class InterpEnum(str, Enum):
    linear = "linear"
    bspline = "bspline"


class Storage(_Node):
    element_class: str = Field("Storage", const=True)
    flow_boundary: Optional[bool] = Field(
        False,
        description="Optional inflow or lateral flow into the Storage node",
    )
    volume_unit: Optional[str] = Field(
        None, description="Optional volume unit: CM (default), MCM, BCM"
    )
    level_volume: List[_StorageLevelVolume] = Field(
        ...,
        description="Mandatory evel-storage table providing the "
        "storage volume per level",
        min_items=4,
    )
    level_volume_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-storage interpolation approach"
    )
    level_capacity: Optional[List[_StorageLevelCapacity]] = Field(
        None,
        description="Optional level-capacity table providing the "
        "maximum total outflow per level",
        min_items=4,
    )
    level_capacity_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-capacity interpolation approach"
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )

    @validator("level_volume")
    def check_monotonic_volume(cls, v: Any) -> Any:
        for a, b in zip(v, v[1:]):
            if a.level >= b.level:
                raise ValueError(
                    "Level must be strictly increasing ({a.level} >= {b.level})"
                )
            if a.volume >= b.volume:
                raise ValueError(
                    "Volume must be strictly increasing ({a.volume} >= {b.volume})"
                )
        return v

    @validator("level_capacity")
    def check_monotonic_capacity(cls, v: Any) -> Any:
        for a, b in zip(v, v[1:]):
            if a.level >= b.level:
                raise ValueError(
                    "Level must be strictly increasing ({a.level} >= {b.level})"
                )
            if a.capacity > b.capacity:
                raise ValueError(
                    "Volume must be increasing ({a.capacity} > {b.capacity})"
                )
        return v
