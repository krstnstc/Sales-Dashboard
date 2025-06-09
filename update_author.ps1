$oldEmail = "92261282+aanthonytomas@users.noreply.github.com"
$newEmail = "krstnstc@users.noreply.github.com"
$newName = "krstnstc"

# Update the author information for all commits
git filter-branch --env-filter "
    if [ \"$GIT_COMMITTER_EMAIL\" = \"$oldEmail\" ]; then
        export GIT_COMMITTER_NAME=\"$newName\"
        export GIT_COMMITTER_EMAIL=\"$newEmail\"
    fi
    if [ \"$GIT_AUTHOR_EMAIL\" = \"$oldEmail\" ]; then
        export GIT_AUTHOR_NAME=\"$newName\"
        export GIT_AUTHOR_EMAIL=\"$newEmail\"
    fi
" --tag-name-filter cat -- --all
