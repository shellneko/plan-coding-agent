#!/usr/bin/env bash

set -euo pipefail

case "$(uname -s)" in
  Darwin)
    NCPU="$(sysctl -n hw.logicalcpu)"
    ;;
  Linux)
    NCPU="$(nproc)"
    ;;
  *)
    echo "Unsupported OS: $(uname -s)" >&2
    exit 1
    ;;
esac

git clone https://github.com/eclipse-cyclonedds/cyclonedds -b releases/0.10.x 

CYCLONEDDS_SOURCE_DIR="$(cd cyclonedds && pwd)"
CYCLONEDDS_BUILD_DIR="${CYCLONEDDS_SOURCE_DIR}/build"
CYCLONEDDS_INSTALL_DIR="${CYCLONEDDS_SOURCE_DIR}/install"

mkdir -p "${CYCLONEDDS_BUILD_DIR}" "${CYCLONEDDS_INSTALL_DIR}"

cmake \
  -S "${CYCLONEDDS_SOURCE_DIR}" \
  -B "${CYCLONEDDS_BUILD_DIR}" \
  -DCMAKE_INSTALL_PREFIX="${CYCLONEDDS_INSTALL_DIR}"

cmake \
  --build "${CYCLONEDDS_BUILD_DIR}" \
  --target install \
  --parallel "${NCPU}"

CYCLONEDDS_HOME="${CYCLONEDDS_INSTALL_DIR}" uv sync