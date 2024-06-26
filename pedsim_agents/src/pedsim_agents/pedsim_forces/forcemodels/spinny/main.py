import numpy as np
from pedsim_agents.pedsim_forces import PedsimForcemodel, ForcemodelName, Forcemodel
from pedsim_agents.utils import FeedbackDatum, FeedbackData
import pedsim_msgs.msg

@PedsimForcemodel.register(ForcemodelName.SPINNY)
class Plugin_Spinny(Forcemodel):

    offset = 30

    def __init__(self):
        ...

    def callback(self, data) -> FeedbackData:
        
        def datapoint_to_vec(agent: pedsim_msgs.msg.AgentState) -> FeedbackDatum:
            
            angle = agent.direction
            velocity = np.linalg.norm(np.array([agent.twist.linear.x, agent.twist.linear.y]))

            feedback = pedsim_msgs.msg.AgentFeedback()

            feedback.id = agent.id
            feedback.force.x = np.cos(angle + self.offset * np.pi/180) * velocity
            feedback.force.y = np.sin(angle + self.offset * np.pi/180) * velocity

            return FeedbackDatum(feedback)

        return [datapoint_to_vec(agent) for agent in data.agents]