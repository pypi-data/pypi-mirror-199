from ayeaye.connectors.engine_type_modifiers.abstract_modifier import AbstractModifier


class SmartOpenModifier(AbstractModifier):
    """
    Use a sub-set of smart-open (https://pypi.org/project/smart-open/) to-
    - open s3 blobs
    - transparently compress and de-compress
    - expand file patterns using wild cards

    for all sub-classes of :class:`FilesystemConnector`.
    """

    my_thing = "this is smart open"


# >>> from smart_open import open, register_compressor
# >>> with open('smart_open/tests/test_data/1984.txt.gz', 'rb', compression='disable') as fin:
# ...     print(fin.read(32))
#
# >>> from smart_open import open, register_compressor
# >>> with open('smart_open/tests/test_data/1984.txt.gzip', compression='.gz') as fin:
# ...     print(fin.read(32))
# It was a bright cold day in Apri
