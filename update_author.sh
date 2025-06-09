#!/bin/sh

git filter-branch --env-filter '
OLD_EMAIL="92261282+aanthonytomas@users.noreply.github.com"
CORRECT_NAME="krstnstc"
CORRECT_EMAIL="kristinestc18@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --all

git push --force --tags origin 'refs/heads/*'
