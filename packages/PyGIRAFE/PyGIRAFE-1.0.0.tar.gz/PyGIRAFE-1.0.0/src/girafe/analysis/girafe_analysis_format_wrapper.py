from abc import ABC, abstractmethod, abstractproperty


class GirafeAnalysisFormatWrapper(ABC):
    """
    An abstract class that should be inherit in order to create a specific format wrapper
    Two constants should be added on the classe WRAPPER_ID and DATA_FORMAT

    """

    def __init__(self, data_ref, data_format, load_data=True):
        """

        Args:
            data_ref: A reference to the data to analyse. It could be the data directly instantiate.
            But more commonly, it would a file_name or a directory. Will be used by load_data method to load the data.
            load_data: load the data in the __init__ methods, otherwise the user will have to call load_data()
        """
        super().__init__()
        self._data_ref = data_ref
        self.load_data_at_init = load_data
        self._data_format = data_format
        self.data_loaded = False

    @staticmethod
    @abstractmethod
    def is_data_valid(data_ref):
        """
        Check if the data can be an input for this wrapper as data_ref
        Args:
            data_ref: file or directory

        Returns: a boolean

        """
        pass

    @property
    def data_format(self):
        return self._data_format

    def load_data(self):
        """
        Load data in memory
        Returns:

        """
        self.data_loaded = True

    @staticmethod
    def grouped_by():
        """
        Indicate by which factor the data can be grouped
        ex: age, species, contains behavior, categories of age..
        :return: a dictionary with key the name of the group (str) that will be displayed in the GUI, and as value
        the a sring representing either an argument or a method of the wrapper class (hasattr() and callable() will be
        use to get them)
        """

        return dict()

    # it's only needed to provide an implementation only for the getter in the class works and allows for instantiation
    @property
    @abstractmethod
    def identifier(self):
        """
        Identifier of the session
        :return:
        """
        pass

    @property
    def data_ref(self):
        """
        Return the path of the file or directory corresponding to this data session
        :return:
        """
        return self._data_ref
