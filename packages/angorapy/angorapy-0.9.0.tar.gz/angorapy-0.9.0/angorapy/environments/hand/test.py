import angorapy as ang
import numpy as np

from angorapy import get_model_builder, make_env
from angorapy.analysis.investigation import Investigator

agent = ang.agent.PPOAgent(get_model_builder("shadow", "rnn"), make_env("ReachAbsolute-v0"), )
investigator = Investigator.from_agent(agent)

investigator.render_episode(agent.env)