from __future__ import annotations
from time import time
from dataclasses import dataclass, fields
from typing import List, Sequence, Iterator, Tuple, Callable
import pickle
import toml

# third
import numpy as np

# local
from .features import SoundFeatures
from .records import Record, record_stats
from .augment import Aug, Augs, mk_balanced_augs


@dataclass
class DataPoint:
    # patient lookup
    record: Record
    aug: Aug
    features: SoundFeatures

    @classmethod
    def mk_augmented_points(cls, record: Record | str, augs: Augs) -> List[DataPoint]:
        """
        Create a sequance of points from single recording using augmentation
        """
        if isinstance(record, Record):
            r = record
        else:
            r = Record(record)

        data = [
            cls(r, aug, r.get_features(aug.modify)) for aug in augs if aug.apply2(r)
        ]

        return data

    def map(self, func, *args, inplace=False, **kwargs) -> DataPoint:
        """
        Create a new data by mapping data in self using func and *arg, **kwargs

        if inplace==True:
            updates self with new data
        else:
            returns new instance of Self
        """
        mfeatures = self.features.map(func, *args, **kwargs, inplace=inplace)
        if not inplace:
            return type(self)(self.record, self.aug, mfeatures)

    def pad(self, tdim: int, pad_end=False, inplace=False, **kwargs):
        pfeatures = self.features.pad(tdim, pad_end, inplace, **kwargs)
        if not inplace:
            return type(self)(self.record, self.aug, pfeatures)

    def __repr__(self) -> str:
        lines = [f"{type(self).__name__}: {id(self)}"]
        lines.extend(f"{f.name}: {getattr(self, f.name)}" for f in fields(self))
        return "\n\t".join(lines)

    def save(self, path: str):
        with open(path, mode="wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(path) -> DataPoint:
        with open(path, mode="rb") as file:
            return pickle.load(file)


def s2hms(seconds: float, decimals: int = 1) -> str:
    dt = seconds
    hms = (
        str(dt // 3600),
        str((dt % 3600) // 60),
        str(round(dt % 60, decimals)),
    )
    return ":".join(hms)


class DataSet:
    def __init__(self, data: Sequence[DataPoint]):
        self.data: Sequence[DataPoint] = data

    def __getitem__(self, s):
        if type(s) == int:
            return self.data[s]
        return type(self)(self.data[s])

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[DataPoint]:
        return iter(self.data)

    def __eq__(self, o: DataSet) -> bool:
        if len(self) != len(o):
            return False
        return all(p1 == p2 for p1, p2 in zip(self, o))

    @property
    def features(self) -> np.ndarray:
        return np.array([dp.features.values for dp in self])

    def map(self, func: Callable, *args, inplace=False, **kwargs) -> DataSet:
        """
        Create new SoundFeatures by appling func.
        if inplace:
            update inplace
        else:
            return new DataSet
        """
        if not inplace:
            return type(self)([dp.map(func, *args, **kwargs) for dp in self])
        for dp in self:
            dp.map(func, *args, **kwargs, inplace=True)

    def has_time_dim(self) -> bool:
        if len(self) == 0:
            return False
        return all(dp.features.has_tdim() for dp in self)

    def max_tdim(self) -> int:
        return max(dp.features.max_tdim() for dp in self)

    def pad(self, pad_end=False, inplace=False, **kwargs):
        """
        Pad the soundfeatures so the time dimension size the same size for all datapoints
        if inplace:
            update inplace
        else:
            return a new instance of DataSet
        """
        tdim = self.max_tdim()
        if not inplace:
            return type(self)(
                [dp.pad(tdim, pad_end, inplace=False, **kwargs) for dp in self]
            )
        for dp in self:
            dp.pad(tdim, pad_end, inplace=True, **kwargs)

    def is_time_homo(self) -> bool:
        """
        checks if all features have same time size
        """
        if not self.has_time_dim():
            return False

        if len(self) == 1:
            return True

        len1 = self[0].features.max_tdim()
        for dp in self[1:]:
            if not dp.features.is_time_homo() or (dp.features.max_tdim() != len1):
                return False
        return True

    @classmethod
    def load_wavs(cls, records=None, augs=None, s=slice(0, -1)) -> DataSet:
        if records is None:
            records = Record.load_wavs()

        if type(s) == int:
            recs = [records[s]]
        else:
            recs = records[s]

        if augs is None:
            augs = mk_balanced_augs(recs)

        n_recs = len(recs)
        for r in recs:
            print(r)
        print(f"extracting data from {n_recs} records...")
        dts = []
        data = []
        for i, r in enumerate(recs):
            t0 = time()
            data.extend(DataPoint.mk_augmented_points(r, augs))
            dt = time() - t0
            dts.append(dt)
            avg_dt = sum(dts) / len(dts)
            eta = s2hms(avg_dt * (n_recs - i))
            print(
                f"augmented datapoints: {len(data)}, processed records: {i+1}/{n_recs}, eta: {eta}"
            )
        return cls(data)

    def __repr__(self) -> str:
        lines = [f"{type(self).__name__}: {id(self)}\n---"]
        lines.extend(str(point) for point in self.data)
        return "\n\n".join(lines)

    def __str__(self) -> str:
        """
        create a summary of self
        """
        stats = record_stats([dp.record for dp in self])
        stats_str = toml.dumps(stats)
        msg = f"""
{type(self).__name__} at {id(self)}
len: {len(self)}

#stats
{stats_str}
        """
        return msg

    def reduce(self) -> DataSet:
        data = [point.reduce() for point in self.data]
        return type(self)(data)

    def save_pickle(self, path: str):
        print(f"saving data at {path}")
        with open(path, mode="wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_pickle(cls, path) -> DataSet:
        with open(path, mode="rb") as file:
            instance = pickle.load(file)
        return instance
