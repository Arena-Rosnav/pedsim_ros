import sismic.model
import sismic.io
import sismic.interpreter

import dynamic_reconfigure.client

import typing
import enum

import numpy as np
import numpy.typing as npt
from pedsim_agents.utils import InData, WorkData

import rospy

class Range(typing.NamedTuple):
    MIN: float = 0
    MAX: float = 100
    DEFAULT: float = 50

    @classmethod
    def parse(cls, *args: float) -> "Range":
        if len(args) == 0: return cls() 
        if len(args) == 1: return cls(DEFAULT=args[0])
        if len(args) == 2: return cls(MIN=args[0], MAX=args[1], DEFAULT=(args[1]-args[0])/2)
        return cls(MIN=args[0], MAX=args[1], DEFAULT=args[2]) 


class StatechartProvider:
    @classmethod
    def load(cls, filepath: str):
        def wrapper(inner: typing.Type[Pedestrian]):
            class Wrapped(inner):
                __statechart: sismic.model.Statechart

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.__statechart = sismic.io.import_from_yaml(filepath=filepath)

                @property
                def statechart(self):
                    return self.__statechart
            
            return Wrapped
        return wrapper
    
    @property
    def statechart(self) -> sismic.model.Statechart:
        raise NotImplementedError(f"{type(self).__name__} has no associated statechart")


class Pedestrian(StatechartProvider):

    _config: typing.Dict
    _runtime: typing.Dict
    _state: typing.Dict
    _animation: str

    def __init__(self, id: str, config: typing.Dict):

        self._config = dict()

        self._runtime = dict(
            id = id,
            f = float(rospy.get_param("pedsim_simulator/update_rate")),
            dt = 1 / float(rospy.get_param("pedsim_simulator/update_rate")),
            rng = np.random.default_rng(None)
        )

        self._state = dict()

        #dynamic_reconfigure.client.Client("")

        self._animation = ""

    def setup(self) -> "Pedestrian":
        self._statemachine = sismic.interpreter.Interpreter(
            self.statechart,
            initial_context=dict(
                config = self._config,
                runtime = self._runtime,
                state = self._state
            )
        )
        self._statemachine.bind(self.event_handler)
        return self

    def event_handler(self, event: sismic.model.Event):
        if event.name == "animation":
            self._animation = str(event.data.get("animation"))
        else:
            pass

    def tick(self, *data: str):
        for event in (*data, "tick"):
            self._statemachine.queue(event).execute_once()

    def post(self, in_data: InData, work_data: WorkData, i: int):
        work_data.social_state[i] = self._animation

from .main import PedsimStates #noqa