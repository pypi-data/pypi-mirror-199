class AbstractModifier:
    """
    engine_urls can be prefixed with modifier that slightly changes how the underlying
    DataConnector works.

    For example-
        engine_url="gz+ndjson:///data/myfile.ndjson.gz"
    Would transparently decompress on the fly.

    Modifier classes are subclasses of this `AbstractModifier` class and their :method:`apply` is
    applied to the target `DataConnector` in the same way that python decorators work behind the
    scenes-

    e.g.

    >>> a_modifer = ExampleCloudStorageModifier()
    >>> my_connector = NdjsonConnector(**some_kwargs)
    >>> my_connector = a_modifer.apply(connector=my_connector)
    """

    my_thing = "hello"

    def apply(self, connector):
        """
        Modify a data connector to use this (i.e. `self`) modifier.

        WARNING - this method mutates the connector and returns the mutated connector.

        @param connector: instance of a subclass of :class:`DataConnector`
        @return: instance of a subclass of :class:`DataConnector`
        """
        raise NotImplementedError("Must be implemented by subclasses")
