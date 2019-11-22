import sagas

class ProcsTests(object):
    def test_df(self):
        """
        $ python -m procs_tests test_df
        :return:
        """
        sagas.print_rs([('tom', 5)], ['name', 'age'])

if __name__ == '__main__':
    import fire
    fire.Fire(ProcsTests)
