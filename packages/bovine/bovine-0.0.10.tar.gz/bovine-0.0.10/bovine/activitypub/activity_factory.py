from bovine.activitystreams.activities import build_accept, build_create, build_like


class ActivityFactory:
    def __init__(self, actor_information):
        self.information = actor_information

    def create(self, note):
        return build_create(note)

    def like(self, target):
        return build_like(self.information["id"], target)

    def accept(self, obj):
        return build_accept(self.information["id"], obj)
