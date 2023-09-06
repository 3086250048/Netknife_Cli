class Object_Exec:
    def __init__(self,protocol='ping',address=None,port=None,param=None) -> None:
        self.protocol=protocol
        self.address=address
        self.port=port
        self.param=param