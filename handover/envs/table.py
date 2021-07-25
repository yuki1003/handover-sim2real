import os


class Table():
  HEIGHT = 0.92

  _COLLISION_ID = 2**0

  def __init__(self,
               bullet_client,
               base_position=[0, 0, 0],
               base_orientation=[0, 0, 0, 1]):
    self._p = bullet_client
    self._base_position = base_position
    self._base_orientation = base_orientation

    urdf_file = os.path.join(os.path.dirname(__file__), "..", "data", "assets",
                             "table", "table.urdf")
    self._body_id = self._p.loadURDF(urdf_file,
                                     basePosition=self._base_position,
                                     baseOrientation=self._base_orientation)

    self._p.changeVisualShape(self._body_id, -1, rgbaColor=[1, 1, 1, 1])

    self._p.setCollisionFilterGroupMask(self._body_id, -1, self._COLLISION_ID,
                                        self._COLLISION_ID)

  @property
  def body_id(self):
    return self._body_id
