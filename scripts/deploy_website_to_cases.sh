#!/usr/bin/env bash
# 将 website/ 部署到 Cases 静态资源服务器 /data/cases
# 使用前设置：REMOTE_USER REMOTE_HOST（或使用默认）
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="${REPO_ROOT}/website"
REMOTE_USER="${REMOTE_USER:-deploy}"
REMOTE_HOST="${REMOTE_HOST:-cases.wumaitech.com}"
REMOTE_PATH="${REMOTE_PATH:-/data/cases}"

echo "Deploy: $SOURCE -> ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
read -p "Continue? [y/N] " -n 1 -r; echo
[[ $REPLY =~ ^[yY]$ ]] || exit 0

rsync -avz --delete \
  --exclude="README.md" \
  "$SOURCE/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"

echo "Done. Site: http://${REMOTE_HOST}:8081/"
