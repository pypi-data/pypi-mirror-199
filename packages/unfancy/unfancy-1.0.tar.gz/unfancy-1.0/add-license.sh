#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2022 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: CC0-1.0

#
reuse addheader --copyright "$(git config user.name) <$(git config user.email)>" --year $(date +%Y) --license "$1" "$2"
