class SaaiConf(object):
    @property
    def runtime_dir(self):
        """
        >>> from saai.saai_conf import saai_conf
        >>> saai_conf.runtime_dir
        :return:
        """
        import os
        return os.path.dirname(__file__)

saai_conf=SaaiConf()

