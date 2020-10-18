#!/usr/bin/env sh
# Get some property from release
# Usage:
#   get_latest_release user/repo tag_name
get_latest_release() {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
    grep "\"$2\":" |                                                # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}

# Getting last version
NEW_VER=$(get_latest_release $MK_REPO tag_name)

if [ $NEW_VER = $MK_VERSION ]; then
    echo 'Up to date';
else
    echo "A new version is available"
    body=$(get_latest_release $MK_REPO body)
    echo "Upgrading from $MK_VERSION to $NEW_VER

     Release notes
************************
$body
************************
";
    # Downloading and executing upgrade script
    curl -sL https://raw.githubusercontent.com/$MK_REPO/master/scripts/upgrade.sh | ( echo "MK_REPO=$MK_REPO; MK_VERSION=$NEW_VER; "; cat -   ) | sh
fi;