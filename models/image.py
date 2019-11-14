from config import Config
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    image_path = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_url(self):
        return Config.S3_LOCATION + self.image_path