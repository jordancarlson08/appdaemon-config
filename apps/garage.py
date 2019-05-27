import appdaemon.plugins.hass.hassapi as hass
import datetime
#
# Garage Door
# Notifications and reminders
#
# Args:
#   name: name of the door
#   entity_id: entity ID of the door
#
class GarageDoor(hass.Hass):

    def initialize(self):
        self.listen_state(self.garage_state_changed, self.args["entity_id"])
        self.listen_event(self.close_garage, event="html5_notification.clicked", action="garage_close_" + self.args["entity_id"])

        self.call_service("notify/notifier_name_jordan_pixel_3", title="Garage", message="Garage App Started")


    def garage_state_changed(self, entity, attribute, old, new, kwargs):
        if (new == 'open'):
            self.handle = self.run_in(self.notify_garage_open, 300)
        else:
            self.cancel_timer(self.handle)
        time = datetime.datetime.now().time().strftime('%H:%M')
        
        if (new == 'open'):
            actionData = { "tag" : "garage_door_" + self.args["entity_id"], "actions": [ {"action": "garage_close_" + self.args["entity_id"], "title": "Close" } ] }
            notificationData = { "push": { "category": "garage" }, "entity_id": self.args["entity_id"] }
        else:
            actionData = { "tag" : "garage_door_" + self.args["entity_id"] }
            notificationData = {}
        self.call_service("notify/notifier_name_jordan_pixel_3", title="Garage", message=self.args["name"] + " " + new + " at " + time, data=actionData)


    def notify_garage_open(self, kwargs):
        actionData={"tag" : "garage_door_" + self.args["entity_id"], "actions": [ {"action": "garage_close_" + self.args["entity_id"], "title": "Close" } ] } 
        self.call_service("notify/notifier_name_jordan_pixel_3", title="Garage", message=self.args["name"] + " has been open for 5 minutes.", data=actionData)

    def close_garage(self, event_name, data, kwargs):
        if (self.get_state(self.args["entity_id"]) == 'open'):
            self.call_service("cover/close_cover", entity_id=self.args["entity_id"])