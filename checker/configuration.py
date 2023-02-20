"""
Contains features for load settings
"""
from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    from_date: str
    to_date: str
    update_period: int
    sample_time: str
    print_detailed_info: bool


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    # load configuration from file
    return Config(
        from_date=env.str('FROM_DATE'),
        to_date=env.str('TO_DATE'),
        update_period=env.int('UPDATE_PERIOD'),
        sample_time=env.str('SAMPLE_TIME'),
        print_detailed_info=env.bool('PRINT_DETAILED_INFO')
    )
