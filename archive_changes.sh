#!/bin/bash

# 归档已完成的变更提案
DATE=$(date +%Y-%m-%d)
CHANGE_NAME="document-blog-project-overview"

# 创建归档目录
ARCHIVE_DIR="specs/changes/archive/${DATE}-${CHANGE_NAME}"
mkdir -p "${ARCHIVE_DIR}"

# 移动变更文件到归档目录
mv "specs/changes/${CHANGE_NAME}/proposal.md" "${ARCHIVE_DIR}/"
mv "specs/changes/${CHANGE_NAME}/tasks.md" "${ARCHIVE_DIR}/"
mv "specs/changes/${CHANGE_NAME}/specs" "${ARCHIVE_DIR}/"

# 删除原变更目录（如果为空）
rmdir "specs/changes/${CHANGE_NAME}" 2>/dev/null || true

echo "变更 ${CHANGE_NAME} 已归档到 ${ARCHIVE_DIR}"