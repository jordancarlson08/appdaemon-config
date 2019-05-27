import appdaemon.plugins.hass.hassapi as hass
#
# Garage Door
# Notifications and reminders
#
# Args:
#   name: name of the door
#   entity_id: entity ID of the door
#
class MultiTap(hass.Hass):

    def initialize(self):
        self.listen_event(self.evaluate_click, event="zwave.scene_activated")


    def evaluate_click(self, entity, attribute, old, new, kwargs):
        if (new == 'open'):
            self.handle = self.run_in(self.notify_garage_open, 300)
        else:
            self.cancel_timer(self.handle)