from json import dumps


class CourseLocationVo:
    location_name = ""
    location_url = ""
    location_address = ""
    location_longitude = 0
    location_latitude = 0
    location_score = 0.00
    location_type = ""

    def __init__(
        self,
        location_name,
        location_url,
        location_address,
        location_score,
        location_type,
    ):
        self.location_name = location_name
        self.location_url = location_url
        self.location_address = location_address
        self.location_score = location_score
        self.location_type = location_type

    def setLongitude_setLatitude(self, longitude, latitude):
        self.location_longitude = longitude
        self.location_latitude = latitude

    @property
    def json(self):
        return {
            "location_name": self.location_name,
            "location_url": self.location_url,
            "location_address": self.location_address,
            "location_longitude": self.location_longitude,
            "location_latitude": self.location_latitude,
            "location_score": self.location_score,
            "location_type": self.location_type,
        }
