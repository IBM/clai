#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

#!/usr/bin/env python

'''
Implement calls to your favorite planners here.
'''

from urllib import request, parse
import json, requests

'''
globals
'''
_planning_domains = 'http://solver.planning.domains/solve'
_pr2plan_hostname = 'http://ae-robots.com:3456'

'''
method :: agile planner on the cloud / no observations
note   :: this makes a call to planning.domains: http://planning.domains/
'''
def get_plan_from_christian(domain: str, problem: str) -> list:
    try:

        data = parse.urlencode({"domain": domain, "problem": problem}).encode()
        req = request.Request(_planning_domains, data=data)
        res = json.loads(request.urlopen(req).read())

        # warning :: planners don't always use standards, every response has to be parsed it's own way
        plan = [act['name'][1:-1].replace('-', '_') for act in res['result']['plan']]
        return plan

    except Exception as e:
        print(e)


'''
method :: optimal planner with observations
note   :: this uses the pr2plan compilation before calling FAST-DOWNWARD
----------------------------------------------------------------------
pr2plan --> https://sites.google.com/site/prasplanning/file-cabinet
FAST-DOWNWARD --> http://www.fast-downward.org/
'''
def get_plan_from_pr2plan(domain: str, problem: str, obs: list, q: list = None) -> list:
    try:

        obs_format = '\n'.join(['({})'.format(o) for o in obs])
        # note :: additional entry for observations used by pr2plan compilation
        output = requests.put(_pr2plan_hostname + '/solve', json={"domain": domain, "problem": problem, "obs": obs_format}, timeout=3).json()

        # warning :: planners don't always use standards, every response has to be parsed it's own way
        plan = [action.strip()[1:-4] if '_1' in action else action[1:-2] for action in
                output["fd-output"].strip().split('\n')[:-1]]

        # note :: the following is going to only return the actionable items after the LAST explained observation
        # note :: should ideally be replaced by an investigation of partial orders to determine necessity
        remaining_plan = ['set-state']
        for action in plan[::-1]:
            if 'explain_obs' in action: pass
            else: remaining_plan.insert(1, action)

        return remaining_plan

    except Exception as e:
        return None
