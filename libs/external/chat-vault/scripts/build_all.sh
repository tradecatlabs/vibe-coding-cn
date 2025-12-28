#!/bin/bash
# 构建所有服务
set -e

echo "Building all services..."
for dir in services/*/; do
    echo "Building $dir"
    # docker build -t "${dir%/}" "$dir"
done
echo "Done!"
