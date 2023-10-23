import hashlib

from lfr.netlistgenerator.primitive import Primitive, PrimitiveType


class ConnectionPrimitive(Primitive):
    """
    Connection primitive class.
    """

    def __init__(self, mint: str = "") -> None:
        """Initializes the connection primitive.

        Args:
            mint (str, optional): MINT string to initialize the connection primitive. Defaults to "".
        """
        super().__init__(mint)
        self._type = PrimitiveType.CONNECTION
        self._uid = hashlib.md5(f"{self._mint}".encode("utf-8")).hexdigest()

    @property
    def mint(self) -> str:
        """Returns the MINT string for the connection primitive.

        Returns:
            str: MINT string for the connection primitive
        """
        return self._mint

    @property
    def uid(self) -> str:
        """Returns the UID of the connection primitive.

        Returns:
            str: UID of the connection primitive
        """
        return self._uid
