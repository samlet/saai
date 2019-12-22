class Runtime(object):
    def __init__(self):
        import os
        self.run_env=os.getenv('runtime', 'local')

    def is_docker(self):
        return self.run_env=='docker'

runtime=Runtime()
