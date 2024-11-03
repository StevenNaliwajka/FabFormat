from CodeBase.fileIO.CommonFormat.CFLayer.layer_parent import LayerParent


class AdditiveLayer(LayerParent):
    def __init__(self, layer_number):
        super().__init__(layer_number)
        self.layer_type = "a"
