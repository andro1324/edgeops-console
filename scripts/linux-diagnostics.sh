#!/usr/bin/env bash
# Small, read-only Linux diagnostics helper for the EdgeOps Console portfolio.
set -Eeuo pipefail

printf '\n== Host ==\n'
hostnamectl 2>/dev/null || { printf 'Hostname: '; hostname; }
printf '\n== OS ==\n'
if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  printf '%s %s\n' "${PRETTY_NAME:-Linux}" "${VERSION_ID:-}"
else
  uname -a
fi
printf '\n== Uptime and load ==\n'
uptime
printf '\n== Memory ==\n'
free -h 2>/dev/null || cat /proc/meminfo | head -8
printf '\n== Disk ==\n'
df -h /
printf '\n== Top CPU processes ==\n'
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -8
printf '\n== Listening TCP ports ==\n'
if command -v ss >/dev/null 2>&1; then
  ss -lnt
else
  printf 'Install iproute2 to inspect listening sockets with ss.\n'
fi
