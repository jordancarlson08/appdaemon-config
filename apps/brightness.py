import appdaemon.plugins.hass.hassapi as hass
#
# Brightness
# Set automatic brightness level at certain times
#
# Args:
#   entity_id: entity ID of the light
#
class Brightness(hass.Hass):

    def initialize(self):
        self.listen_state(self.lights_on, self.args["entity_id"], new = "on")

    def lights_on(self, entity, attribute, old, new, kwargs):
        if self.now_is_between("21:00:00", "06:00:00"):
            self.turn_on(self.args["entity_id"], brightness = 50)