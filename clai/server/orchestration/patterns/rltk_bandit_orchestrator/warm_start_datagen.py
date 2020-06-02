import numpy as np


def get_noop_warmstart_data(n_points, context_size, noop_position):
    """ generates warm start data for noop behavior """

    confidence_vals = np.random.rand(n_points, context_size)

    data_tids = []
    data_contexts = []
    data_arm_rewards = []
    tid = 0

    for i in range(n_points):
        confs = confidence_vals[i]

        for arm in range(context_size):
            data_tids.append(f'warm-start-tid-{tid}')
            reward = 1.0 if arm == noop_position else -1.0

            data_contexts.append(confs)
            data_arm_rewards.append((arm, reward))

            tid += 1

    # randomise order
    idxorder = np.random.permutation(n_points)

    data_tids = [data_tids[i] for i in idxorder]
    data_contexts = [data_contexts[i] for i in idxorder]
    data_arm_rewards = [data_arm_rewards[i] for i in idxorder]

    return data_tids, np.array(data_contexts), data_arm_rewards


def get_warmstart_data(profile, **kwargs):

    if profile.lower() == 'noop-always':
        return get_noop_warmstart_data(**kwargs)
