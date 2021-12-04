from marshmallow import Schema, fields, post_load
from marshmallow.utils import get_value, set_value


class Reach(fields.Field):
    def __init__(self, inner, path, **kwargs):
        super().__init__(**kwargs)
        self.inner = inner
        self.path = path

    def _deserialize(self, value, attr, data, **kwargs):
        val = get_value(value, self.path)
        return self.inner.deserialize(val, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        val = self.inner._serialize(value, attr, obj, **kwargs)
        ret = {}
        set_value(ret, self.path, val)
        return ret


class ProductInfo(Schema):
    id = fields.Str(data_key="Id")
    name = fields.Str(data_key="Name")
    image_url = Reach(fields.Str(), path="B", data_key="Pic")
    price = Reach(fields.Int(), path="P", data_key="Price")

    @post_load
    def add_base_address(self, data, **kwargs):
        data["image_url"] = "https://d.ecimg.tw" + data["image_url"]
        return data


class ProductDescription(Schema):
    description = fields.Str(data_key="Slogan")

    @post_load
    def convert_newline_symbol_to_unix_format(self, data, **kwargs):
        data["description"] = data["description"].replace("\r\n", "\n")
        return data


class ProductStatus(Schema):
    quantity = fields.Int(data_key="Qty")
    status = fields.Function(
        deserialize=lambda value: ("現貨" if int(value) else "缺貨中"),
        data_key="SaleStatus",  # noqa: E501
    )
