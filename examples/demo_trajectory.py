import numpy as np
import pybullet

from handover.utils.cmd import set_config_from_args
from handover.envs.handover_env import HandoverEnv

scene_id = 105

start_conf = np.array([
    -0.0593, -1.6124, -0.1970, -2.5300, -0.0952, +1.6780, +0.587, +0.0400, +0.0400,
])

traj = np.array([
    [-0.1528, -1.5523, -0.1171, -2.5378, -0.0192, +1.6908, +0.4985, +0.0400, +0.0400],
    [-0.2446, -1.4955, -0.0390, -2.5454, +0.0602, +1.7035, +0.4076, +0.0400, +0.0400],
    [-0.3346, -1.4370, +0.0375, -2.5528, +0.1428, +1.7162, +0.3145, +0.0400, +0.0400],
    [-0.4231, -1.3759, +0.1124, -2.5601, +0.2284, +1.7288, +0.2194, +0.0400, +0.0400],
    [-0.5102, -1.3124, +0.1858, -2.5672, +0.3168, +1.7414, +0.1225, +0.0400, +0.0400],
    [-0.5960, -1.2467, +0.2580, -2.5742, +0.4077, +1.7540, +0.0238, +0.0400, +0.0400],
    [-0.6806, -1.1791, +0.3290, -2.5810, +0.5008, +1.7665, -0.0764, +0.0400, +0.0400],
    [-0.7641, -1.1097, +0.3990, -2.5878, +0.5960, +1.7791, -0.1779, +0.0400, +0.0400],
    [-0.8467, -1.0387, +0.4680, -2.5944, +0.6930, +1.7916, -0.2807, +0.0400, +0.0400],
    [-0.9285, -0.9664, +0.5362, -2.6010, +0.7915, +1.8040, -0.3846, +0.0400, +0.0400],
    [-1.0096, -0.8930, +0.6037, -2.6074, +0.8914, +1.8165, -0.4893, +0.0400, +0.0400],
    [-1.0838, -0.8196, +0.6762, -2.6098, +0.9923, +1.8277, -0.5972, +0.0400, +0.0400],
    [-1.1572, -0.7456, +0.7485, -2.6115, +1.0942, +1.8388, -0.7058, +0.0400, +0.0400],
    [-1.2267, -0.6724, +0.8235, -2.6059, +1.1963, +1.8502, -0.8161, +0.0400, +0.0400],
    [-1.2944, -0.5992, +0.8995, -2.5978, +1.2986, +1.8616, -0.9271, +0.0400, +0.0400],
    [-1.3619, -0.5261, +0.9757, -2.5891, +1.4010, +1.8729, -1.0382, +0.0400, +0.0400],
    [-1.4286, -0.4532, +1.0534, -2.5801, +1.5029, +1.8842, -1.1493, +0.0400, +0.0400],
    [-1.4944, -0.3811, +1.1323, -2.5689, +1.6046, +1.8953, -1.2601, +0.0400, +0.0400],
    [-1.5597, -0.3097, +1.2125, -2.5572, +1.7056, +1.9064, -1.3706, +0.0400, +0.0400],
    [-1.6250, -0.2391, +1.2938, -2.5453, +1.8056, +1.9175, -1.4805, +0.0400, +0.0400],
    [-1.6876, -0.1697, +1.3792, -2.5329, +1.9036, +1.9285, -1.5896, +0.0400, +0.0400],
    [-1.7500, -0.1015, +1.4663, -2.5203, +2.0001, +1.9395, -1.6979, +0.0400, +0.0400],
    [-1.8117, -0.0350, +1.5551, -2.5074, +2.0950, +1.9498, -1.8055, +0.0400, +0.0400],
    [-1.8765, +0.0316, +1.6431, -2.4933, +2.1882, +1.9592, -1.9117, +0.0400, +0.0400],
    [-1.9426, +0.0964, +1.7324, -2.4793, +2.2794, +1.9693, -2.0163, +0.0400, +0.0400],
    [-2.0085, +0.1582, +1.8246, -2.4641, +2.3687, +1.9803, -2.1190, +0.0400, +0.0400],
    [-1.9812, +0.0670, +1.8150, -2.4308, +2.4190, +1.9478, -2.0687, +0.0400, +0.0400],
    [-1.9811, -0.0292, +1.8288, -2.3966, +2.4714, +1.9170, -2.0122, +0.0400, +0.0400],
    [-1.9973, -0.1114, +1.8576, -2.3592, +2.5184, +1.8992, -1.9623, +0.0400, +0.0400],
    [-2.0184, -0.1788, +1.8898, -2.3187, +2.5586, +1.8933, -1.9206, +0.0400, +0.0400],
], dtype=np.float32)

num_action_repeat = 130


def main():
  set_config_from_args()

  env = HandoverEnv(is_render=True)

  while True:
    env.reset(scene_id)

    for _ in range(3000):
      action = start_conf
      env.step(action)

    for i in range(len(traj)):
      action = traj[i]
      for _ in range(num_action_repeat):
        env.step(action)

    for _ in range(200):
      action = traj[-1].copy()
      action[-2:] = 0.0
      env.step(action)

    pos = pybullet.getLinkState(env._panda.body_id, env._panda.LINK_IND_HAND)[4]
    for i in range(10):
      pos = (pos[0], pos[1] - 0.03, pos[2])
      action = np.array(pybullet.calculateInverseKinematics(
          env._panda.body_id, env._panda.LINK_IND_HAND, pos),
                        dtype=np.float32)
      action[-2:] = 0.0
      for _ in range(num_action_repeat):
        env.step(action)


if __name__ == '__main__':
  main()
