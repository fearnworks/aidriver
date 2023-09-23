from enum import StrEnum
from ai_driver.flows.swarm import SwarmConfig


class OAIModels(StrEnum):
    GPT4 = ("gpt-4",)
    GPT3_5_Turbo_16k = "gpt-3.5-turbo-16k"
    GPT3_5_Turbo = "gpt-3.5-turbo"


default_swarm_config = SwarmConfig(
    num_agents=3,
    max_response_tokens=7000,
    final_response_length=2000,
    iterations=2,
    system_message_model=OAIModels.GPT4,
    answer_generation_model=OAIModels.GPT3_5_Turbo,
    answer_iteration_model=OAIModels.GPT3_5_Turbo_16k,
    response_aggregation_model=OAIModels.GPT3_5_Turbo_16k,
    temperature=0.4,
)
