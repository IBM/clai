#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

from clai.server.logger import current_logger as logger
import pandas as pd
import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from PIL import Image


class DATAXPLORE(Agent):
    def __init__(self):
        super(DATAXPLORE, self).__init__()
        # self.service = Service()

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        try:
            logger.info("Command passed in dataxplore: " + command)
            commandStr = str(command)
            commandTokenized = commandStr.split(" ")
            if len(commandTokenized) == 2:
                if commandTokenized[0] == "summarize":
                    fileName = commandTokenized[1]
                    csvFile = fileName.split(".")
                    if len(csvFile) == 2:
                        if csvFile[1] == "csv":
                            path = os.path.abspath(fileName)
                            data = pd.read_csv(path)
                            df = pd.DataFrame(data)
                            response = df.describe().to_string()
                        else:
                            response = "We currently support only csv files. Please, Try >> clai dataxplore summarize csvFileLocation "
                    else:
                        response = "Not a supported file format. Please, Try >> clai dataxplore summarize csvFileLocation "
                elif commandTokenized[0] == "plot":
                    fileName = commandTokenized[1]
                    csvFile = fileName.split(".")
                    if len(csvFile) == 2:
                        if csvFile[1] == "csv":
                            plt.close("all")
                            path = os.path.abspath(fileName)
                            data = pd.read_csv(path, index_col=0, parse_dates=True)
                            data.plot()
                            plt.savefig("/tmp/claifigure.png")
                            im = Image.open("/tmp/claifigure.png")
                            im.show()
                            response = "Please, check the popup for figure."
                        else:
                            response = "We currently support only csv files. Please, Try >> clai dataxplore plot csvFileLocation "
                    else:
                        response = "Not a supported file format. Please, Try >> clai dataxplore plot csvFileLocation "
                else:
                    response = "Try >> clai dataxplore function fileLocation "
            else:
                response = "Few parts missing. Please, Try >> clai dataxplore function fileLocation "

            confidence = 0.0

            return Action(
                suggested_command=NOOP_COMMAND,
                execute=True,
                description=Colorize().info().append(response).to_console(),
                confidence=confidence,
            )

        except Exception as ex:
            return [{"text": "Method failed with status " + str(ex)}, 0.0]
