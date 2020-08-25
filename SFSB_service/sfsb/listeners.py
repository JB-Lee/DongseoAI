import numpy as np
from keras import models

import cortex
from global_variable import Config


class PowerListener(cortex.Listener):
    cols: list
    state = list()
    __current_state = np.zeros((5, 5))
    __state_size = Config.config.get("Metric.Focus.State_Size")
    model = models.load_model(Config.config.get("Metric.Focus.Model"))

    def __init__(self):
        pass

    @cortex.Listener.handler(cortex.ID.SUBSCRIPTION.SUBSCRIBE)
    def handle_subscribe(self, data):
        for stream in data["success"]:
            if stream["streamName"] == "pow":
                self.cols = stream["cols"]

    @cortex.Listener.handler("pow")
    def handle_pow(self, data):
        if len(self.state) > self.__state_size:
            self.state.pop(0)
        self.__current_state = np.array(data["pow"]).reshape(5, 5)
        self.state.append(self.model.predict([data["pow"]])[0][0])

    @property
    def metric(self):
        if len(self.state) <= 0:
            return False
        return np.min(self.state) < Config.config.get("Metric.Focus.Threshold")

    @property
    def data(self):
        return self.__current_state


class MetricListener(cortex.Listener):
    cols: list
    state: dict

    def __init__(self):
        pass

    @cortex.Listener.handler(cortex.ID.SUBSCRIPTION.SUBSCRIBE)
    def handle_subscribe(self, data):
        for stream in data["success"]:
            if stream["streamName"] == "met":
                self.cols = stream["cols"]

    @cortex.Listener.handler("met")
    def handle_metric(self, data):
        self.state = {k: v for (k, v) in zip(self.cols, data["met"])}

    @property
    def metric(self):
        if not hasattr(self, "state"):
            return False

        stress = self.state["str"]
        exc = self.state["exc"]
        rel = self.state["rel"]

        if not (stress and exc and rel):
            return False

        return (stress + exc) / rel > Config.config.get("Metric.Exc.Threshold")


class MotionListener(cortex.Listener):
    cols: list

    def __init__(self, callback):
        self.callback = callback

    @cortex.Listener.handler(cortex.ID.SUBSCRIPTION.SUBSCRIBE)
    def handle_subscribe(self, data):
        for stream in data["success"]:
            if stream["streamName"] == "mot":
                self.cols = stream["cols"]

    @cortex.Listener.handler("mot")
    def handle_metric(self, data):
        dat = {k: v for (k, v) in zip(self.cols, data["mot"])}
        self.callback(dat)
