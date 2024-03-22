import os


class EnvironmentUtils:

    @staticmethod
    def get_env(env_name: str):
        if env_name not in os.environ or not os.environ[env_name]:
            raise RuntimeError(
                "{} variable not configured in environment!".format(env_name)
            )
        return os.environ[env_name]
