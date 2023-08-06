from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, overload

from vstools import (ColorRange, ColorRangeT, CustomIntEnum, CustomRuntimeError, FuncExceptT,
                     FunctionUtil, PlanesT, core, fallback, inject_self, normalize_seq, vs)

from .abstract import Debander

__all__ = [
    'SampleMode',

    'F3kdb'
]


if TYPE_CHECKING:
    class Algorithm(CustomIntEnum):
        OLD = 0
        UNIFORM = 1
        GAUSSIAN = 2

        @overload
        def __call__(  # type: ignore
            self: Literal[GAUSSIAN], sigma: float = 1.0, grain_sigma: float = 1.0
        ) -> SampleModeAlgorithmWithInfo:
            ...

        @overload
        def __call__(self) -> SampleModeAlgorithmWithInfo:
            ...

        def __call__(self, *args: Any) -> Any:  # type: ignore
            ...


def _create_Algorithm(sample_mode: SampleMode | SampleModeMidDiffInfo) -> type[Algorithm]:
    class inner_algorithm(CustomIntEnum):
        OLD = 0
        UNIFORM = 1
        GAUSSIAN = 2

        def __call__(  # type: ignore
            self: Literal[GAUSSIAN], sigma: float = 1.0, grain_sigma: float = 1.0
        ) -> SampleModeAlgorithmWithInfo:
            return SampleModeAlgorithmWithInfo(self, sample_mode, sigma, grain_sigma)  # type: ignore

    return inner_algorithm  # type: ignore


class SampleModeBase:
    if TYPE_CHECKING:
        Algorithm: type[Algorithm]
    else:
        @property
        def Algorithm(self) -> type[Algorithm]:
            return _create_Algorithm(self)


@dataclass
class SampleModeMidDiffInfo(SampleModeBase):
    sample_mode: SampleMode
    thr_mid: int | list[int]
    thr_max: int | list[int]


@dataclass
class SampleModeAlgorithmWithInfo:
    algo: Algorithm
    sample_mode: SampleMode | SampleModeMidDiffInfo
    sigma: float = 1.0
    grain_sigma: float = 1.0


class SampleMode(SampleModeBase, CustomIntEnum):
    COLUMN = 1
    """Take 2 pixels as reference pixel. Reference pixels are in the same column of current pixel."""

    SQUARE = 2
    """Take 4 pixels as reference pixel. Reference pixels are in the square around current pixel."""

    ROW = 3
    """Take 2 pixels as reference pixel. Reference pixels are in the same row of current pixel."""

    COL_ROW_MEAN = 4
    """Arithmetic mean of COLUMN and ROW. Reference points are randomly picked within the range."""

    MEAN_DIFF = 5
    """Similar to COL_ROW_MEAN, adds max/mid diff thresholds."""

    def __call__(  # type: ignore
        self: Literal[MEAN_DIFF], thr_mid: int | list[int], thr_max: int | list[int]
    ) -> SampleModeMidDiffInfo:
        return SampleModeMidDiffInfo(self, thr_mid, thr_max)


SampleModeT = SampleMode | SampleModeMidDiffInfo | SampleModeAlgorithmWithInfo


@dataclass
class F3kdb(Debander):
    """Debander wrapper around the f3kdb plugin."""

    radius: int | None = None
    thr: int | list[int] | None = None
    grains: int | list[int] | None = None

    sample_mode: SampleModeT | None = None

    seed: int | None = None
    dynamic_grain: int | None = None

    blur_first: bool | None = None

    def __post_init__(self) -> None:
        super().__post_init__()

        self.config = Debander.SupportsConfig(True, True, False)

    @inject_self
    def deband(  # type: ignore[override]
        self, clip: vs.VideoNode,
        radius: int = 16,
        thr: int | list[int] = 96,
        grains: int | list[int] = 0,
        sample_mode: SampleModeT = SampleMode.SQUARE,
        dynamic_grain: int | None = None,
        blur_first: bool | None = None,
        color_range: ColorRangeT | None = None,
        seed: int | None = None,
        planes: PlanesT = None,
        _func: FuncExceptT | None = None
    ) -> vs.VideoNode:
        func = FunctionUtil(clip, _func or self.deband, planes, (vs.GRAY, vs.YUV), range(8, 16))

        if not hasattr(core, 'neo_f3kdb'):
            raise CustomRuntimeError('You are missing the neo_f3kdb plugin!', func.func)

        if 'y_2' not in core.neo_f3kdb.Deband.__signature__.parameters:  # type: ignore
            raise CustomRuntimeError('You are using an outdated version of neo_f3kdb, upgrade now!', func.func)

        radius = fallback(self.radius, radius)

        y, cb, cr = func.norm_seq(fallback(self.thr, thr))
        gry, grc = normalize_seq(fallback(self.grains, grains), 2)

        sample_mode = fallback(self.sample_mode, sample_mode)  # type: ignore

        color_range = ColorRange.from_param(
            color_range, self.deband
        ) or ColorRange.from_video(func.work_clip, func=func.func)

        random_algo_ref = 1
        random_param_ref = random_param_grain = 1.0

        if isinstance(sample_mode, SampleModeAlgorithmWithInfo):
            random_param_ref, random_param_grain = sample_mode.sigma, sample_mode.grain_sigma
            random_algo_ref = sample_mode.algo.value
            sample_mode = sample_mode.sample_mode

        y1 = cb1 = cr1 = y2 = cb2 = cr2 = None

        if isinstance(sample_mode, SampleModeMidDiffInfo):
            y1, cb1, cr1 = func.norm_seq(sample_mode.thr_mid)
            y2, cb2, cr2 = func.norm_seq(sample_mode.thr_max)
            sample_mode = sample_mode.sample_mode

        blur_first = fallback(self.blur_first or blur_first, max(y, cb, cr) < 2048)  # type: ignore

        debanded = core.neo_f3kdb.Deband(
            func.work_clip, radius, y, cb, cr, gry, grc,  # type: ignore
            sample_mode.value, self.seed or seed, blur_first, self.dynamic_grain or dynamic_grain,
            None, None, None, color_range.is_limited, 16, random_algo_ref, random_algo_ref,
            random_param_ref, random_param_grain, None, y1, cb1, cr1, y2, cb2, cr2, True
        )

        return func.return_clip(debanded)

    @inject_self
    def grain(  # type: ignore[override]
        self, clip: vs.VideoNode, strength: int | tuple[int, int] = 4, dynamic: bool | int = True,
        radius: int = 16, sample_mode: SampleMode = SampleMode.SQUARE,
        color_range: ColorRangeT | None = None, seed: int | None = None, planes: PlanesT = None
    ) -> vs.VideoNode:
        return self.deband(
            clip, radius, [1, 1, 1],
            strength, sample_mode, dynamic, None, color_range, seed, planes  # type: ignore
        )
