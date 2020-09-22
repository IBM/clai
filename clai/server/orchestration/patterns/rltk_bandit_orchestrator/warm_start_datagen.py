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
            data_tids.append(f"warm-start-tid-{tid}")
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


def get_ignore_skill_warmstart_data(n_points, context_size, skill_idx):
    """ generates warm start data for always ignoring a skill behavior """

    confidence_vals = np.random.rand(n_points, context_size)

    data_tids = []
    data_contexts = []
    data_arm_rewards = []
    tid = 0

    for i in range(n_points):
        confs = confidence_vals[i]

        confs_sortidx = np.argsort(confs)
        max_confidx = confs_sortidx[-1]
        second_max_confidx = confs_sortidx[-2]

        # Negative reward on choosing the specified skill
        reward = -1.0
        data_tids.append(f"warm-start-tid-{tid}")
        data_contexts.append(list(confs))
        data_arm_rewards.append((skill_idx, reward))
        tid += 1

        # Positive reward on selecting the maximum skill
        if max_confidx != skill_idx:
            reward = +1.0
            data_tids.append(f"warm-start-tid-{tid}")
            data_contexts.append(list(confs))
            data_arm_rewards.append((max_confidx, reward))
            tid += 1
        else:
            reward = +1.0
            data_tids.append(f"warm-start-tid-{tid}")
            data_contexts.append(list(confs))
            data_arm_rewards.append((second_max_confidx, reward))
            tid += 1

    # randomise order
    idxorder = np.random.permutation(n_points)

    data_tids = [data_tids[i] for i in idxorder]
    data_contexts = [data_contexts[i] for i in idxorder]
    data_arm_rewards = [data_arm_rewards[i] for i in idxorder]

    return data_tids, np.array(data_contexts), data_arm_rewards


def get_max_skill_warmstart_data(n_points, context_size):
    """ generates warm start data for always ignoring a skill behavior """

    confidence_vals = np.random.rand(n_points, context_size)

    data_tids = []
    data_contexts = []
    data_arm_rewards = []
    tid = 0

    for i in range(n_points):
        confs = confidence_vals[i]
        maxidx = np.argmax(confs)

        for arm in range(context_size):
            data_tids.append(f"warm-start-tid-{tid}")
            reward = +1.0 if arm == maxidx else -1.0

            data_contexts.append(confs)
            data_arm_rewards.append((arm, reward))

            tid += 1

    # randomise order
    idxorder = np.random.permutation(n_points)

    data_tids = [data_tids[i] for i in idxorder]
    data_contexts = [data_contexts[i] for i in idxorder]
    data_arm_rewards = [data_arm_rewards[i] for i in idxorder]

    return data_tids, np.array(data_contexts), data_arm_rewards


# pylint: disable=too-many-locals
def get_preferred_skill_warmstart_data(
    n_points, context_size, advantage_skillidx, disadvantage_skillidx
):
    """ generates warm start data to prefer one skill over another behavior """

    confidence_vals = np.random.rand(n_points, context_size)

    data_tids = []
    data_contexts = []
    data_arm_rewards = []
    tid = 0

    for i in range(n_points):
        confs = confidence_vals[i]
        confs_sorted_idx = np.argsort(confs)

        max_conf_idx = confs_sorted_idx[-1]
        second_max_conf_idx = confs_sorted_idx[-2]

        # Unless the disadvantaged skill has the max confidence and the advantaged
        # skill has the second highest, follow the max orchestrator behavior
        if (
            max_conf_idx != disadvantage_skillidx
            and second_max_conf_idx != advantage_skillidx
        ):
            reward = +1.0
            data_tids.append(f"warm-start-tid-{tid}")
            data_contexts.append(list(confs))
            data_arm_rewards.append((max_conf_idx, reward))
            tid += 1

        # Make disadvantaged skill highest ranked, and preferred skill second highest
        confs[disadvantage_skillidx], confs[max_conf_idx] = (
            confs[max_conf_idx],
            confs[disadvantage_skillidx],
        )
        confs[advantage_skillidx], confs[second_max_conf_idx] = (
            confs[second_max_conf_idx],
            confs[advantage_skillidx],
        )

        # Negative reward for selecting disadvantaged skill if it has the
        # max confidence and the advantaged skill has the second highest
        data_tids.append(f"warm-start-tid-{tid}")
        data_contexts.append(list(confs))
        data_arm_rewards.append((disadvantage_skillidx, -1.0))
        tid += 1

        # Positive reward for selecting advantaged skill if it has the
        # second highest confidence and the disadvantaged skill has the highest
        data_tids.append(f"warm-start-tid-{tid}")
        data_contexts.append(list(confs))
        data_arm_rewards.append((advantage_skillidx, +1.0))
        tid += 1

    # randomise order
    idxorder = np.random.permutation(n_points)

    data_tids = [data_tids[i] for i in idxorder]
    data_contexts = [data_contexts[i] for i in idxorder]
    data_arm_rewards = [data_arm_rewards[i] for i in idxorder]

    return data_tids, np.array(data_contexts), data_arm_rewards


def get_warmstart_data(profile, **kwargs):

    if profile.lower() == "noop-always":
        result = get_noop_warmstart_data(**kwargs)

    elif profile.lower() == "ignore-skill":
        result = get_ignore_skill_warmstart_data(**kwargs)

    elif profile.lower() == "max-orchestrator":
        result = get_max_skill_warmstart_data(**kwargs)

    elif profile.lower() == "preferred-skill":
        result = get_preferred_skill_warmstart_data(**kwargs)

    return result
