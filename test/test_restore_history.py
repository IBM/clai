#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.restore_history import __remove_clai_history__


def test_should_remove_when_not_commands():
    lines = []

    new_lines = __remove_clai_history__(lines, "ls")

    assert new_lines == []


def test_should_remove_the_list_if_only_one_command():
    lines = ["ls"]

    new_lines = __remove_clai_history__(lines, "ls")

    assert new_lines == ["ls"]


def test_should_remove_last_command_if_have_two_repeat():
    lines = ["pwd", "ls", "ls"]

    new_lines = __remove_clai_history__(lines, "ls")

    assert new_lines == ["pwd", "ls"]


def test_should_remove_nothing_if_have_only_the_command():
    lines = ["pwd", "ls"]

    new_lines = __remove_clai_history__(lines, "ls")

    assert new_lines == ["pwd", "ls"]


def test_should_remove_dirty_until_the_command():
    lines = ["pwd", "ls", "pwd", "cd"]

    new_lines = __remove_clai_history__(lines, "ls")

    assert new_lines == ["pwd", "ls"]


def test_should_not_remove_if_command_not_exist():
    lines = ["pwd", "ls"]

    new_lines = __remove_clai_history__(lines, "ls -la")

    assert new_lines == ["pwd", "ls"]


def test_should_remove_dirt_if_it_is_the_first_comment():
    lines = ["clai", ":"]

    new_lines = __remove_clai_history__(lines, "clai")

    assert new_lines == ["clai"]
