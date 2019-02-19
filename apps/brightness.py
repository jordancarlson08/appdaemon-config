import appdaemon.plugins.hass.hassapi as hass
#
# Brightness
# Set automatic brightness level at certain times
#
# Args:
#   entity_id: entity Id of the light
#   brightness: level between 0-255
#   start: time ex "21:00:00"
#   stop: time ex "06:00:00"
#
class Brightness(hass.Hass):

    def initialize(self):
        self.listen_state(self.lights_on, self.args["entity_id"], new = "on", old="off")

    def lights_on(self, entity, attribute, old, new, kwargs):
        if self.now_is_between(self.args["start"], self.args["stop"]):
            self.turn_on(self.args["entity_id"], brightness = self.args["brightness"])