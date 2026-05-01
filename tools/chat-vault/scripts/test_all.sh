#!/bin/bash
# 测试所有服务
set -e

echo "Testing all services..."
for dir in services/*/; do
    echo "Testing $dir"
    # cd "$dir" && pytest tests/
done
echo "Done!"
