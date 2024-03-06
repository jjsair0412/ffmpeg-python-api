#!/bin/bash
find ./tmp -type f -exec chmod 644 {} \;
find ./tmp -type d -exec chmod 755 {} \;

exec "$@"
